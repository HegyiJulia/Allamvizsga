# 📚 Projekt áttekintés – Szenátusi Határozat Kereső

A **Szenátusi Határozat Kereső** egy Elasticsearch-alapú intelligens keresőrendszer, amely a Sapientia Egyetem szenátusi ülésein elfogadott határozatok feldolgozását és elérését teszi lehetővé.  
A felhasználók – tanárok, adminisztratív munkatársak és diákok – egy webes felületen kereshetnek a határozatok között lexikális vagy szemantikus módszerekkel.  
A rendszer lehetőséget biztosít dokumentumok böngészésére is, és az Elasticsearch technológia révén a keresési műveletek rendkívül gyorsak és hatékonyak.

##  Főbb funkciók

###  Böngészés szenátusi ülések szerint
- A főoldalon megtekinthető az összes szenátusi ülés listája
- Egy adott ülés kiválasztásával annak részletes határozatai jelennek meg
- A határozatok PDF formátumban is letölthetők

### Lexikális keresés
- Kulcsszavas keresés és pontos kifejezések keresése a határozatok szövegében
- Szűrés dátum alapján
- A találatok listában jelennek meg, minden találatnál látható a dokumentumok címe és részletei

### Szemantikus keresés
- A keresett szöveghez hasonló jelentésű határozatokat jeleníti meg
- Minden találathoz tartozik egy hasonlósági százalékos érték, amely mutatja, mennyire egyezik a találat a keresett tartalommal

## 🛠 Technológiai háttér

### Backend
- **Nyelv**: Python
- **Keretrendszer**: FastAPI
- **Adatbázis**: Elasticsearch (két külön index: szenátusi ülések és határozatok)
- **Futtatás**: Docker konténerben
- PDF fájlok feldolgozása külön Python szkripttel történik, amely letölti és indexeli az adatokat
- Az indexelés közvetlenül az Elasticsearch-be történik API hívással

### Frontend
- **Technológia**: React + TypeScript
- A React-alkalmazás REST API-n keresztül kommunikál a backenddel
- Három fő oldal:
  - Böngészés szenátusi ülések között
  - Lexikális keresés
  - Szemantikus keresés

### Mesterséges intelligencia
- A szemantikus kereséshez a [SentenceTransformer](https://www.sbert.net/) `paraphrase-multilingual-MiniLM-L12-v2` modell kerül alkalmazásra
- A hasonlóság százalékosan kerül kiszámításra és megjelenítésre
- A modell Docker környezetben, lokálisan fut

### Infrastruktúra és adattárolás
- Az alkalmazás minden komponense (backend, frontend, szemantikus modell) külön Docker image-ben fut
- Az adatok az Elasticsearch-ben kerülnek tárolásra, illetve külön lokális fájlban is megjelennek

## Telepítés és futtatás – Szenátusi Határozat Kereső

Ez a rész segít a projekt lokális elindításában. A rendszer FastAPI backendből, React frontendből és Elasticsearchből áll, mindhárom Docker konténerben fut.

### 🔧 Előfeltételek

Telepíteni szükséges:
- Python 3.10.18
- Node.js (React 19.0.0 verzióval)
- Docker és Docker Compose
- Elasticsearch 8.11.1 (Docker konténerben fut)

---

### 🐳 Docker alapú indítás

A projekt minden komponense (backend, frontend, Elasticsearch) Docker konténerekben fut, így nincs szükség külön virtuális környezetre vagy lokális telepítésre.

---

### 🖥️ Backend futtatása (FastAPI)

- A backend Docker konténerből indul, elérhető a `http://localhost:8000` címen
- PDF-ek feldolgozása és indexelése egy API POST kérés segítségével történik:

```bash
curl -X POST http://localhost:8000/files/process_pdfs
```
## 📁 Projektstruktúra

```
Avizsga/
├── backend/
│ ├── app/
│ │ ├── models/
│ │ │ ├── search.py
│ │ │ └── semantic_search_documents.py
│ │ ├── routers/
│ │ │ ├── files.py
│ │ │ ├── search.py
│ │ │ └── semantic_search.py
│ │ ├── services/
│ │ │ ├── elastic_handler.py
│ │ │ ├── file_downloader.py
│ │ │ ├── pdf_processor.py
│ │ │ └── semantic_search.py
│ │ └── main.py
│ ├── .env
│ ├── .gitignore
│ ├── Dockerfile
│ └── requirements.txt
│
├── myfrontend/
│ ├── src/
│ │ ├── api/
│ │ │ ├── client.ts
│ │ │ ├── search.ts
│ │ │ └── semantic.ts
│ │ ├── components/
│ │ │ ├── TopNavBar.css
│ │ │ └── TopNavBar.tsx
│ │ ├── pages/
│ │ │ ├── Home.tsx
│ │ │ ├── Search.css
│ │ │ ├── Search.tsx
│ │ │ └── SemanticSearch.tsx
│ │ ├── App.css
│ │ ├── App.tsx
│ │ ├── index.css
│ │ └── main.tsx
│ ├── .env
│ ├── .gitignore
│ ├── index.html
│ ├── package.json
│ ├── package-lock.json
│ └── vite.config.ts
│
├── docker-compose.yml
└── README.md
```
