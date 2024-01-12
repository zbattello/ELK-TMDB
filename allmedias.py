import requests
import csv
import time

# API key and URL TMBD
api_key = '1d2a958442de161a2791dc703cb9dcbc'
base_url = 'https://api.themoviedb.org/3/'

# Function to read existing IDs from CSV
def get_existing_ids(csv_filename):
    existing_ids = set()
    try:
        with open(csv_filename, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                existing_ids.add(row[0])  # ID is the first column
    except FileNotFoundError:
        pass  # File doesn't exist yet
    return existing_ids

# Function to write or append data to CSV
def write_or_append_to_csv(csv_filename, url, is_movie, existing_ids, start_page, end_page):
    with open(csv_filename, 'a', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        # Write headers only if the file is newly created
        if not existing_ids and start_page == 1:
            headers = ['ID', 'Title', 'Vote Average', 'Date', 'Original Language', 'Genre IDs', 'IsMovie']
            csv_writer.writerow(headers)

        for page in range(start_page, end_page + 1):
            if page > end_page:  # To avoid going over the API limit
                        break
            response = requests.get(f'{url}&page={page}')
            if response.status_code != 200:
                print(f"Error fetching page {page}: {response.status_code} - {response.text}")
                break

            data = response.json()

            if 'results' in data:
                for item in data['results']:
                    id = str(item.get('id'))  # Ensure ID is a string for set comparison
                    if id not in existing_ids:
                        title = item.get('title') if is_movie else item.get('name')
                        vote_average = item.get('vote_average')
                        date = item.get('release_date') if is_movie else item.get('first_air_date')
                        original_language = item.get('original_language')
                        genre_ids = item.get('genre_ids')
                        csv_writer.writerow([id, title, vote_average, date, original_language, genre_ids, is_movie])
                        existing_ids.add(id)

            time.sleep(1)  # Delay to avoid hitting rate limits

# Output filename
output_filename = 'media_list.csv'

# Get existing IDs from the CSV
existing_ids = get_existing_ids(output_filename)

# Function to process movies or TV shows in chunks
def process_in_chunks(url, is_movie, total_pages, chunk_size=500):
    for start_page in range(1, total_pages, chunk_size):
        start_time = time.time()  # Start time

        end_page = min(start_page + chunk_size - 1, total_pages)
        print('isMovie: ' + str(is_movie) + ' - retrieve from page: ' + str(start_page) + ' to ' + str(end_page))

        write_or_append_to_csv(output_filename, url, is_movie, existing_ids, start_page, end_page)

        end_time = time.time()  # End time
        elapsed_time = end_time - start_time  
        print('end chunk - Time taken: {:.2f} seconds'.format(elapsed_time))

# Define total pages for movies and TV shows
total_movie_pages = 41848
total_tv_show_pages = 8107

# URLs for movies and TV shows
url_movies = f'{base_url}discover/movie?api_key={api_key}&year=2024'
url_tv_shows = f'{base_url}discover/tv?api_key={api_key}&year=2024'

# Process movies and TV shows in chunks
process_in_chunks(url_movies, True, total_movie_pages)
process_in_chunks(url_tv_shows, False, total_tv_show_pages)
