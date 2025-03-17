import os
import requests
#from urllib.parse import urljoin
from bs4 import BeautifulSoup
from app.config import PDF_DIRECTORY

BASE_URL = "https://sapientia.ro/hu/az-egyetemrol/dokumentumok_/szenatusi-hatarozatok_"

def fetch_file_links():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    return [link['href'] for link in soup.select('div.news-descr a')]
    #return [urljoin(BASE_URL, link['href']) for link in soup.select('div.news-descr a')]

def download_files():
    file_links = fetch_file_links()
    downloaded = []
    for link in file_links:
        file_name = os.path.join(PDF_DIRECTORY, os.path.basename(link))
        response = requests.get(link)
        with open(file_name, 'wb') as f:
            f.write(response.content)
        downloaded.append(file_name)
    return downloaded
