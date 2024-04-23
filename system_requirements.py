import requests

def get_steam_system_requirements(game_name):
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
        requirements = game_data.get('pc_requirements', {})
        minimum = requirements.get('minimum', 'Minimum requirements not available')
        recommended = requirements.get('recommended', 'Recommended requirements not available')
        
        # Returning system requirements as a dictionary
        return {
            'minimum': minimum,
            'recommended': recommended
        }
    else:
        return "System requirements not found or invalid AppID"

# Example usage:
requirements = get_steam_system_requirements('Portal 2')
print(requirements)
