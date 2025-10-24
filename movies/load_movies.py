import requests, os
from movies.models import Movie

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

def get_popular_movies():
    url = "https://kinopoiskapiunofficial.tech/api/v2.2/films/top"
    headers = {
            'X-API-KEY': 'e4b0d4d9-1c02-4a5c-8381-3f2031de3845',
            'Content-Type': 'application/json',
        }
    params = {
            'type': 'TOP_100_POPULAR_FILMS',
            'page': 1
        }
    response = requests.get(url,headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['films']
    else:
        print(f"Except {response.status_code}")
        return []
    

def save_movies_to_db():
    movies = get_popular_movies()
    for m in movies:
        Movie.objects.get_or_create(
            tmdb_id=m.get('filmId'),
            defaults={
                'title': m.get('nameRu') or m.get('nameEn') or 'Без названия',
                'description': m.get('description') or 'Описание отсутствует',
                'poster_url': m.get('posterUrl') or ''
            }
        )
