from PyPDF2 import PdfReader
import os

# Chemin du répertoire de sortie pour les fichiers texte extraits
dossier_sortie = "C:/Users/Utilisateur/Documents/Devoirs et Cours 5A/PTUT/rh-documents-txt"

# Fonction pour extraire le texte d'un fichier PDF
def extract_text_with_pyPDF(PDF_File):
    pdf_reader = PdfReader(PDF_File)
    raw_text = ''

    for i, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text

    return raw_text

# Chemin du dossier racine contenant les sous-répertoires "Guide", "FAQ", "Fiche"
dossier_pdf_racine = "C:\\Users\\Utilisateur\\Documents\\Devoirs et Cours 5A\\PTUT\\Tri"

# Vérification si le dossier de sortie existe, sinon le créer
if not os.path.exists(dossier_sortie):
    os.makedirs(dossier_sortie)

# Itération sur tous les sous-dossiers dans le répertoire racine
for sous_dossier in os.listdir(dossier_pdf_racine):
    chemin_sous_dossier = os.path.join(dossier_pdf_racine, sous_dossier)

    # Vérifier si c'est un dossier
    if os.path.isdir(chemin_sous_dossier):
        # Itérer sur tous les fichiers PDF dans ce sous-dossier
        for fichier_pdf in os.listdir(chemin_sous_dossier):
            if fichier_pdf.endswith(".pdf"):
                chemin_fichier_pdf = os.path.join(chemin_sous_dossier, fichier_pdf)

                # Extraction du texte
                text_with_pyPDF = extract_text_with_pyPDF(chemin_fichier_pdf)

                # Créer le nom du fichier TXT (même nom que le PDF, mais avec l'extension .txt)
                nom_fichier_txt = os.path.splitext(fichier_pdf)[0] + ".txt"

                # Chemin complet du fichier TXT
                chemin_fichier_sortie = os.path.join(dossier_sortie, nom_fichier_txt)

                # Écriture du texte extrait dans le fichier TXT
                with open(chemin_fichier_sortie, "w", encoding="utf-8") as fichier:
                    fichier.write(text_with_pyPDF)

                print(f"Extraction terminée : '{fichier_pdf}' enregistré dans '{chemin_fichier_sortie}'")

print("Traitement des PDF terminé. Tous les fichiers extraits ont été enregistrés.")