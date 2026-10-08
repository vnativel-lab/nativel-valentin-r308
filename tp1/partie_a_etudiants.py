# -*- coding: utf-8 -*-                                   # Encodage du fichier source (accents autorisés)
"""TP1 - Partie A : dictionnaire d'étudiants (nom -> note)."""  # Docstring : décrit le rôle du module

FICHIER_NOTES = "notes.txt"                               # Nom du fichier texte utilisé pour la sauvegarde


def convertir_note(valeur):                               # Fonction qui transforme une valeur en float de façon robuste
    """Convertit une valeur en float, renvoie None si impossible."""  # Docstring de la fonction
    try:                                                  # On tente la conversion (elle peut échouer)
        texte = str(valeur).strip().replace(",", ".")     # En texte, sans espaces, virgule française -> point
        note = float(texte)                               # Conversion en nombre à virgule
    except (ValueError, TypeError):                       # Si la valeur n'est pas un nombre ("abc", None...)
        return None                                       # On signale l'échec avec None au lieu de planter
    if note != note or note in (float("inf"), float("-inf")):  # Rejette NaN (NaN != NaN) et l'infini
        return None                                       # Ces valeurs ne sont pas des notes valides
    return note                                           # Conversion réussie : on renvoie la note


def ajouter_etudiant(d, nom, note):                       # Ajoute un étudiant ou met à jour sa note
    """Ajoute (ou met à jour) l'étudiant `nom` avec la note `note`."""  # Docstring
    nom = str(nom).strip()                                # Nettoie le nom (espaces en trop)
    valeur = convertir_note(note)                         # Convertit la note en float de manière sûre
    if not nom or valeur is None:                         # Nom vide ou note invalide ?
        print(f"Entrée ignorée : nom={nom!r}, note={note!r}")  # On prévient l'utilisateur
        return False                                      # On indique que l'ajout a échoué
    d[nom] = valeur                                       # Ajout ou remplacement dans le dictionnaire
    return True                                           # On indique que l'ajout a réussi


def moyenne_classe(d):                                    # Calcule la moyenne de toutes les notes
    """Renvoie la moyenne arrondie à 2 décimales, ou None si vide."""  # Docstring
    if not d:                                             # Dictionnaire vide : pas de division par zéro
        return None                                       # On renvoie None plutôt que de planter
    return round(sum(d.values()) / len(d), 2)             # Somme des notes / nombre d'étudiants, arrondi


def meilleur_etudiant(d):                                 # Cherche l'étudiant avec la meilleure note
    """Renvoie le tuple (nom, note) du meilleur, ou None si vide."""  # Docstring
    if not d:                                             # Dictionnaire vide : aucun meilleur
        return None                                       # On renvoie None
    nom = max(d, key=d.get)                               # Clé dont la valeur (note) est la plus grande
    return (nom, d[nom])                                  # Tuple (nom, note) comme demandé


def sauvegarder(d, chemin=FICHIER_NOTES):                 # Écrit le dictionnaire dans un fichier texte
    """Écrit une ligne 'nom:note' par étudiant. Renvoie True si OK."""  # Docstring
    try:                                                  # L'écriture disque peut échouer
        with open(chemin, "w", encoding="utf-8") as f:    # Ouverture en écriture (le fichier est écrasé)
            for nom, note in d.items():                   # Parcourt chaque paire nom/note
                f.write(f"{nom}:{note}\n")                # Écrit "nom:note" puis un retour à la ligne
        return True                                       # Écriture réussie
    except OSError as e:                                  # Erreur d'E/S (droits, disque plein, chemin invalide)
        print(f"Erreur d'écriture dans {chemin} : {e}")   # Message clair au lieu d'un plantage
        return False                                      # Échec signalé


def charger(chemin=FICHIER_NOTES):                        # Relit le fichier et reconstruit le dictionnaire
    """Lit le fichier 'nom:note'. Fichier absent ou lignes invalides : pas de plantage."""  # Docstring
    d = {}                                                # Dictionnaire résultat, vide au départ
    try:                                                  # La lecture peut échouer
        with open(chemin, "r", encoding="utf-8") as f:    # Ouverture en lecture
            for numero, ligne in enumerate(f, start=1):   # Parcourt les lignes avec leur numéro (à partir de 1)
                ligne = ligne.strip()                     # Retire espaces et retour à la ligne
                if not ligne:                             # Ligne vide ?
                    continue                              # On passe à la suivante
                if ":" not in ligne:                      # Pas de séparateur ":" -> ligne mal formée
                    print(f"Ligne {numero} ignorée (pas de ':') : {ligne!r}")  # Avertissement
                    continue                              # On ignore la ligne
                nom, note = ligne.rsplit(":", 1)          # Coupe au dernier ":" (le nom peut contenir ":")
                if not ajouter_etudiant(d, nom, note):    # Ajout avec conversion robuste
                    print(f"Ligne {numero} ignorée (mal formée).")  # Message si la note est invalide
    except FileNotFoundError:                             # Le fichier n'existe pas
        print(f"Fichier {chemin} absent : dictionnaire vide.")  # On part d'un dictionnaire vide
    except OSError as e:                                  # Autre erreur d'E/S (droits...)
        print(f"Erreur de lecture de {chemin} : {e}")     # Message clair
    except UnicodeDecodeError:                            # Fichier qui n'est pas du texte UTF-8
        print(f"Fichier {chemin} illisible (encodage).")  # Message clair
    return d                                              # Renvoie ce qui a pu être chargé


if __name__ == "__main__":                                # Ce bloc ne s'exécute que si on lance ce fichier directement
    etudiants = {}                                        # 1. Création du dictionnaire vide
    ajouter_etudiant(etudiants, "Alice", 12)              # Jeu d'essai : Alice 12
    ajouter_etudiant(etudiants, "Bob", 15)                # Jeu d'essai : Bob 15
    ajouter_etudiant(etudiants, "Claire", 9.5)            # Jeu d'essai : Claire 9.5
    print("Dictionnaire :", etudiants)                    # Affiche le contenu
    print("moyenne_classe(d)    ->", moyenne_classe(etudiants))     # Attendu : 12.17
    print("meilleur_etudiant(d) ->", meilleur_etudiant(etudiants))  # Attendu : ('Bob', 15.0)

    sauvegarder(etudiants)                                # 3. Sauvegarde dans notes.txt
    recharge = charger()                                  # Rechargement depuis le fichier
    print("Après rechargement :", recharge)               # Doit être identique
    print("Identique ?", recharge == etudiants)           # Vérification automatique

    print("\n--- Cas limites ---")                        # Titre des tests de robustesse
    print("Dictionnaire vide : moyenne =", moyenne_classe({}), "| meilleur =", meilleur_etudiant({}))  # Pas de plantage
    ajouter_etudiant(etudiants, "Dave", "abc")            # Note non numérique -> ignorée
    ajouter_etudiant(etudiants, "Eve", "13,5")            # Virgule française -> acceptée (13.5)
    print("Fichier absent :", charger("fichier_inexistant.txt"))  # Pas de plantage, dict vide
    with open("notes_test.txt", "w", encoding="utf-8") as f:  # Crée un fichier de test avec des lignes invalides
        f.write("Alice:12\nligne_sans_deux_points\nBob:quinze\n\nClaire:9.5\n")  # Lignes bonnes et mauvaises
    print("Lignes mal formées :", charger("notes_test.txt"))  # Seules les lignes valides sont gardées
