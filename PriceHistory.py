from bs4 import BeautifulSoup
import requests
import time

def lowest_price_history(game_name):
    app_id = None
    api_data = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    if api_data.status_code == 200:
        data = api_data.json()
        for app in data["applist"]["apps"]:
            if app["name"] == game_name:
                app_id = app["appid"]
                break
        if app_id:
            print(f"PriceHistory: The AppID for '{game_name}' is: {app_id}")
        else:
            print(f"PriceHistory: Game '{game_name}' not found.")
            return "Data not found", "Data not found", "Data not found"
    else:
        print(f"PriceHistory: Failed to retrieve data: {api_data.status_code}")
        return "Data not found", "Data not found", "Data not found"

    if app_id:
        game_price_link = requests.get(f'https://steampricehistory.com/app/{app_id}').text
        soup = BeautifulSoup(game_price_link, 'lxml')
        table = soup.find('table', class_='data-table')
        if table is not None:
            rows = table.find_all('tr')
            for row in rows:
                prices = row.find_all('td')
                if prices:
                    current_price = prices[0].text.strip()
                    highest_price = prices[1].text.strip()
                    lowest_price = prices[2].text.strip()
                    return current_price, highest_price, lowest_price
        else:
            print("Table not found")
            return "Data not found", "Data not found", "Data not found"
    else:
        return "Data not found", "Data not found", "Data not found"
