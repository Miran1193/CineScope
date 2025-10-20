from django.shortcuts import render
import requests, os 
from .models import Movie

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

def get_popular_movies():
    url = f"{BASE_URL}/movie/popular"
    params = {
        'api_key': API_KEY,
        'language': 'en-US',
        'page': 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        print(f"Except {response.status_code}")
        return []
    

def save_movies_to_db():
    movies = get_popular_movies()
    for m in movies:
        Movie.objects.get_or_create(
            tmdb_id=m['id'],
            defaults={
                'title': m['title'],
                'description': m['description'],
                'poster_url': f"https://image.tmdb.org/t/p/w500{m['poster_path']}"
            }
        )
