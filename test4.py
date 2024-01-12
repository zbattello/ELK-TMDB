import requests
import json

# API key and URL setup
api_key = '1d2a958442de161a2791dc703cb9dcbc'
base_url = 'https://api.themoviedb.org/3/'

# Action genre ID for TV shows (assuming it's the same as movies, but you might need to verify this)
action_genre_id = 10759

# Discover URL for action TV shows
url = f'{base_url}discover/tv?api_key={api_key}&with_genres={action_genre_id}'

# Initialize variables
total_shows = 0
page = 1
update_interval = 10  # Interval to print the number of shows retrieved
tv_shows_list = []  # List to store all TV shows

try:
    while True:
        response = requests.get(f'{url}&page={page}')
        data = response.json()

        if 'results' in data:
            shows_found = len(data['results'])
            if shows_found == 0:
                # No more shows found, stop the loop
                break
            total_shows += shows_found
            tv_shows_list.extend(data['results'])  # Add shows to the list

            if total_shows % update_interval == 0:
                print(f'Number of TV shows retrieved: {total_shows}')
        else:
            print(f"Warning: No 'results' found on page {page}.")
            print(f"Response: {data}")
            break

        if total_shows >= 10 or page >= 500:  # Stopping at 10 TV shows
            break

        page += 1
except Exception as e:
    print(f"An error occurred: {e}")

# Output the final count
print(f'Total number of action TV shows: {total_shows}')

# Save the TV shows list to a JSON file
with open('tv_shows_list.json', 'w') as file:
    json.dump(tv_shows_list, file, indent=4)
