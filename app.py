import os
import sqlite3
from flask import Flask, jsonify, render_template, redirect, url_for, request, flash
from flask import session as flask_session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length #if you didnt type something in the field it will alert, (there's validators for email addresses)
from flask_sqlalchemy import SQLAlchemy, session #database
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_change_password import ChangePassword, ChangePasswordForm
from IGNscore import get_ign_score
from PriceHistory import lowest_price_history
from GamePopular import game_popular
from vendors import get_game_deals
from youtube_embed import get_youtube_trailer_url

app = Flask(__name__)  # Create application object
app.config['SECRET_KEY'] = 'This is my super secret key'
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
flask_change_password = ChangePassword(min_password_length=8, rules=dict(long_password_override=2))
flask_change_password.init_app(app)

with app.app_context():
    db.create_all()

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    first = db.Column(db.String(80))
    last = db.Column(db.String(80)) 

class UserGame(db.Model):
    __tablename__ = 'user_game'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cover_image_url = db.Column(db.String(255), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
	remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    first = StringField('first name', validators=[InputRequired(), Length(min=2, max=80)])
    last = StringField('last name', validators=[InputRequired(), Length(min=2, max=80)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
@login_required
def home():
    return render_template('home_page.html', name=current_user.username)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile_page.html', name=current_user.username)

@app.route('/about')
@login_required
def settings():
    return render_template('about.html', name=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login_page.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            return '<h1>Username already exists. Please choose a different username.</h1>'

        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256') # Update the method argument to 'pbkdf2:sha256'
        new_user = User(first=form.first.data, last=form.last.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1><p>You may now <a class="btn btn-lg btn-primary btn-block" href="login" role="button">Log in</a></p>'

    return render_template('signup_page.html', form=form)

@app.route('/changed/<title>/<new_password>')
@login_required
def page_changed(title, new_password=''):
    return render_template('changed.html', title=title, new_password=new_password, name=current_user.username)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def page_change_password():
    title = 'Change Password'
    form = ChangePasswordForm(username=current_user.username, changing=True, title=title)
    if form.validate_on_submit():
        valid = flask_change_password.verify_password_change_form(form)
        if valid:
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            current_user.password = hashed_password
            db.session.commit()
            return redirect(url_for('page_changed', title='changed', new_password=form.password.data))

        return redirect(url_for('page_change_password'))
    password_template = flask_change_password.change_password_template(form, submit_text='Change')
    return render_template('change_password.html', password_template=password_template, title=title, form=form,
                           user=dict(username=current_user.username), name=current_user.username)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # This will enable column access by name
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM game WHERE name LIKE ?", ('%' + query + '%',))
    games = [dict(row) for row in cursor.fetchall()]

    conn.close()
    
    return render_template('search_results.html', games=games, name=current_user.username, query=query)

@app.route('/game_details')
def game_details():
    game_id = request.args.get('game_id')
    user_id = current_user.id
    game_in_library = UserGame.query.filter_by(user_id=user_id, game_id=game_id).first() is not None
    game_name = request.args.get('game_name', None)
    cover_image_url = request.args.get('cover_image_url')
    if not game_name:  # Handling cases where game_name is None
        game_details = db.session.query(Game).filter_by(id=game_id).first()
        if game_details:
            game_name = game_details.name  # Use name from the database if not passed as parameter
            cover_image_url = game_details.cover_image_url  # Similarly for the cover image URL
        else:
            return 'Game not found', 404  # Or redirect to another appropriate error handling page
    youtube_trailer_url = get_youtube_trailer_url(game_name, 'AIzaSyDhDfW13uJDS1DRgSplLwDLTbvLF_x3New')
    current_price, highest_price, lowest_price = lowest_price_history(game_name)
    total_ingame, total_upvote, total_downvote, upvote_percentage = game_popular(game_name)
    ign_score = get_ign_score(game_name)
    deals = get_game_deals(game_name)
    game_details = db.session.query(Game).filter_by(id=game_id).first()
    if game_details:
        return render_template('game-details.html', 
                                game_id=game_id, 
                                game_name=game_name, 
                                cover_image_url=cover_image_url, 
                                name=current_user.username,
                                current_price=current_price,
                                highest_price=highest_price,
                                lowest_price=lowest_price,
                                total_ingame=total_ingame, 
                                total_upvote=total_upvote, 
                                total_downvote=total_downvote, 
                                upvote_percentage=upvote_percentage,
                                ign_score=ign_score,
                                youtube_trailer_url=youtube_trailer_url,
                                deals=deals,
                                game=game_details,
                                game_in_library=game_in_library)  # Add this to pass the library status to the template
    else:
        return 'Game not found', 404

@app.route('/add_to_library/<int:game_id>', methods=['POST'])
def add_to_library(game_id):
    user_id = current_user.id
    new_entry = UserGame(user_id=user_id, game_id=game_id)
    db.session.add(new_entry)
    try:
        db.session.commit()
        game_name = request.args.get('game_name')
        cover_image_url = request.args.get('cover_image_url')
        # Redirect with necessary details
        return redirect(url_for('game_details', game_id=game_id, game_name=game_name, cover_image_url=cover_image_url))
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to add game to library'})

@app.route('/remove_from_library/<int:game_id>', methods=['POST'])
def remove_from_library(game_id):
    user_id = current_user.id
    # Assuming UserGame is the model for the user_game table
    game_entry = UserGame.query.filter_by(user_id=user_id, game_id=game_id).first()
    if game_entry:
        db.session.delete(game_entry)
        try:
            db.session.commit()
            game_name = request.args.get('name')
            cover_image_url = request.args.get('cover_image_url')
            # Redirect with necessary details
            return redirect(url_for('game_details', game_id=game_id, game_name=game_name, cover_image_url=cover_image_url))
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Failed to remove game from library'})
    else:
        return jsonify({'success': False, 'message': 'Game not found in library'})

@app.route('/myGames')
def myGames():
    user_id = current_user.id
    # Fetch games from the user_game association table joined with the game table
    user_games = db.session.query(Game).join(UserGame, UserGame.game_id == Game.id).filter(UserGame.user_id == user_id).all()
    return render_template('myGames.html', games=user_games, name=current_user.username)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True)  # Run our application
