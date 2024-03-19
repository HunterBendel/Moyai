import requests
from bs4 import BeautifulSoup
import sqlite3
import json

def fetch_steam_apps():
    url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            return data['applist']['apps']
        except json.decoder.JSONDecodeError:
            print(f"Failed to parse JSON from response: {response.text}")
    else:
        print(f"Request to {url} failed with status code {response.status_code}")
    return []

def fetch_app_details(app_id):
    url = f'https://store.steampowered.com/api/appdetails?appids={app_id}'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            if data and str(app_id) in data and 'data' in data[str(app_id)] and data[str(app_id)]['success']:
                return data[str(app_id)]['data']
        except json.decoder.JSONDecodeError:
            print(f"Failed to parse JSON from response: {response.text}")
    else:
        print(f"Request to {url} failed with status code {response.status_code}")
    return None

def fetch_cover_image_url(app_id):
    store_url = f"https://store.steampowered.com/app/{app_id}"
    response = requests.get(store_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        cover_image_tag = soup.find('img', class_='game_header_image_full')
        if cover_image_tag:
            return cover_image_tag['src']
    else:
        print(f"Request to {store_url} failed with status code {response.status_code}")
    return None

def insert_game_into_db(game_name, cover_image_url):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO game (name, cover_image_url) VALUES (?, ?)", (game_name, cover_image_url))
    conn.commit()
    conn.close()

def populate_game_table():
    apps = fetch_steam_apps()
    for app in apps:
        details = fetch_app_details(app['appid'])
        if details and details['type'] == 'game':
            cover_image_url = fetch_cover_image_url(app['appid'])
            if cover_image_url:
                insert_game_into_db(details['name'], cover_image_url)

if __name__ == '__main__':
    populate_game_table()
