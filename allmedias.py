import datetime
import requests
import csv
import time
import calendar

# API key and URL TMDB
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
                existing_ids.add(row[0])  # ID in first column
    except FileNotFoundError:
        pass  
    return existing_ids

# Function to write data to CSV
def write_or_append_to_csv(csv_filename, data, is_movie, existing_ids):
    with open(csv_filename, 'a', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        if not existing_ids:
            headers = ['ID', 'Title', 'Vote Average', 'Date', 'Original Language', 'Genre IDs', 'IsMovie']
            csv_writer.writerow(headers)

        for item in data:
            id = str(item.get('id')) 
            if id not in existing_ids:
                title = item.get('title') if is_movie else item.get('name')
                vote_average = item.get('vote_average')
                date = item.get('release_date') if is_movie else item.get('first_air_date')
                original_language = item.get('original_language')
                genre_ids = item.get('genre_ids')
                csv_writer.writerow([id, title, vote_average, date, original_language, genre_ids, is_movie])
                existing_ids.add(id)

def process_media(url, is_movie, csv_filename, existing_ids):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return 0

    data = response.json()
    total_pages = min(data['total_pages'], 500)  # Limit 500 pages
    total_results = 0 
    for page in range(1, total_pages + 1):
        response = requests.get(f'{url}&page={page}')
        if response.status_code != 200:
            print(f"Error fetching page {page}: {response.status_code} - {response.text}")
            continue

        page_data = response.json().get('results', [])
        write_or_append_to_csv(csv_filename, page_data, is_movie, existing_ids)
        total_results += len(page_data)
        time.sleep(5)  # Delay 

    return total_results  # Return the count items

# Function to iterate over months 
def iterate_and_process_dates(start_date, end_date, output_filename):
    current_date = start_date
    while current_date <= end_date:
        # Get the last day of the current month
        last_day_of_month = calendar.monthrange(current_date.year, current_date.month)[1]
        start_date_str = current_date.strftime('%Y-%m-%d')
        end_date_str = current_date.replace(day=last_day_of_month).strftime('%Y-%m-%d')

        url_tv_shows = f'{base_url}discover/tv?api_key={api_key}&first_air_date.gte={start_date_str}&first_air_date.lte={end_date_str}'
        url_movies = f'{base_url}discover/movie?api_key={api_key}&primary_release_date.gte={start_date_str}&primary_release_date.lte={end_date_str}'

        existing_ids = get_existing_ids(output_filename)

        tv_show_count = process_media(url_tv_shows, False, output_filename, existing_ids)
        movie_count = process_media(url_movies, True, output_filename, existing_ids)

        if movie_count != 0 or tv_show_count != 0:
            print(f"Month: {current_date.strftime('%Y-%m')}, Movies: {movie_count}, TV Shows: {tv_show_count}")

        # Increment the date to the first day of the next month
        if current_date.month == 12:
            current_date = datetime.date(current_date.year + 1, 1, 1)
        else:
            current_date = datetime.date(current_date.year, current_date.month + 1, 1)
        time.sleep(1)  # Delay 

# Output 
output_filename = 'media_list.csv'

# Get IDs from the CSV
existing_ids = get_existing_ids(output_filename)

#start and end dates 
#start_date = datetime.date(1874, 12, 8) # first date
start_date = datetime.date(2024, 1, 8)
end_date = datetime.date.today()  # today

# Start 
iterate_and_process_dates(start_date, end_date, output_filename)