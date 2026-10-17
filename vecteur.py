import ollama
import math

def similarite(v1, v2):
    produit = sum(a * b for a, b in zip(v1, v2))
    norme1 = math.sqrt(sum(a * a for a in v1))
    norme2 = math.sqrt(sum(b * b for b in v2))
    return produit / (norme1 * norme2)


def vectoriser(texte, modele="bge-m3"):
    reponse = ollama.embed(model=modele, input=texte)
    return reponse["embeddings"][0]


if __name__ == "__main__":
    question = vectoriser("Combien dois-je payer ?")
    phrases = [
        "Total TTC : 293.40 EUR",
        "Montant de la facture à régler",
        "Les frais de repas sont remboursés jusqu'à 25 EUR",
        "Recette de la tarte aux pommes",
    ]
    for phrase in phrases:
        score = similarite(question, vectoriser(phrase))
        print(f"{score:.3f}  {phrase}")
        
        
        