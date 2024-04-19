import requests
from bs4 import BeautifulSoup

def get_steam_game_details(game_name):
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
        game_data = data[str(app_id)]['data']
        details = {
            'developer': ', '.join(game_data.get('developers', ['Not available'])),
            'publisher': ', '.join(game_data.get('publishers', ['Not available'])),
            'release_date': game_data['release_date']['date'] if 'release_date' in game_data and 'date' in game_data['release_date'] else 'Not available'
        }
        return details
    else:
        return "Game details not found or invalid AppID"