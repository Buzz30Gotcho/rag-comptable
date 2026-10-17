# texte = le texte du PDF à découper
# taille = la taille maximale du morceau de texte a decouper (texte decoupe)
# chevauchement = le nombre de caractere pris du morceau de texte precedent sur le morceau de texte suivant
# taille - chevauchement : c’est le nombre de caractères nouveaux qu’apporte chaque morceau.
# | chevauchement | nouveaux caractères |
# |   3 repris    |      7 nouveaux     |   = 10 au total (la taille)


from ast import main


def decouper(texte, taille, chevauchement):
    morceaux=[]
    for i in range(0,len(texte), taille-chevauchement):
        morceaux.append(texte[i:i+taille])
        if (i+taille >= len(texte)):
            break
    return morceaux

if __name__ == "__main__":
    resultat = decouper("Total TTC : 293.40 EUR", 10, 3)
    for morceau in resultat:
        print(repr(morceau))