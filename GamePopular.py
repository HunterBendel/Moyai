from bs4 import BeautifulSoup
import requests
import time

def game_popular(game_name):
    app_id = None
    api_data = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    if api_data.status_code == 200:
        data = api_data.json()
        for app in data["applist"]["apps"]:
            if app["name"] == game_name:
                app_id = app["appid"]
                break
        if app_id:
            print(f"GamePopular: The AppID for '{game_name}' is: {app_id}")
        else:
            print(f"GamePopular: Game '{game_name}' not found.")
            return "Data not found", "Data not found", "Data not found", "Data not found"
    else:
        print(f"GamePopular: Failed to retrieve data: {api_data.status_code}")
        return "Data not found", "Data not found", "Data not found", "Data not found"

    if app_id:
        lower_game_name = game_name.lower()
        lower_game_name_format = lower_game_name.replace(" ", "-")
        game_popular_link = requests.get(f'https://steambase.io/games/{lower_game_name_format}/steam-charts').text
        soup = BeautifulSoup(game_popular_link, 'html.parser')

        total_ingame = soup.find('span', class_='text-2xl font-bold text-white')
        total_ingame = total_ingame.text if total_ingame else "Data not found"

        total_upvote = soup.find('span', class_='text-green-400')
        total_upvote = total_upvote.text if total_upvote else "Data not found"

        total_downvote = soup.find('span', class_='text-red-400')
        total_downvote = total_downvote.text if total_downvote else "Data not found"

        if total_upvote != "Data not found" and total_downvote != "Data not found":
            total_upvote_format = float(total_upvote.replace(",", ""))
            total_downvote_format = float(total_downvote.replace(",", ""))
            upvote_percentage = round(total_upvote_format / (total_upvote_format + total_downvote_format) * 100, 2)
        else:
            upvote_percentage = "Data not found"

        return total_ingame, total_upvote, total_downvote, upvote_percentage
    else:
        return "Data not found", "Data not found", "Data not found", "Data not found"
