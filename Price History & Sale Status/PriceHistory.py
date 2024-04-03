from bs4 import BeautifulSoup
import requests
import time

#Video used: https://youtu.be/XVv6mJpFOb0?si=MFGV69vfcdMvNw6P

def lowest_price_history():
    game_name = input("Please enter the name of the game that you want to find the lowest price for: ") #SPELLING AND CAPITALIZATION MATTERS
    app_id = None
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
        game_price_link = requests.get(f'https://steampricehistory.com/app/{app_id}').text
        soup = BeautifulSoup(game_price_link, 'lxml')
        # Find the table with class 'data-table'
        table = soup.find('table', class_='data-table')
        # Find all 'tr' elements in the table
        rows = table.find_all('tr')
        
        # Iterate through each row and get prices
        for row in rows:
            # Using 'td' tags to find the relevant data since they hold the price values
            prices = row.find_all('td')
            if prices:
                current_price = prices[0].text.strip()
                highest_price = prices[1].text.strip()
                lowest_price = prices[2].text.strip()
                # print(f'Current Price: {current_price}')
                # print(f'Highest Price: {highest_price}')
                # print(f'Lowest Price: {lowest_price}')
                return current_price, highest_price, lowest_price

if __name__ == '__main__':
    cur, high, low = lowest_price_history()
    print(f'Current Price: {cur}')
    print(f'Highest Price: {high}')
    print(f'Lowest Price: {low}')