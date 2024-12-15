import re

# Charger le fichier
chemin_fichier = r"C:\Users\Utilisateur\Documents\Devoirs et Cours 5A\PTUT\rh-documents-txt\-rh-fiche-indemnite-urgences-juin-2020.txt"

def charger_fichier(chemin):
    with open(chemin, "r", encoding="utf-8") as fichier:
        return fichier.read()

# Fonction de nettoyage
def nettoyer_texte(texte):
    # Supprimer les numéros de page, en-têtes ou pieds de page (si vous en avez)
    texte = re.sub(r'\b(page \d+|\\page\\)\b', '', texte)

    # Supprimer les caractères spéciaux et non pertinents (tout sauf les lettres et les espaces)
    texte = re.sub(r'[^A-Za-zÀ-ÿ0-9\s,.;:!?(){}[\]]', '', texte)  # Garde les lettres, chiffres et certains symboles de ponctuation
    # Normaliser les espaces multiples en un seul espace
    texte = re.sub(r'\s+', ' ', texte).strip()
    
    return texte

# Charger et nettoyer le texte
texte_brut = charger_fichier(chemin_fichier)
texte_nettoye = nettoyer_texte(texte_brut)

# Sauvegarder le texte nettoyé dans un nouveau fichier dans le dossier cible
chemin_sortie = r"C:\Users\Utilisateur\Documents\Devoirs et Cours 5A\PTUT\Test PDF extract\texte_nettoye.txt"

def sauvegarder_texte(texte, chemin_sortie):
    with open(chemin_sortie, "w", encoding="utf-8") as fichier:
        fichier.write(texte)

# Sauvegarder le texte nettoyé dans le répertoire spécifié
sauvegarder_texte(texte_nettoye, chemin_sortie)

print(f"Fichier nettoyé sauvegardé à : {chemin_sortie}")
