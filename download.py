#!/usr/bin/env python3

import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import pickle as pkl
import urllib
import urllib.request

base_url = 'http://pt.jikos.cz/garfield/'
year_start = 1978
year_end = 2021

month_start = 1
month_end = 12

URL_ARCHIVE_FILE = "urls.pkl"
DATA_DIR = 'images'
BAD_URLS = 'bad_urls.txt'

def get_urls(url):
    try:
        soup = bs(requests.get(url).content, "html.parser")
        urls = []
        for img in soup.find_all("img"):
            img_url = img.attrs.get("src")
            if not img_url:
                continue
            img_url = urljoin(url, img_url)
            if not ('valid-xhtml10.gif' in img_url):
                if not ('valid-css.gif' in img_url):
                    if not ('vim.gif' in img_url):
                        urls.append(img_url)
        return urls 
    except Exception as e:
        print(f"Exception on {url}: {e}")
        return None

if not os.path.exists(URL_ARCHIVE_FILE):
    urls = {}
    for year in tqdm(range(year_start, year_end+1)):
        urls[year] = {}
        for month in tqdm(range(month_start, month_end+1), leave=False):
            #print(f"Year: {year}, month: {month}")
            retn_urls = get_urls(f'http://pt.jikos.cz/garfield/{year}/{month}/')
            urls[year][month] = retn_urls

    with open(URL_ARCHIVE_FILE, 'wb') as url_file:
        pkl.dump(urls, url_file, protocol=0)

if not os.path.isdir(f'{DATA_DIR}'):
    os.mkdir(f'{DATA_DIR}')

if not os.path.exists(f'{BAD_URLS}'):
    with open(f'{BAD_URLS}', 'w') as f:
        f.write('')

with open(f'{BAD_URLS}', 'r') as f:
    known_bad_urls = f.read().split(',')[-1]

with open(URL_ARCHIVE_FILE, 'rb') as url_file:
    all_urls = pkl.load(url_file)
    for year in tqdm(range(year_start, year_end+1)):
        if not os.path.isdir(f'{DATA_DIR}/{year}'):
            os.mkdir(f'{DATA_DIR}/{year}')
        for month in tqdm(range(month_start, month_end+1), leave=False):
            if not os.path.isdir(f'{DATA_DIR}/{year}/{month}'):
                os.mkdir(f'{DATA_DIR}/{year}/{month}')
            yearmonth_urls = all_urls[year][month]
            for url in tqdm(yearmonth_urls, leave=False):
                filename = f'{DATA_DIR}/{year}/{month}/' + str(url.split('/')[-1])
                if not os.path.exists(filename):
                    if not url in known_bad_urls:
                        req = requests.get(url)
                        if req.status_code == 200: # URL OK
                            with open(filename, 'wb') as f:
                                f.write(req.content)
                        else:
                            print(f'Error on {req.url}: {req.status_code}')
                            with open(f'{BAD_URLS}', 'a') as f:
                                f.write(f'{url},')
