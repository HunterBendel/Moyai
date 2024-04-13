import requests

def get_store_lookup():
    # This function maps store IDs to store names
    return {
        '1': 'Steam', '2': 'GamersGate', '3': 'GreenManGaming', '4': 'Amazon', '5': 'GameStop', '6': 'Direct2Drive', '7': 'GOG', '8': 'Origin', '9': 'Get Games', '10': 'Shiny Loot',
        '11': 'Humble Store', '12': 'Desura', '13': 'Uplay', '14': 'IndieGameStand', '15': 'Fanatical', '16': 'Gamesrocket', '17': 'Games Republic', '18': 'SilaGames',
        '19': 'Playfield', '20': 'ImperialGames', '21': 'WinGameStore', '22': 'FunStockDigital', '23': 'GameBillet', '24': 'Voidu', '25': 'Epic Games Store', '26': 'Razer Game Store',
        '27': 'Gamesplanet', '28': 'Gamesload', '29': '2Game', '30': 'IndieGala', '31': 'Blizzard Shop', '32': 'AllYouPlay', '33': 'DLGamer', '34': 'Noctre', '35': 'DreamGame'
    }

def get_steam_id(game_name):
    app_id = None
    api_data = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    if api_data.status_code == 200:
        data = api_data.json()
        for app in data["applist"]["apps"]:
            if app["name"] == game_name:
                app_id = app["appid"]
                break
        if app_id:
            return app_id
                

def get_game_deals(game_name):
    # Step 1: Retrieve the gameID using steamAppID
    steamAppID = get_steam_id(game_name)
    game_lookup_url = f"https://www.cheapshark.com/api/1.0/games?steamAppID={steamAppID}"
    game_lookup_response = requests.get(game_lookup_url)
    game_lookup_data = game_lookup_response.json()

    if not game_lookup_data:
        print("No games found for the given steamAppID.")
        return "No games found for the given steamAppID."

    gameID = game_lookup_data[0]['gameID']  # Assume the first entry is correct

    # Step 2: Retrieve deals using the gameID
    game_deals_url = f"https://www.cheapshark.com/api/1.0/games?id={gameID}"
    game_deals_response = requests.get(game_deals_url)
    game_deals_data = game_deals_response.json()

    # List to store active deals with detailed info
    active_deals = []

    # Step 3: Fetch each deal's detailed information
    for deal in game_deals_data['deals']:
        deal_lookup_url = f"https://www.cheapshark.com/api/1.0/deals?id={deal['dealID']}"
        deal_response = requests.get(deal_lookup_url)
        deal_data = deal_response.json()
    
        # Convert prices to float and format as string with two decimals
        sale_price = float(deal_data['gameInfo']['salePrice'])
        formatted_sale_price = f"{sale_price:.2f}"  # Ensuring two decimal places
        retail_price = float(deal_data['gameInfo']['retailPrice'])

        # Check if the sale price is less than the retail price
        if sale_price < retail_price:
            deal_url = f"https://www.cheapshark.com/redirect?dealID={deal['dealID']}"
            active_deals.append({
                'store': get_store_lookup().get(deal_data['gameInfo']['storeID'], 'Unknown store'),
                'salePrice': formatted_sale_price,
                'dealUrl': deal_url  # Include the deal URL
            })

    if not active_deals:
        print("No active deals! Check back tomorrow!")
        return "No active deals! Check back tomorrow!"


    return active_deals