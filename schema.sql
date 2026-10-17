-- Structure de la base de données du projet RAG comptable
-- À exécuter une seule fois, sur une base PostgreSQL avec l'extension pgvector

-- Active pgvector (ajoute le type "vector" à PostgreSQL)
CREATE EXTENSION IF NOT EXISTS vector;

-- Un morceau de document, avec son étiquette et son vecteur
CREATE TABLE IF NOT EXISTS morceaux (
    id SERIAL PRIMARY KEY,
    fichier TEXT NOT NULL, -- nom du PDF d'origine
    page INTEGER NOT NULL, -- numéro de page, pour citer la source
    contenu TEXT NOT NULL, -- texte du morceau
    vecteur vector (1024) NOT NULL -- vecteur calculé par bge-m3 (1024 dimensions)
);

-- Index pour accélérer la recherche des vecteurs les plus proches (similarité cosinus)
CREATE INDEX IF NOT EXISTS morceaux_vecteur_idx ON morceaux USING hnsw (vecteur vector_cosine_ops);