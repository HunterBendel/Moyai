from bs4 import BeautifulSoup
import requests

def get_ign_score(game_name):
    # Construct the URL to search for the game's IGN review on Yahoo
    search_url = f'https://search.yahoo.com/search?p={game_name.replace(" ", "+")}+IGN+Review'

    # Send a request to the URL
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the element containing the score
    score_element = soup.find('label', class_='fw-b')
    if score_element:
        return score_element.text.strip()
    else:
        return "Score not found"