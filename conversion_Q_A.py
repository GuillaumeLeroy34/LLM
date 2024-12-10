import os
import csv
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

def charger_modele_bloom():
    """
    Charge le modèle BLOOM-560M depuis Hugging Face.
    """
    model_name = "bigscience/bloom-560m"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

def generer_question_reponse_bloom(pipeline_model, texte, max_length=200):
    """
    Utilise BLOOM pour générer une question-réponse à partir d'un segment de texte.
    """
    prompt = (
        f"Voici un extrait de texte :\n{texte}\n\n"
        "Générez une question pertinente sur ce contenu suivie d'une réponse concise au format :\n"
        "Question : [votre question]\nRéponse : [votre réponse]."
    )
    resultat = pipeline_model(
        prompt,
        max_length=max_length,
        truncation=True,
        num_return_sequences=1,
        temperature=0.7,
        top_p=0.9
    )
    texte_genere = resultat[0]["generated_text"]
    print(texte_genere)
    # Extraire question et réponse du texte généré
    try:
        question = texte_genere.split("Question :")[1].split("Réponse :")[0].strip()
        reponse = texte_genere.split("Réponse :")[1].strip()
        return question, reponse
    except IndexError:
        return None, None

def traiter_fichier_texte(pipeline_model, fichier_entree, fichier_sortie, segment_size=500):
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
        question, reponse = generer_question_reponse_bloom(pipeline_model, segment)
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

    # Chargement du modèle BLOOM
    print("Chargement du modèle BLOOM-560M...")
    pipeline_model = charger_modele_bloom()

    for fichier in fichiers:
        chemin_entree = os.path.join(dossier_entree, fichier)
        nom_csv = os.path.splitext(fichier)[0] + ".csv"
        chemin_sortie = os.path.join(dossier_sortie, nom_csv)

        print(f"Traitement de {fichier}...")
        traiter_fichier_texte(pipeline_model, chemin_entree, chemin_sortie)

if __name__ == "__main__":
    dossier_entree = "./fichiers_texte"
    dossier_sortie = "./Q_A"

    traiter_dossier(dossier_entree, dossier_sortie)
    print(f"Tâche terminée. Les fichiers CSV sont disponibles dans {dossier_sortie}.")
