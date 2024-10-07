import pdfplumber
import re
import os
from database import create_connection
from datetime import datetime

# PDF szövegének kinyerése
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        all_text = ""
        for page in pdf.pages:
            all_text += page.extract_text()
        return all_text

# Hónapok helyettesítése számokkal
def replace_month_with_number(date_str):
    month_map = {
        'január': '01',
        'február': '02',
        'március': '03',
        'április': '04',
        'május': '05',
        'június': '06',
        'július': '07',
        'augusztus': '08',
        'szeptember': '09',
        'október': '10',
        'november': '11',
        'december': '12'
    }

    for month_name, month_number in month_map.items():
        date_str = date_str.replace(month_name, month_number)

    return date_str

# Dátum konvertálása
def convert_date_format(date_str):
    try:
        # A hónapok helyettesítése számokkal
        date_str = replace_month_with_number(date_str.strip())
        # Dátum konvertálása ISO formátumra
        date_obj = datetime.strptime(date_str, '%Y. %m %d.')  # Az új formátum '%Y. %m %d.'
        return date_obj.strftime('%Y-%m-%d')  # ISO formátumra alakítjuk
    except ValueError as e:
        print(f"Dátum konvertálás hiba: {e}")
        return None  # Visszatérünk None értékkel, ha hiba történt

# Meeting adatok kinyerése a PDF-ből
def extract_meeting_data(text):
    session_number_pattern = r"A Szenátus (\w+)\. ülésének határozatai"
    session_number_match = re.search(session_number_pattern, text)

    session_number = session_number_match.group(1) if session_number_match else None

    # Frissített dátum kinyerés
    date_pattern = r"(\d{4}\. \w+ \d{1,2}\.)"
    date_match = re.search(date_pattern, text)

    date = date_match.group(1) if date_match else None

    if date:
        # A dátum konvertálása
        date = convert_date_format(date)

    president_pattern = r"Dr\. ([\w\s]+) egyetemi tanár"
    secretary_pattern = r"Hauer Melinda"

    president_match = re.search(president_pattern, text)
    secretary_match = re.search(secretary_pattern, text)

    president = president_match.group(1) if president_match else "Unknown"
    secretary = "Hauer Melinda"  # Mert ezt mindig megadod a példában

    return {
        "session_number": session_number,
        "date": date,
        "president": president,
        "secretary": secretary
    }

# Meeting beszúrása az adatbázisba
def insert_meeting(connection, meeting_data):
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO meetings (session_number, date, president, secretary)
    VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(insert_query, (
            meeting_data['session_number'],
            meeting_data['date'],
            meeting_data['president'],
            meeting_data['secretary']
        ))
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Hiba a meeting beszúrása során:", e)
        return None

# Határozatok kinyerése
def extract_resolutions(text):
    pattern = r"(\d+)\. határozat\n(.*?)(?=\d+\. határozat|\Z)"
    matches = re.findall(pattern, text, re.DOTALL)
    resolutions = []

    for match in matches:
        resolution_number = match[0]
        content = match[1].replace('\n', ' ').strip()

        # Melléklet számának kinyerése
        appendix_pattern = r"\((\d+(?:\.\s?[a-z]?)?)\. melléklet\)"
        appendix_match = re.search(appendix_pattern, content)
        appendix = appendix_match.group(1) if appendix_match else None

        resolutions.append({
            "resolution_number": resolution_number,
            "content": content,
            "appendix": appendix  # Melléklet számának hozzáadása
        })
    return resolutions

# Határozatok beszúrása az adatbázisba
def insert_resolution(connection, resolution, meeting_id):
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO resolutions (meeting_id, resolution_number, content,appendix)
    VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(insert_query, (
            meeting_id,
            resolution['resolution_number'],
            resolution['content'],
            resolution['appendix']
        ))
        connection.commit()
    except Exception as e:
        print("Hiba a határozat beszúrása során:", e)

# Fő feldolgozó funkció a PDF-hez
def process_pdf_to_database(pdf_file):
    connection = create_connection()
    
    if connection:
        pdf_text = extract_text_from_pdf(pdf_file)
        meeting_data = extract_meeting_data(pdf_text)

        if meeting_data['date'] is None:  # Ellenőrzés, hogy a dátum érvényes-e
            print("A kinyert meeting adatok között a dátum NULL értékkel rendelkezik.")
            return

        meeting_id = insert_meeting(connection, meeting_data)
        
        if meeting_id is None:  # Ellenőrzés, hogy a meeting beszúrása sikeres volt-e
            print("A meeting beszúrása nem volt sikeres.")
            return

        resolutions = extract_resolutions(pdf_text)

        for resolution in resolutions:
            insert_resolution(connection, resolution, meeting_id)

        connection.close()

# PDF feldolgozása és adatbázisba illesztése
pdf_file = os.path.join("downloaded_files", "pdf_files", "hatarozatok 190.pdf")
process_pdf_to_database(pdf_file)

# Debug: Ellenőrizd a kinyert szöveget és a meeting adatokat
pdf_text = extract_text_from_pdf(pdf_file)
print("Kinyert szöveg:\n", pdf_text)  
meeting_data = extract_meeting_data(pdf_text)
print("Kinyert meeting adatok:", meeting_data)  
