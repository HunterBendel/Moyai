from bs4 import BeautifulSoup
import requests

def get_latest_game_news(game_name, count=3, maxlength=300):
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

    url = f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={app_id}&count={count}&maxlength={maxlength}&format=json"
    response = requests.get(url)
    data = response.json()
    
    if 'appnews' in data and 'newsitems' in data['appnews']:
        news_items = []
        for item in data['appnews']['newsitems']:
            soup = BeautifulSoup(item['contents'], 'html.parser')
            clean_text = soup.get_text()  # This removes all HTML tags and returns clean text
            news_items.append({
                'title': item['title'],
                'url': item['url'],
                'contents': clean_text
            })
        return news_items
    return []