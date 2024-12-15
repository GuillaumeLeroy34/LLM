import re
import os

# Dossier de sortie et nom du fichier
dossier_sortie = "C:/Users/Utilisateur/Documents/Devoirs et Cours 5A/PTUT/Test PDF extract"
nom_fichier = "resultat_extraction_nettoye.txt"

# Vérification si le dossier de sortie existe, sinon le créer
if not os.path.exists(dossier_sortie):
    os.makedirs(dossier_sortie)

# Chemin complet du fichier TXT
chemin_fichier_sortie = os.path.join(dossier_sortie, nom_fichier)

def nettoyer_texte(texte):
    # Suppression des sauts de ligne inutiles
    texte = re.sub(r'\n+', ' ', texte)
    # Suppression des caractères multiples inutiles
    texte = re.sub(r'[\.\-]{2,}', '', texte)
    # Correction des espaces multiples
    texte = re.sub(r'\s{2,}', ' ', texte)
    # Reformater les titres en majuscules pour les rendre clairs
    texte = re.sub(r'(LE NOUVEAU STATUT DE PRATICIEN ASSOCIE|CONDITIONS STATUTAIRES)', r'\n\n\1\n', texte)
    # Ajout d'une numérotation propre pour les listes
    texte = re.sub(r'', '-', texte)  # Transformer les puces en tirets
    
    return texte.strip()

try:
    # Lecture du fichier source
    fichier_source = "C:/Users/Utilisateur/Documents/Devoirs et Cours 5A/PTUT/Test PDF extract/resultat_extractionv2.txt"
    print(f"Lecture du fichier source : {fichier_source}...")
    with open(fichier_source, "r", encoding="utf-8") as fichier:
        texte_brut = fichier.read()
    print("Fichier source lu avec succès.")

    # Nettoyage du texte
    print("Nettoyage du texte...")
    texte_nettoye = nettoyer_texte(texte_brut)

    # Écriture dans le fichier de sortie
    print(f"Écriture dans le fichier de sortie : {chemin_fichier_sortie}...")
    with open(chemin_fichier_sortie, "w", encoding="utf-8") as fichier_sortie:
        fichier_sortie.write(texte_nettoye)
    print(f"Texte nettoyé et sauvegardé dans '{chemin_fichier_sortie}'")

except FileNotFoundError as e:
    print(f"Erreur : Fichier source introuvable - {e}")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")
