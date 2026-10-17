from pathlib import Path
from pypdf import PdfReader
from decoupage import decouper


def charger_morceaux():
    tous_les_morceaux = []
    for fichier in Path("data").glob("*.pdf"):
        pdf_reader = PdfReader(fichier)
        for numero, page in enumerate(pdf_reader.pages, start=1):
            texte = page.extract_text()
            morceaux = decouper(texte, 1000, 150)
            for morceau in morceaux:
                tous_les_morceaux.append({
                    "fichier": fichier.name,
                    "page": numero,
                    "contenu": morceau,
                })
    return tous_les_morceaux


if __name__ == "__main__":
    morceaux = charger_morceaux()
    print(f"Nombre total de morceaux : {len(morceaux)}")