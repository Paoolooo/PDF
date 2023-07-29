import requests
import fitz
import re
import json

def extract_missions_principales_from_pdf(pdf_url):
    # Télécharger le contenu du fichier PDF à partir du lien
    response = requests.get(pdf_url)
    with open("temp.pdf", "wb") as file:
        file.write(response.content)

    # Extraire les missions principales
    missions_principales = "Aucune information trouvée"
    with fitz.open("temp.pdf") as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text()
            missions_start = re.search(r"Missions\s+principales", page_text, re.IGNORECASE)
            if missions_start:
                missions_start = missions_start.end()
                missions_end = page_text.find("PROFIL", missions_start)
                missions_principales = page_text[missions_start:missions_end].strip()
                break

    return missions_principales

# Lien vers le fichier PDF
pdf_url = "https://www.rouenhabitat.fr/wp-content/uploads/2022/09/OFFRE-EMPLOI-INGENIEUR-INFORMATIQUE.pdf"
missions_principales = extract_missions_principales_from_pdf(pdf_url)

# Créer un dictionnaire contenant les missions principales
data = {
    "Missions principales": missions_principales
}

# Créer un fichier JSON et y écrire les données
with open("missions_principales.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Missions principales :")
print(missions_principales)
