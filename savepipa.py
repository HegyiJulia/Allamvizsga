import os
import requests
from bs4 import BeautifulSoup

# A weboldal URL-je
BASE_URL = 'https://sapientia.ro/hu/az-egyetemrol/dokumentumok_/szenatusi-hatarozatok_'
DOWNLOAD_FOLDER = 'downloaded_files'
PDF_FOLDER = os.path.join(DOWNLOAD_FOLDER, 'pdf_files')
DOC_FOLDER = os.path.join(DOWNLOAD_FOLDER, 'doc_files')
ZIP_FOLDER = os.path.join(DOWNLOAD_FOLDER, 'zip_files')
RAR_FOLDER = os.path.join(DOWNLOAD_FOLDER, 'rar_files')  # RAR mappa létrehozása

# Mappák létrehozása a letöltött fájlok számára
os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(DOC_FOLDER, exist_ok=True)
os.makedirs(ZIP_FOLDER, exist_ok=True)
os.makedirs(RAR_FOLDER, exist_ok=True)  # RAR mappa létrehozása

def download_file(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Hibák kezelése

        # Ellenőrizzük a válasz tartalmát
        if 'text/html' in response.headers.get('Content-Type', ''):
            print(f"Hiba: HTML tartalom észlelve a következő URL-en: {url}")
            return False

        # Fájl kiterjesztésének ellenőrzése
        file_extension = url.split('.')[-1].lower()
        
        # Fájl elhelyezése a megfelelő mappába
        if file_extension == 'pdf':
            filename = os.path.join(PDF_FOLDER, url.split('/')[-1])
        elif file_extension in ['doc', 'docx']:
            filename = os.path.join(DOC_FOLDER, url.split('/')[-1])
        elif file_extension == 'zip':  # ZIP fájlok kezelése
            filename = os.path.join(ZIP_FOLDER, url.split('/')[-1].lower())  # Kisbetűs mentés
        elif file_extension in ['rar', 'RAR']:  # RAR fájlok kezelése
            filename = os.path.join(RAR_FOLDER, url.split('/')[-1])
        else:
            print(f"Támogatott fájltípus: {file_extension} - letöltés nem történik.")
            return False
        
        # Fájl mentése
        with open(filename, 'wb') as f:
            f.write(response.content)
        #print(f"A fájl sikeresen letöltve: {filename}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Hiba történt a letöltés során: {e}")
        return False

def fetch_file_links():
    try:
        # Weboldal letöltése
        response = requests.get(BASE_URL)
        response.raise_for_status()  # Hibák kezelése

        # HTML elemzés
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Linkek keresése
        file_links = []
        for link in soup.select('div.news-descr a'):
            file_links.append(link['href'])

        return file_links

    except requests.exceptions.RequestException as e:
        print(f"Hiba történt az oldal letöltésekor: {e}")
        return []

def main():
    # Fájlok linkjeinek lekérése
    file_links = fetch_file_links()

    # Fájlok letöltése
    for relative_url in file_links:
        # Ellenőrizzük, hogy a relative_url abszolút URL-e
        if relative_url.startswith('http://') or relative_url.startswith('https://'):
            full_url = relative_url  # Használjuk az abszolút URL-t
        else:
            full_url = f'https://sapientia.ro/{relative_url.lstrip("/")}'
        
        download_file(full_url)

if __name__ == "__main__":
    main()
