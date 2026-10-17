# texte = le texte du PDF à découper
# taille = la taille maximale du morceau de texte a decouper (texte decoupe)
# chevauchement = le nombre de caractere pris du morceau de texte precedent sur le morceau de texte suivant
# taille - chevauchement : c’est le nombre de caractères nouveaux qu’apporte chaque morceau.
# | chevauchement | nouveaux caractères |
# |   3 repris    |      7 nouveaux     |   = 10 au total (la taille)



def decouper(texte, taille, chevauchement):
    morceaux = []
    debut = 0
    while debut < len(texte):
        fin = debut + taille

        # Si on n'est pas à la fin du texte, on recule jusqu'au dernier espace
        if fin < len(texte):
            espace = texte.rfind(" ", debut, fin)
            if espace != -1:
                fin = espace

        morceaux.append(texte[debut:fin])

        if fin >= len(texte):
            break
        debut = fin - chevauchement
        espace = texte.find(" ", debut)
        if espace != -1:
            debut = espace + 1

    return morceaux

if __name__ == "__main__":
    for m in decouper("Les frais de repas engagés lors d'un déplacement professionnel", 20, 5):
        print(m)