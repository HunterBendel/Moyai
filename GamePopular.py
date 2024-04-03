from bs4 import BeautifulSoup
import requests
import time

#Video used: https://youtu.be/XVv6mJpFOb0?si=MFGV69vfcdMvNw6P

def game_popular(game_name):
    #game_name = input("Please enter the name of the game that you want to find the popularity for: ") #SPELLING AND CAPITALIZATION MATTERS
    app_id = None
    # Lines 11 to 23 are just to retrieve the game ID so we can use it for the webscraping
    api_data = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    if api_data.status_code == 200:
        data = api_data.json()
        for app in data["applist"]["apps"]:
            if app["name"] == game_name:
                app_id = app["appid"]
                break
        if app_id:
            print(f"The AppID for '{game_name}' is: {app_id}")
        else:
            print(f"Game '{game_name}' not found.")
    else:
        print(f"Failed to retrieve data: {api_data.status_code}")

    if app_id:
        lower_game_name = game_name.lower()
        lower_game_name_format = lower_game_name.replace(" ", "-")
        game_popular_link = requests.get(f'https://steambase.io/games/{lower_game_name_format}/steam-charts').text
        soup = BeautifulSoup(game_popular_link, 'html.parser')

        total_ingame = soup.find('span', class_='text-2xl font-bold text-white').text
        print(total_ingame)

        total_upvote = soup.find('span', class_='text-green-400').text
        print(total_upvote)

        total_downvote = soup.find('span', class_='text-red-400').text
        print(total_downvote)

        total_upvote_format = float(total_upvote.replace(",", ""))
        total_downvote_format = float(total_downvote.replace(",", ""))

        upvote_percentage = round((total_upvote_format / (total_upvote_format + total_downvote_format)*100), 2)
        str_upvote_percentage = str(upvote_percentage) + "%"
        #print(round((upvote_percentage * 100), 2))

        return total_ingame, total_upvote, total_downvote, str_upvote_percentage