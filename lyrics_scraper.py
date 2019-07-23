"""
This module scrapes the lyrics of Etta James and Billy Joel form lyrics.com and saves it as as .csv file
"""

import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

ETTA = 'Etta'
JAMES = 'James'
URL_ETTA = 'https://www.lyrics.com/artist.php?name=Etta-James&aid=387&o=1'
BILLY = 'Billy'
JOEL = 'Joel'
URL_BILLY = 'https://www.lyrics.com/artist.php?name=Billy-Joel&aid=4615&o=1'


def append_url(first_name, name, url_artist):
    """ Append the URLs into a single list, return the artist URL list """
    artist_linked = re.findall(f'href=\"(\/lyric\/\d+\/{first_name}\+{name}\/[^"]*)\"',
                               requests.get(url_artist).text)

    artist_list = []
    for i in artist_linked:
        url = ('https://www.lyrics.com' + i)
        artist_list.append(url)

    return artist_list


def get_lyrics(first_name, name, url_artist):
    """ Scrape lyrics of an artist, return a {first_name}_cleaned.csv file """
    artist_soup = []
    for j in append_url(first_name, name, url_artist):
        file = BeautifulSoup(requests.get(j).text, features='lxml').find_all(attrs={'id': 'lyric-body-text'})
        artist_soup.append(file)

    flat_list = []
    for sublist in artist_soup:
        for item in sublist:
            flat_list.append(item.text)

    return pd.DataFrame(flat_list).to_csv(f'{first_name}_cleaned.csv', sep='\t', index=False)

get_lyrics(ETTA, JAMES, URL_ETTA)
get_lyrics(BILLY, JOEL, URL_BILLY)