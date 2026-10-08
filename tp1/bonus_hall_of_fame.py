# -*- coding: utf-8 -*-                                   # Encodage du fichier source
"""TP1 - Bonus : Jeu 1 « Hall of fame » + Jeu 2 « Tournoi du Pendu »."""  # Docstring du module

import os                                                 # Pour construire le chemin de scores.txt

from partie_a_etudiants import convertir_note             # Réutilise la conversion float robuste de la partie A
from partie_c_mots import charger_mots, choisir_mot       # Réutilise le chargement et le choix de mot (partie C)
from partie_d_pendu import jouer_pendu, mot_secret_2_joueurs  # Réutilise le pendu et le mode 2 joueurs (partie D)

DOSSIER = os.path.dirname(os.path.abspath(__file__))      # Dossier du script
FICHIER_SCORES = os.path.join(DOSSIER, "scores.txt")      # scores.txt à côté du script


def charger_scores(chemin=FICHIER_SCORES):                # Relit le hall of fame au lancement
    """Renvoie {nom: victoires}. Fichier absent -> départ à zéro (dict vide)."""  # Docstring
    scores = {}                                           # Dictionnaire résultat
    try:                                                  # La lecture peut échouer
        with open(chemin, "r", encoding="utf-8") as f:    # Ouverture en lecture
            for ligne in f:                               # Parcourt chaque ligne
                ligne = ligne.strip()                     # Nettoie la ligne
                if ":" not in ligne:                      # Ligne vide ou mal formée
                    continue                              # On l'ignore
                nom, valeur = ligne.rsplit(":", 1)        # Sépare nom et nombre de victoires
                victoires = convertir_note(valeur)        # Conversion float sûre
                if nom.strip() and victoires is not None:  # Nom non vide et nombre valide
                    scores[nom.strip()] = victoires       # On garde l'entrée
    except FileNotFoundError:                             # Pas encore de fichier
        pass                                              # Départ à zéro : dictionnaire vide
    except (OSError, UnicodeDecodeError) as e:            # Autre problème de lecture
        print(f"Lecture de {chemin} impossible ({e}) : départ à zéro.")  # Message clair
    return scores                                         # Renvoie les scores


def sauvegarder_scores(scores, chemin=FICHIER_SCORES):    # Réécrit scores.txt à la fin
    """Écrit 'nom:victoires' par ligne (ex : Ana:2.0)."""  # Docstring
    try:                                                  # L'écriture peut échouer
        with open(chemin, "w", encoding="utf-8") as f:    # Ouverture en écriture
            for nom, victoires in sorted(scores.items(), key=lambda x: -x[1]):  # Trie du meilleur au moins bon
                f.write(f"{nom}:{float(victoires)}\n")    # Format "Ana:2.0"
    except OSError as e:                                  # Erreur d'écriture
        print(f"Impossible d'écrire {chemin} : {e}")      # Message clair


def afficher_hall_of_fame(scores):                        # Affiche le classement
    """Affiche les joueurs triés par victoires."""         # Docstring
    print("\n--- Hall of fame ---")                       # Titre
    if not scores:                                        # Aucun score
        print("(vide)")                                   # Indique que c'est vide
    for nom, v in sorted(scores.items(), key=lambda x: -x[1]):  # Du meilleur au moins bon
        print(f"{nom:<15} {v}")                           # Nom aligné à gauche sur 15 caractères, puis score


def main():                                               # Programme principal
    """Boucle de parties avec « Rejouer ? (o/n) » et scores persistants."""  # Docstring
    scores = charger_scores()                             # Relit scores.txt au lancement
    afficher_hall_of_fame(scores)                         # Montre le classement actuel
    nom = input("\nVotre nom : ").strip() or "Anonyme"    # Nom du joueur (Anonyme si vide)
    nom = nom.replace(":", "")                            # Retire ":" pour ne pas casser le format du fichier
    print(f"{nom}, vous repartez de {scores.get(nom, 0.0)} victoire(s).")  # Ex : « Ana repart de 2.0 »
    mots = charger_mots()                                 # Charge la liste de mots une seule fois
    while True:                                           # Boucle des parties
        tournoi = input("Mot choisi par votre voisin (tournoi) ? (o/n) ").strip().lower()  # Jeu 2 : tournoi
        if tournoi in ("o", "oui"):                       # Le voisin choisit le mot
            mot = mot_secret_2_joueurs()                  # Saisie cachée du mot par le voisin
        else:                                             # Sinon mot aléatoire
            mot = choisir_mot(mots)                       # Mot tiré dans mots.txt
        if jouer_pendu(mot):                              # Partie jouée ; True si gagnée
            scores[nom] = scores.get(nom, 0.0) + 1        # Ajoute une victoire au joueur
            sauvegarder_scores(scores)                    # Sauvegarde aussitôt (rien de perdu si crash)
        if input("Rejouer ? (o/n) ").strip().lower() not in ("o", "oui"):  # Demande après chaque partie
            break                                         # Sortie si non
    sauvegarder_scores(scores)                            # Réécrit scores.txt à la fin
    afficher_hall_of_fame(scores)                         # Affiche le classement final


if __name__ == "__main__":                                # Exécuté seulement si on lance ce fichier
    try:                                                  # Protège contre Ctrl+C
        main()                                            # Lance le jeu
    except (KeyboardInterrupt, EOFError):                 # Interruption
        print("\nPartie interrompue.")                    # Sortie propre
