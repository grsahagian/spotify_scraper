from bs4 import BeautifulSoup
import pandas as pd
import requests
from time import sleep
from datetime import date, timedelta
import random
import bar_chart_race as bcr



url = "https://spotifycharts.com/regional/us/daily/"

COOKIE = ''


start_date = date(2021, 1, 1) # Year - Month - Day
end_date = date(2021, 11, 3)
delta = end_date - start_date

# Generates list of date strings from start_date to end_date
def date_list():
    dates = []
    for i in range(delta.days+1):
         day = start_date + timedelta(days=i)
         day_string = day.strftime("%Y-%m-%d")
         dates.append(day_string)
    return dates

dates = date_list()

# Generates list of urls for each date in date_list
def create_url_list():
    url_list = []
    for date in dates:
        url_string = url + date
        url_list.append(url_string)
    return url_list

urls = create_url_list()


def request_spotify():
    '''

    Scrapes top 200 songs from spotify from start_date to end_date
    and exports data as Excel.

    '''
    headers = {
        'authority': 'spotifycharts.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cookie': COOKIE
    }

    scraped_info = []

    for url in urls:
        print('Scraping ' + url + '...')
        response = requests.request("GET", url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', class_='chart-table')
        for x in table.find('tbody').find_all('tr'):
            track = x.find('td', class_='chart-table-track').strong.text
            artist = x.find('td', class_='chart-table-track').span.text
            track_and_artist = track + ' ' + artist
            artist = artist.replace("by ","").strip()
            streams = x.find('td', class_='chart-table-streams').text
            id = x.find('td', class_='chart-table-image').a.get('href')
            id = id.split("track/")[1]
            chart_date = url.split("daily/")[1]

            song_details = {
                            # 'track': track,
                            # 'artist': artist,
                            'track_and_artist': track_and_artist,
                            'streams': streams,
                            'id': id,
                            'chart_date': chart_date
                       }

            scraped_info.append(song_details)

        sleep(random.random()) # sleep 0 - 1 seconds after scraping each page

    scraped_info = pd.DataFrame(scraped_info)
    scraped_info.to_excel(f'spotify-streams-small-{start_date}-{end_date}.xlsx')

request_spotify()


#  Pivot data to prepare it to be processed by bar_chart_race
df = pd.read_excel('spotify-streams-2021-01-01-2021-11-03.xlsx', engine='openpyxl')
df['streams'] = df['streams'].str.replace(',','')
df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
df['track_and_artist'] = df['track_and_artist'].str.replace('$', '')
df = pd.pivot_table(df, values='streams', columns='track_and_artist', index='chart_date').cumsum()


# Create Bar Chart Race as HTML -- individual frames in folder /spotify_frames/*.png
bcr.bar_chart_race(df, title= 'Spotify Top Songs of 2021', filename='spotify.html',
                   steps_per_period=10,
                   n_bars=20,
                   filter_column_colors=True,
                   figsize=(7, 4)
                   )


