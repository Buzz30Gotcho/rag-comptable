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
    

import ollama

# 5. Construire le contexte à partir des 3 meilleurs morceaux
contexte = ""
for m in morceaux_tries[:3]:
    contexte += f"[Source : {m['fichier']}, page {m['page']}]\n{m['contenu']}\n\n"

# 6. Construire le prompt
prompt = f"""Tu es un assistant comptable. Réponds à la question en te basant UNIQUEMENT sur les extraits ci-dessous.
Cite les sources utilisées (nom du fichier).
Si les extraits ne permettent pas de répondre, dis-le clairement.

Extraits :
{contexte}
Question : {question}"""

# 7. Envoyer le prompt à llama3
reponse = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}],options={"num_thread": 4})
print("\n===== RÉPONSE =====")
print(reponse["message"]["content"])