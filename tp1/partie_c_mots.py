# -*- coding: utf-8 -*-                                   # Encodage du fichier source
"""TP1 - Partie C : manipulation des mots."""             # Docstring du module

import os                                                 # Pour construire le chemin du fichier mots.txt
import random                                             # Pour choisir un mot au hasard

DOSSIER = os.path.dirname(os.path.abspath(__file__))      # Dossier où se trouve ce script
FICHIER_MOTS = os.path.join(DOSSIER, "mots.txt")          # Chemin complet de mots.txt (marche d'où qu'on lance)
MOTS_PAR_DEFAUT = ["PYTHON", "RESEAU", "ROUTEUR", "SERVEUR"]  # Liste de secours si le fichier manque


def charger_mots(chemin=FICHIER_MOTS):                    # 1. Charge la liste de mots depuis un .txt
    """Renvoie la liste des mots du fichier (un par ligne), ou la liste par défaut."""  # Docstring
    try:                                                  # La lecture peut échouer
        with open(chemin, "r", encoding="utf-8") as f:    # Ouverture en lecture UTF-8 (accents)
            mots = [ligne.strip() for ligne in f if ligne.strip()]  # Garde les lignes non vides, nettoyées
    except (OSError, UnicodeDecodeError) as e:            # Fichier absent, illisible ou mal encodé
        print(f"Impossible de lire {chemin} ({e}) : liste par défaut.")  # Message clair
        return list(MOTS_PAR_DEFAUT)                      # Copie de la liste de secours
    return mots if mots else list(MOTS_PAR_DEFAUT)        # Fichier vide -> liste de secours


def choisir_mot(liste):                                   # 2. Choisit un mot et le renvoie en MAJUSCULES
    """Renvoie un mot aléatoire de `liste`, en majuscules."""  # Docstring
    if not liste:                                         # Liste vide : random.choice planterait
        liste = MOTS_PAR_DEFAUT                           # On utilise la liste de secours
    return random.choice(liste).strip().upper()           # Mot au hasard, sans espaces, en majuscules


def masque(mot):                                          # 3. Construit le masque du mot
    """Renvoie une liste de '_' de même longueur que `mot`."""  # Docstring
    return ["_"] * len(mot)                               # Liste répétant "_" autant de fois que de lettres


if __name__ == "__main__":                                # Exécuté seulement si on lance ce fichier
    mots = charger_mots()                                 # Charge les mots depuis mots.txt
    print("Mots chargés :", mots)                         # Affiche la liste
    mot = choisir_mot(mots)                               # Tire un mot au hasard
    print("Mot choisi :", mot)                            # Affiche le mot (en majuscules)
    print("Masque :", masque(mot))                        # Affiche son masque
    print('masque("PYTHON") ->', masque("PYTHON"))        # Jeu d'essai : ['_', '_', '_', '_', '_', '_']
