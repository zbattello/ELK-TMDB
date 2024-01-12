import requests
import json

# API key and URL setup
api_key = '1d2a958442de161a2791dc703cb9dcbc'
base_url = 'https://api.themoviedb.org/3/'

# Action genre ID
action_genre_id = 28

# Discover URL for action movies
url = f'{base_url}discover/movie?api_key={api_key}&with_genres={action_genre_id}'

# Initialize variables
total_movies = 0
page = 1
update_interval = 105  # Interval to print the number of films retrieved
movies_list = []  # List to store all movies

try:
    while True:
        response = requests.get(f'{url}&page={page}')
        data = response.json()

        if 'results' in data:
            movies_found = len(data['results'])
            if movies_found == 0:
                # No more movies found, stop the loop
                break
            total_movies += movies_found
            movies_list.extend(data['results'])  # Add movies to the list

            if total_movies % update_interval == 0:
                print(f'Number of films retrieved: {total_movies}')
        else:
            print(f"Warning: No 'results' found on page {page}.")
            print(f"Response: {data}")
            break

        if total_movies >= 1000000 or page >= 500:
            break

        page += 1
except Exception as e:
    print(f"An error occurred: {e}")

# Output the final count
print(f'Total number of action movies: {total_movies}')

# Save the movies list to a JSON file
with open('movies_list.json', 'w') as file:
    json.dump(movies_list, file, indent=4)
