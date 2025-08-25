import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

def fetch_data(movie_title):
    """
    Makes an API call to get information about a movie.
    Returns a list of animal data in JSON format or None in case of an Error.
    """
    api_url = f'https://www.omdbapi.com/?apikey={api_key}&t={movie_title}'
    response = requests.get(api_url)

    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

print(fetch_data('one'))