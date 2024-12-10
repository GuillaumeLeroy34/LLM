from PyPDF2 import PdfReader
import os

# Chemin du dossier où tu veux enregistrer les fichiers TXT
dossier_sortie = "C:\\Users\\Utilisateur\\Documents\\Devoirs et Cours 5A\\PTUT\\Full PDF extract"

# Fonction pour extraire le texte d'un fichier PDF
def extract_text_with_pyPDF(PDF_File):
    pdf_reader = PdfReader(PDF_File)
    raw_text = ''

    for i, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text

    return raw_text

# Chemin du dossier contenant les fichiers PDF
#TODO faire en sorte que ça soit facilement modifiable 
dossier_pdf = "C:\\Users\\Utilisateur\\Documents\\Devoirs et Cours 5A\\PTUT\\Sources RAG - Fine-tuning\\santexpo2024-dev\\pdf_all"

# Vérification si le dossier de sortie existe, sinon le créer
if not os.path.exists(dossier_sortie):
    os.makedirs(dossier_sortie)

# Itération sur tous les fichiers PDF dans le dossier pdf_all
for fichier_pdf in os.listdir(dossier_pdf):
    # Vérifier si le fichier est un PDF
    if fichier_pdf.endswith(".pdf"):
        chemin_fichier_pdf = os.path.join(dossier_pdf, fichier_pdf)
        
        # Extraction du texte
        text_with_pyPDF = extract_text_with_pyPDF(chemin_fichier_pdf)
        
        # Créer le nom du fichier TXT (même nom que le PDF, mais avec l'extension .txt)
        nom_fichier_txt = os.path.splitext(fichier_pdf)[0] + ".txt"
        
        # Chemin complet du fichier TXT
        chemin_fichier_sortie = os.path.join(dossier_sortie, nom_fichier_txt)
        
        # Écriture du texte extrait dans le fichier TXT
        with open(chemin_fichier_sortie, "w", encoding="utf-8") as fichier:
            fichier.write(text_with_pyPDF)
        
        print(f"Le texte du fichier PDF '{fichier_pdf}' a été extrait et enregistré dans le fichier : {chemin_fichier_sortie}")
