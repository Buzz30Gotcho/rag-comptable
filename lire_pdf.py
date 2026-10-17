from pathlib import Path
from pypdf import PdfReader

# Boucle 1 : pour chaque fichier PDF du dossier data
for fichier in Path("data").glob("*.pdf"):
    print(f"===== {fichier.name} =====")
    pdf_reader = PdfReader(fichier)  # on ouvre CE fichier

    # Boucle 2 : pour chaque page de ce fichier
    for numero, page in enumerate(pdf_reader.pages, start=1):
        texte = page.extract_text()
        print(f"Page {numero} :")
        print(texte)