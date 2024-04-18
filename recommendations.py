import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def create_user_item_matrix(data):
    # Creating a user-item matrix
    user_item_matrix = data.pivot_table(index='user_id', columns='game_id', aggfunc='size', fill_value=0)
    return user_item_matrix

def calculate_similarity(user_item_matrix):
    # Calculating cosine similarity between users
    similarity_matrix = cosine_similarity(user_item_matrix)
    similarity_df = pd.DataFrame(similarity_matrix, index=user_item_matrix.index, columns=user_item_matrix.index)
    return similarity_df

def recommend_games(user_id, similarity_df, user_item_matrix, top_n=6):
    # Find top N similar users
    if user_id not in similarity_df.index:
        return []
    similar_users = similarity_df[user_id].sort_values(ascending=False).iloc[1:].head(top_n).index
    # Find games liked by similar users that the current user hasn't seen
    similar_users_preferences = user_item_matrix.loc[similar_users]
    recommended_games = similar_users_preferences.sum().sort_values(ascending=False)
    already_owned_games = user_item_matrix.loc[user_id]
    recommended_games = recommended_games[already_owned_games == 0]  # Filter out games the user already has
    return recommended_games.head(top_n).index.tolist()

def get_recommendations(user_id, data):
    user_item_matrix = create_user_item_matrix(data)
    similarity_df = calculate_similarity(user_item_matrix)
    recommendations = recommend_games(user_id, similarity_df, user_item_matrix)
    return recommendations
