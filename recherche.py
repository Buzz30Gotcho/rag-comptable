import numpy as np
import psycopg
from pgvector.psycopg import register_vector

from vecteur import vectoriser

conn = psycopg.connect("postgresql://rag:rag@localhost:5432/rag")
register_vector(conn)

# 1. Vectoriser la question (c'est le seul calcul de vecteur à faire)
question = input("Ta question : ")
vecteur_question = np.array(vectoriser(question))

# 2. Demander à PostgreSQL les 3 morceaux les plus proches
lignes = conn.execute(
    """
    SELECT fichier, page, contenu, 1 - (vecteur <=> %s) AS score
    FROM morceaux
    ORDER BY vecteur <=> %s
    LIMIT 3
    """,
    (vecteur_question, vecteur_question),
).fetchall()
conn.close()

# 3. Remettre les résultats sous forme de dictionnaires, comme avant
morceaux_tries = [
    {"fichier": l[0], "page": l[1], "contenu": l[2], "score": l[3]} for l in lignes
]

print(f"Question : {question}\n")
for m in morceaux_tries:
    print(f"{m['score']:.3f} | {m['fichier']} (page {m['page']})")


# On garde seulement les morceaux à moins de 0,08 du meilleur score
meilleur_score = morceaux_tries[0]["score"]
morceaux_tries = [m for m in morceaux_tries if m["score"] >= meilleur_score - 0.08]
import ollama

# 5. Construire le contexte à partir des 3 meilleurs morceaux
contexte = ""
for m in morceaux_tries[:3]:
    contexte += f"[Source : {m['fichier']}, page {m['page']}]\n{m['contenu']}\n\n"

# 6. Construire le prompt
prompt = f"""Tu es un assistant comptable. Réponds à la question en te basant UNIQUEMENT sur les extraits ci-dessous.
Règles :
- Ignore les extraits qui n'ont pas de rapport avec la question.
- Commence par la réponse, en une ou deux phrases, puis donne le détail du calcul si besoin.
- Termine par la liste des fichiers sources utilisés.
- Si les extraits ne permettent vraiment pas de répondre, dis-le clairement.

Extraits :
{contexte}
Question : {question}"""

# 7. Envoyer le prompt à llama3
print("\n===== RÉPONSE =====")
for morceau in ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}], stream=True):
    print(morceau["message"]["content"], end="", flush=True)
print()