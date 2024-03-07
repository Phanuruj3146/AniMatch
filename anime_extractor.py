import csv

def extract_anime_titles(csv_file_path):
    anime_titles = []

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)

        for row in csv_reader:
            title = row[2]  # 3rd entry of anime titles in csv data chunk
            anime_titles.append(title)

    return anime_titles

def extract_anime_url(csv_file_path):
    anime_urls = []

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)

        for row in csv_reader:
            url = row[1]  # 3rd entry of anime titles in csv data chunk
            anime_urls.append(url)

    return anime_urls
    