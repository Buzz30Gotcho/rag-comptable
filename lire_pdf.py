from pathlib import Path
from pypdf import PdfReader
from decoupage import decouper

tous_les_morceaux=[]

# Boucle 1 : pour chaque fichier PDF du dossier data
for fichier in Path("data").glob("*.pdf"):
    print(f"===== {fichier.name} =====")
    pdf_reader = PdfReader(fichier)  # on ouvre CE fichier

    # Boucle 2 : pour chaque page de ce fichier
    for numero, page in enumerate(pdf_reader.pages, start=1):
        texte = page.extract_text()
        morceaux=decouper(texte, 200, 30)# on découpe le texte de la page en morceaux
        for morceau in morceaux:
            tous_les_morceaux.append({"fichier":fichier.name, 
                                      "page":numero, 
                                      "contenu":morceau})
            
print(f"Nombre total de morceaux : {len(tous_les_morceaux)}")
for m in tous_les_morceaux:
    print(m)
        