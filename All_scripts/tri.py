import os
import shutil

# Définir le chemin du répertoire contenant les fichiers à organiser
directory = 'C:/Users/Utilisateur/Documents/Devoirs et Cours 5A/PTUT/Sources RAG - Fine-tuning/santexpo2024-dev/pdf_all'

def organize_files(directory):
    # Définir des catégories pour organiser les fichiers : chaque catégorie est associée à un dossier
    categories = {'guide': 'C:/Users/Utilisateur/Documents/Devoirs et Cours 5A/PTUT/Tri/Guides/',
                  'fiche': 'C:/Users/Utilisateur/Documents/Devoirs et Cours 5A/PTUT/Tri/Fiches_RH/',
                  'faq': 'C:/Users/Utilisateur/Documents/Devoirs et Cours 5A/PTUT/Tri/FAQ/'}

    # Parcourir tous les fichiers dans le répertoire spécifié
    for filename in os.listdir(directory):
        # Vérifier si le fichier a l'extension .pdf
        if filename.endswith(".pdf"):
            # Remplacer les espaces et les tirets par des underscores et convertir le nom en minuscules pour une uniformisation
            new_name = filename.replace(" ", "_").replace("-", "_").lower()


            # Déterminer la catégorie du fichier en fonction de son nom
            for category in categories:
                # Si le nom du fichier contient le nom d'une catégorie, l'associer à cette catégorie
                if category in new_name:
                    category_folder = categories[category]

                    # Créer le dossier de la catégorie si il n'existe pas déjà
                    if not os.path.exists(category_folder):
                        os.makedirs(category_folder)

                    # Déplacer le fichier dans le dossier correspondant
                    shutil.move(os.path.join(directory, filename), os.path.join(category_folder, new_name))

                    # Afficher un message pour confirmer que le fichier a été déplacé
                    print(f"Le fichier {filename} a été déplacé vers {category_folder}")
                    break

# Appeler la fonction pour organiser les fichiers
organize_files(directory)
