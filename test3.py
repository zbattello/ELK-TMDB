import requests
import csv
import time

# API key and URL setup
api_key = '1d2a958442de161a2791dc703cb9dcbc'
base_url = 'https://api.themoviedb.org/3/'

# Function to write or append data to CSV
def write_or_append_to_csv(csv_filename, url, is_movie, mode):
    page = 1
    entry_count = 0
    with open(csv_filename, mode, newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        # Write headers only if it's in write mode
        if mode == 'w':
            headers = ['ID', 'Title', 'Vote Average', 'Date', 'Original Language', 'Genre IDs', 'IsMovie']
            csv_writer.writerow(headers)

        while entry_count < 20000:  # Assuming you want to stop at 20,000 entries
            try:
                response = requests.get(f'{url}&page={page}')
                if page > 490:
                    print(page)
                
                if response.status_code != 200:
                    print(f"Error fetching page {page}: {response.status_code} - {response.text}")
                    break

                data = response.json()

                if 'results' in data:
                    for item in data['results']:
                        id = item.get('id')
                        title = item.get('title') if is_movie else item.get('name')
                        vote_average = item.get('vote_average')
                        date = item.get('release_date') if is_movie else item.get('first_air_date')
                        original_language = item.get('original_language')
                        genre_ids = item.get('genre_ids')
                        csv_writer.writerow([id, title, vote_average, date, original_language, genre_ids, is_movie])
                        entry_count += 1

                        if entry_count >= 20000:
                            break

                    page += 1
                    if page > 500:  # To avoid going over the API limit
                        break
                else:
                    print(f"No more results at page {page}")
                    break
            except Exception as e:
                print(f"An exception occurred: {e}")
                break

            time.sleep(1)  # Delay to avoid hitting rate limits

# URLs for movies and TV shows
url_movies = f'{base_url}discover/movie?api_key={api_key}'
url_tv_shows = f'{base_url}discover/tv?api_key={api_key}'

# Output filename
output_filename = 'media_list.csv'

# Write movie data to CSV
write_or_append_to_csv(output_filename, url_movies, True, 'w')

# Append TV show data to CSV
write_or_append_to_csv(output_filename, url_tv_shows, False, 'a')
