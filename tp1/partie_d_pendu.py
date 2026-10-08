# -*- coding: utf-8 -*-                                   # Encodage du fichier source
"""TP1 - Partie D : jeu du Pendu (7 erreurs max, ASCII art, mode 2 joueurs)."""  # Docstring du module

import getpass                                            # Saisie cachée du mot en mode 2 joueurs
import unicodedata                                        # Pour retirer les accents (É -> E)

from partie_c_mots import charger_mots, choisir_mot, masque  # Réutilise les fonctions de la partie C

ERREURS_MAX = 7                                           # Nombre d'erreurs autorisées avant de perdre

DESSINS = [                                               # ASCII art (bonus) : un dessin par nombre d'erreurs (0 à 7)
    "\n\n\n\n\n=========",                                # 0 erreur : juste le sol
    "\n  |\n  |\n  |\n  |\n=========",                    # 1 erreur : le poteau
    "  +---+\n  |\n  |\n  |\n  |\n=========",             # 2 erreurs : la potence
    "  +---+\n  |   |\n  |   O\n  |\n  |\n=========",     # 3 erreurs : la corde et la tête
    "  +---+\n  |   |\n  |   O\n  |   |\n  |\n=========",   # 4 erreurs : le corps
    "  +---+\n  |   |\n  |   O\n  |  /|\n  |\n=========",  # 5 erreurs : un bras
    "  +---+\n  |   |\n  |   O\n  |  /|\\\n  |\n=========",  # 6 erreurs : deux bras
    "  +---+\n  |   |\n  |   O\n  |  /|\\\n  |  / \\\n=========",  # 7 erreurs : pendu complet
]                                                         # Fin de la liste des dessins


def sans_accent(texte):                                   # Retire les accents et met en majuscules
    """'Éléphant' -> 'ELEPHANT' (sert à comparer les lettres)."""  # Docstring
    decompose = unicodedata.normalize("NFD", texte)       # Sépare lettre et accent (É -> E + ´)
    return "".join(c for c in decompose if unicodedata.category(c) != "Mn").upper()  # Supprime les accents (catégorie Mn)


def demander_lettre(deja_proposees):                      # Demande une lettre valide au joueur
    """Renvoie une lettre (majuscule, sans accent) jamais proposée."""  # Docstring
    while True:                                           # Redemande jusqu'à une saisie valide
        saisie = sans_accent(input("Votre lettre : ").strip())  # Lit, nettoie, retire l'accent, majuscule
        if len(saisie) != 1 or not saisie.isalpha():      # Pas exactement une lettre ?
            print("Entrez UNE seule lettre.")             # Message d'erreur
        elif saisie in deja_proposees:                    # Lettre déjà jouée ?
            print(f"Lettre {saisie} déjà proposée (pas d'erreur en plus).")  # Pas de pénalité
        else:                                             # Saisie correcte et nouvelle
            return saisie                                 # On la renvoie


def jouer_pendu(mot):                                     # Une partie de pendu sur le mot donné
    """Joue une partie avec `mot`. Renvoie True si gagné, False sinon."""  # Docstring
    mot = mot.strip().upper()                             # Mot en majuscules (ex : "Python" -> "PYTHON")
    mot_compare = sans_accent(mot)                        # Version sans accent pour comparer (ÉLÉPHANT -> ELEPHANT)
    cache = masque(mot)                                   # Masque initial : ['_', '_', ...]
    for i, c in enumerate(mot):                           # Parcourt chaque caractère du mot
        if not c.isalpha():                               # Caractère non-lettre (tiret, espace, apostrophe)
            cache[i] = c                                  # On l'affiche directement, il n'est pas à deviner
    erreurs = 0                                           # Compteur d'erreurs
    proposees = []                                        # Lettres déjà proposées (dans l'ordre)
    while "_" in cache and erreurs < ERREURS_MAX:         # Tant qu'il reste des lettres et des vies
        print("\n" + DESSINS[erreurs])                    # Affiche le pendu correspondant aux erreurs
        print("Mot :", " ".join(cache))                   # Affiche le mot masqué : _ Y _ _ O _
        print(f"Erreurs : {erreurs}/{ERREURS_MAX}")       # Affiche le nombre d'erreurs
        print("Lettres proposées :", " ".join(proposees) or "aucune")  # Affiche les lettres déjà jouées
        lettre = demander_lettre(proposees)               # Demande une nouvelle lettre valide
        proposees.append(lettre)                          # Mémorise la lettre
        if lettre in mot_compare:                         # Lettre présente dans le mot ?
            for i, c in enumerate(mot_compare):           # Parcourt chaque position
                if c == lettre:                           # Même lettre à cette position
                    cache[i] = mot[i]                     # Révèle la lettre d'origine (avec accent)
            print("Bien joué !")                          # Retour positif
        else:                                             # Lettre absente
            erreurs += 1                                  # Une erreur de plus
            print(f"La lettre {lettre} n'est pas dans le mot.")  # Retour négatif
    if "_" not in cache:                                  # Plus aucun _ : tout est trouvé
        print("\nMot :", " ".join(cache))                 # Affiche le mot complet
        print("Gagné")                                    # Victoire
        return True                                       # Partie gagnée
    print("\n" + DESSINS[ERREURS_MAX])                    # Affiche le pendu complet
    print(f"Perdu, le mot était {mot}")                   # Défaite avec le mot
    return False                                          # Partie perdue


def mot_secret_2_joueurs():                               # Bonus : mode 2 joueurs
    """Le joueur 1 tape un mot caché ; renvoie ce mot."""  # Docstring
    while True:                                           # Redemande tant que le mot est invalide
        try:                                              # getpass peut ne pas marcher selon le terminal
            mot = getpass.getpass("Joueur 1, entrez le mot secret (caché) : ")  # Saisie invisible
        except Exception:                                 # Terminal incompatible (certains IDE)
            mot = input("Joueur 1, entrez le mot secret : ")  # Saisie visible en secours
            print("\n" * 50)                              # Fait défiler l'écran pour cacher le mot
        mot = mot.strip()                                 # Nettoie les espaces
        if mot and any(c.isalpha() for c in mot):         # Au moins une lettre ?
            return mot                                    # Mot valide
        print("Le mot doit contenir au moins une lettre.")  # Sinon on redemande


def main():                                               # Programme principal
    """Menu : 1 joueur (mot aléatoire) ou 2 joueurs."""   # Docstring
    print("=== Jeu du Pendu ===")                         # Titre
    mode = input("Mode 1 joueur ou 2 joueurs ? (1/2) ").strip()  # Choix du mode
    if mode == "2":                                       # Mode 2 joueurs
        mot = mot_secret_2_joueurs()                      # Le joueur 1 choisit le mot
    else:                                                 # Mode 1 joueur (par défaut)
        mot = choisir_mot(charger_mots())                 # Mot aléatoire depuis mots.txt
    jouer_pendu(mot)                                      # Lance la partie


if __name__ == "__main__":                                # Exécuté seulement si on lance ce fichier
    try:                                                  # Protège contre Ctrl+C
        main()                                            # Lance le jeu
    except (KeyboardInterrupt, EOFError):                 # Interruption de l'utilisateur
        print("\nPartie interrompue.")                    # Sortie propre
