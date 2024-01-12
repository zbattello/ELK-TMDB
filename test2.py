import requests

# API key and URL setup
api_key = '1d2a958442de161a2791dc703cb9dcbc'
base_url = 'https://api.themoviedb.org/3/'

# Discover URL for movies
url_movies = f'{base_url}discover/movie?api_key={api_key}'

# Make a request to get the total number of movies
response_movies = requests.get(f'{url_movies}&year=2024&page=1')
data_movies = response_movies.json()

# Extract the total number of movies
total_movies = data_movies['total_results'] if 'total_results' in data_movies else None
print(total_movies)

# Discover URL for TV shows
url_tv = f'{base_url}discover/tv?api_key={api_key}'

# Make a request to get the total number of TV shows
response_tv = requests.get(f'{url_tv}&page=1')
#print(data_movies)
data_tv = response_tv.json()

# Extract the total number of TV shows
total_tv_shows = data_tv['total_results'] if 'total_results' in data_tv else None
print(total_tv_shows)
#print(data_tv)
