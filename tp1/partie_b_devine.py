# -*- coding: utf-8 -*-                                   # Encodage du fichier source
"""TP1 - Partie B : mini-jeu « Devine le nombre »."""     # Docstring du module

import random                                             # Module pour tirer un nombre au hasard


def demander_entier(message, mini=None, maxi=None):       # Demande un entier au joueur sans jamais planter
    """Redemande tant que la saisie n'est pas un entier dans [mini, maxi]."""  # Docstring
    while True:                                           # Boucle jusqu'à obtenir une saisie valide
        saisie = input(message).strip()                   # Lit la saisie et retire les espaces
        try:                                              # La conversion peut échouer
            valeur = int(saisie)                          # Conversion du texte en entier
        except ValueError:                                # Ce n'était pas un entier ("abc", "4.5", "")
            print("Entrez un nombre entier.")             # Message d'erreur
            continue                                      # On redemande
        if mini is not None and valeur < mini:            # Trop petit par rapport à la borne basse
            print(f"Le nombre doit être >= {mini}.")      # Message
            continue                                      # On redemande
        if maxi is not None and valeur > maxi:            # Trop grand par rapport à la borne haute
            print(f"Le nombre doit être <= {maxi}.")      # Message
            continue                                      # On redemande
        return valeur                                     # Saisie valide : on la renvoie


def jouer(borne_min=1, borne_max=100, essais_max=10):     # Une partie complète
    """Joue une partie. Renvoie True si gagné, False sinon."""  # Docstring
    secret = random.randint(borne_min, borne_max)         # Nombre secret entre les bornes (incluses)
    print(f"\nJ'ai choisi un nombre entre {borne_min} et {borne_max}. Vous avez {essais_max} essais.")  # Règles
    for essai in range(1, essais_max + 1):                # Boucle de 1 à essais_max
        proposition = demander_entier(f"Essai {essai}/{essais_max} : ", borne_min, borne_max)  # Saisie sûre
        if proposition < secret:                          # Proposition inférieure au secret
            print("Trop petit")                           # Indice
        elif proposition > secret:                        # Proposition supérieure au secret
            print("Trop grand")                           # Indice
        else:                                             # Sinon c'est égal
            print(f"Gagné ! en {essai} essai(s).")        # Victoire
            return True                                   # Fin de partie gagnée
    print(f"Perdu ! Le nombre était {secret}.")           # Plus d'essais : défaite
    return False                                          # Fin de partie perdue


def rejouer():                                            # Demande si le joueur veut recommencer
    """Renvoie True si le joueur répond o/oui."""         # Docstring
    reponse = input("Rejouer ? (o/n) ").strip().lower()   # Lit la réponse en minuscules
    return reponse in ("o", "oui")                        # True seulement pour o / oui


def main():                                               # Programme principal
    """Boucle de jeu avec bornes personnalisables (bonus)."""  # Docstring
    print("=== Devine le nombre ===")                     # Titre
    while True:                                           # Boucle de rejouabilité (bonus)
        perso = input("Bornes personnalisées ? (o/n) ").strip().lower()  # Bonus : choix des bornes
        if perso in ("o", "oui"):                         # Le joueur veut ses propres bornes
            bmin = demander_entier("Borne minimale : ")   # Saisie de la borne basse
            bmax = demander_entier("Borne maximale : ", mini=bmin + 1)  # Borne haute > borne basse
        else:                                             # Sinon bornes par défaut
            bmin, bmax = 1, 100                           # 1 à 100 comme dans l'énoncé
        jouer(bmin, bmax)                                 # Lance une partie
        if not rejouer():                                 # Le joueur ne veut pas rejouer ?
            print("Au revoir !")                          # Message de fin
            break                                         # Sortie de la boucle


if __name__ == "__main__":                                # Exécuté seulement si on lance ce fichier
    try:                                                  # Protège contre Ctrl+C / fin d'entrée
        main()                                            # Lance le jeu
    except (KeyboardInterrupt, EOFError):                 # L'utilisateur a interrompu
        print("\nPartie interrompue.")                    # Sortie propre sans trace d'erreur
