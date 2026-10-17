import numpy as np
import psycopg
from pgvector.psycopg import register_vector

from lire_pdf import charger_morceaux
from vecteur import vectoriser

# Connexion à la base (utilisateur:mot_de_passe@adresse:port/nom_de_la_base)
conn = psycopg.connect("postgresql://rag:rag@localhost:5432/rag")
register_vector(conn)

# On vide la table, pour ne pas créer de doublons si on relance le script
conn.execute("TRUNCATE morceaux")

morceaux = charger_morceaux()
for m in morceaux:
    vecteur = vectoriser(m["contenu"])
    conn.execute(
        "INSERT INTO morceaux (fichier, page, contenu, vecteur) VALUES (%s, %s, %s, %s)",
        (m["fichier"], m["page"], m["contenu"], np.array(vecteur)),
    )
    print(f"Indexé : {m['fichier']} (page {m['page']})")

conn.commit()
conn.close()
print(f"\n{len(morceaux)} morceaux enregistrés dans la base.")