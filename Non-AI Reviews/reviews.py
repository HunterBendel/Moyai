from bs4 import BeautifulSoup
import requests
import json

# https://gptzero.stoplight.io/docs/gptzero-api/d2144a785776b-ai-detection-on-single-string

# For now the input is manual
# Need to clarify if we will use reviews from webscraping, database, or both
# For now enter input as '{"document": "string"}'
review_input = input("Enter text: ")
review_json = json.loads(review_input)
ai_probability = requests.post(f'https://api.gptzero.me/v2/predict/review_json')
print(ai_probability)