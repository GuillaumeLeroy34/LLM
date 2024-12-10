import os
import csv
import requests  # For interacting with LM Studio if it exposes an HTTP API

# Configuration for the LM Studio API
LM_STUDIO_URL = "http://127.0.0.1:1234"  # Update this URL if needed

def generer_question_reponse_phi3(texte, max_length=200):
    """
    Utilise le modèle phi-3 via LM Studio pour générer une question-réponse à partir d'un segment de texte.
    """
    prompt = (
        f"Voici un extrait de texte :\n{texte}\n\n"
        "Générez une question pertinente sur ce contenu suivie d'une réponse concise au format :\n"
        "Question : [votre question]\nRéponse : [votre réponse]."
    )
    
    # Payload for LM Studio API
    payload = {
        "prompt": prompt,
        "max_length": max_length,
        "temperature": 0.7,
        "top_p": 0.9,
    }
    
    try:
        response = requests.post(LM_STUDIO_URL, json=payload)
        response.raise_for_status()
        texte_genere = response.json().get("text", "")

        # Extraire question et réponse
        try:
            question = texte_genere.split("Question :")[1].split("Réponse :")[0].strip()
            reponse = texte_genere.split("Réponse :")[1].strip()
            return question, reponse
        except IndexError:
            return None, None
    except requests.RequestException as e:
        print(f"Erreur lors de l'interaction avec le modèle phi-3 : {e}")
        return None, None

def traiter_fichier_texte(fichier_entree, fichier_sortie, segment_size=300):
    """
    Lit un fichier texte, génère des questions-réponses par segments et les sauvegarde dans un fichier CSV.
    """
    with open(fichier_entree, 'r', encoding='utf-8') as f:
        contenu = f.read()

    # Diviser le contenu en segments
    segments = [contenu[i:i + segment_size] for i in range(0, len(contenu), segment_size)]
    questions_reponses = []

    for i, segment in enumerate(segments):
        print(f"Traitement du segment {i + 1}/{len(segments)} pour {fichier_entree}...")
        question, reponse = generer_question_reponse_phi3(segment)
        if question and reponse:
            questions_reponses.append([question, reponse])

    # Sauvegarder les questions-réponses au format CSV
    with open(fichier_sortie, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["question", "réponse"])  # En-têtes du fichier CSV
        writer.writerows(questions_reponses)

    print(f"Fichier CSV créé : {fichier_sortie}")

def traiter_dossier(dossier_entree, dossier_sortie):
    """
    Traite tous les fichiers texte dans un dossier, génère des questions-réponses et les enregistre en CSV.
    """
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    fichiers = [f for f in os.listdir(dossier_entree) if f.endswith(".txt")]

    for fichier in fichiers:
        chemin_entree = os.path.join(dossier_entree, fichier)
        nom_csv = os.path.splitext(fichier)[0] + ".csv"
        chemin_sortie = os.path.join(dossier_sortie, nom_csv)

        print(f"Traitement de {fichier}...")
        traiter_fichier_texte(chemin_entree, chemin_sortie)

if __name__ == "__main__":
    dossier_entree = "./fichiers_texte"
    dossier_sortie = "./Q_A"

    traiter_dossier(dossier_entree, dossier_sortie)
    print(f"Tâche terminée. Les fichiers CSV sont disponibles dans {dossier_sortie}.")
