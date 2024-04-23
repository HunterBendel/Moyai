import requests
from bs4 import BeautifulSoup

def get_steam_game_description(game_name):
    app_id = None
    api_data = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    if api_data.status_code == 200:
        data = api_data.json()
        for app in data["applist"]["apps"]:
            if app["name"].lower() == game_name.lower():
                app_id = app["appid"]
                break

    if not app_id:
        return "Game not found or invalid game name"
    
    url = f"http://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    data = response.json()
    
    if data[str(app_id)]['success']:
        html_content = data[str(app_id)]['data']['detailed_description']
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Assuming the main game description follows the "About the Game" heading
        about_the_game = soup.find('h1', text='About the Game')
        if about_the_game:
            next_siblings = about_the_game.find_next_siblings(text=True)
            if next_siblings:
                description = ' '.join(next_siblings).strip()
                return description
        
        return "Description not found."
    else:
        return "Game not found or invalid AppID"
