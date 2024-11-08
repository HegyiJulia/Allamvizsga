from elasticsearch import Elasticsearch
import re

# Kapcsolódás az Elasticsearch szerverhez HTTP-n keresztül
es = Elasticsearch("http://localhost:9200")

# Kapcsolat ellenőrzése
if es.ping():
    print("Kapcsolódás sikeres!")
else:
    print("Kapcsolódás sikertelen!")
    exit

# Index neve
index_name = "senatus_határozatok"

# Keresési kifejezés megadása
search_term = "tanulmányi ösztöndíj"
try:
    # Keresés match_phrase használatával
    response = es.search(
        index=index_name,
        query={
            "match_phrase": {
                "content": search_term
            }
        },
        highlight={
            "fields": {
                "content": {"pre_tags": ["<em>"], "post_tags": ["</em>"], "number_of_fragments": 0}  # Kiemelés HTML taggel
            }
        }
    )

    # Eredmények kiírása kiemelt szövegrésszel
    print("Keresési eredmények:")
    for hit in response["hits"]["hits"]:
        print(f"Fájl: {hit['_source']['filename']}")
        
        # Kiemelt részletek formázása
        if "highlight" in hit:
            for fragment in hit["highlight"]["content"]:
                # Eltávolítja a HTML formázási elemeket
                cleaned_fragment = re.sub(r"<\/?em>", "", fragment)
                # Keresett kifejezés előtti és utáni szavak megjelenítése
                context = re.findall(r'(\S+\s+)?\S*{}(?:\s+\S+)?'.format(re.escape(search_term)), cleaned_fragment)
                if context:
                    # A találat előtti és utáni szavak megjelenítése
                    before = cleaned_fragment.split(search_term)[0].strip().split()[-3:]  # Az utolsó 3 szó a keresett kifejezés előtt
                    after = cleaned_fragment.split(search_term)[1].strip().split()[:3]  # Az első 3 szó a keresett kifejezés után
                    print(f"Részlet: ...{' '.join(before)} <em>{search_term}</em> {' '.join(after)}...\n")
        else:
            print("Nincs kiemelt találat.")

except NotFoundError:
    print(f"A keresett '{index_name}' index nem található.")
except Exception as e:
    print(f"Hiba történt a keresés során: {e}")
