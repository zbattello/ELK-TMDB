import requests
import time
import datetime

# API key and URL TMDB
api_key = '1d2a958442de161a2791dc703cb9dcbc'
base_url = 'https://api.themoviedb.org/3/'

def get_existing_ids(csv_filename):
    existing_ids = set()
    try:
        with open(csv_filename, 'r', newline='', encoding='utf-8') as file:
            for row in file:
                id = row.split(',')[0]
                existing_ids.add(id)
    except FileNotFoundError:
        pass
    return existing_ids

# Function to get changed IDs from the API
def get_changed_ids(api_url):
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Error fetching changed IDs: {response.status_code} - {response.text}")
        return []

    data = response.json()
    changed_ids = [str(item.get('id')) for item in data.get('results', [])]
    return changed_ids

# Function to update data for changed IDs
def update_changed_ids(api_url, is_movie, log_filename, existing_ids):
    changed_ids = get_changed_ids(api_url)

    for id in changed_ids:
        url = f'{base_url}{is_movie and "movie" or "tv"}/{id}?language=en-US&api_key={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            item_data = response.json()
            write_to_log(log_filename, [item_data], is_movie, existing_ids)

# Function to write data to log file
def write_to_log(log_filename, data, is_movie, existing_ids):
    with open(log_filename, 'a', encoding='utf-8') as file:
        if not existing_ids:
            headers = ['ID', 'Title', 'Vote Average', 'Date', 'Original Language', 'Genre IDs', 'IsMovie']
            file.write('\t'.join(headers) + '\n')

        for item in data:
            id = str(item.get('id'))
            if id not in existing_ids:
                title = item.get('title') if is_movie else item.get('name')
                vote_average = item.get('vote_average')
                date = item.get('release_date') if is_movie else item.get('first_air_date')
                original_language = item.get('original_language')
                genre_ids = item.get('genre_ids')

                # Check if the ID already exists in the log file
                if id not in existing_ids:
                    file.write(f"{id}\t{title}\t{vote_average}\t{date}\t{original_language}\t{genre_ids}\t{is_movie}\n")
                    existing_ids.add(id)

# Function to continuously get new IDs and infos from the API
def continuously_get_new_data():
    while True:
        # Get new IDs from the API
        tv_changes_url = f'{base_url}tv/changes?page=1&api_key={api_key}'
        movie_changes_url = f'{base_url}movie/changes?page=1&api_key={api_key}'

        # Get existing IDs from the log file
        existing_ids = get_existing_ids('new_list.log')

        # Update changed IDs and write to new_list.log
        update_changed_ids(tv_changes_url, False, 'new_list.log', existing_ids)
        update_changed_ids(movie_changes_url, True, 'new_list.log', existing_ids)

        # Wait for 24 hours before checking for new data again
        time.sleep(24 * 60 * 60)

# Start the process to continuously get new data
continuously_get_new_data()
