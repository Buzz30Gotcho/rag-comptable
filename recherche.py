from lire_pdf import charger_morceaux
from vecteur import vectoriser, similarite

# 1. Charger les morceaux et calculer le vecteur de chacun
morceaux = charger_morceaux()
for m in morceaux:
    m["vecteur"] = vectoriser(m["contenu"])          # trou 1 : quel texte vectoriser ?

# 2. Vectoriser la question
question = "Combien ai-je payé à Bureau Plus ?"
vecteur_question = vectoriser(question)

# 3. Calculer le score de chaque morceau par rapport à la question
for m in morceaux:
    m["score"] = similarite(vecteur_question, m["vecteur"])    # trous 2 et 3 : quels vecteurs comparer ?

# 4. Trier du meilleur au moins bon, et afficher les 3 premiers
morceaux_tries = sorted(morceaux, key=lambda m: m["score"], reverse=True)
print(f"Question : {question}\n")
for m in morceaux_tries[:3]:
    print(f"{m['score']:.3f} | {m['fichier']} (page {m['page']})")
    print(m["contenu"])
    print("-" * 40)