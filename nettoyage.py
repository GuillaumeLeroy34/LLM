import os
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import re

def nettoyer_texte(texte):
    """
    Nettoie le texte brut extrait d'un fichier PDF.
    Supprime les en-têtes, les numéros de pages et les espaces superflus.
    """
    texte = re.sub(r"Page \d+|\n\d+\s*", "", texte)  # Supprime les numéros de pages
    texte = re.sub(r"\s{2,}", " ", texte)  # Réduit les espaces multiples
    texte = re.sub(r"\n+", "\n", texte)  # Réduit les sauts de ligne multiples
    return texte.strip()

def charger_modele_bloom(model_name="bigscience/bloom-560m"):
    """
    Charge le modèle BLOOM via Huggingface pour la correction de texte.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

def traiter_texte_par_modele_bloom(pipeline_model, texte, max_length=512):
    prompt = (
        "Réécrivez ce texte pour qu'il soit concis et lisible, sans répétition inutile :\n\n"
        f"{texte}\n\nTexte réécrit :"
    )

    # Génération de texte par le modèle
    resultat = pipeline_model(
        prompt,
        max_length=max_length,
        truncation=True,
        num_return_sequences=1,
    )
    texte_genere = resultat[0]["generated_text"]

    # Suppression du prompt dans le texte généré
    texte_genere = texte_genere.replace(prompt, "").strip()

    return texte_genere
def lire_et_corriger_fichier(pipeline_model, fichier_entree, max_length=1024):
    """
    Lit un fichier texte, corrige et nettoie chaque segment.
    """
    with open(fichier_entree, "r", encoding="utf-8") as f:
        contenu = f.read()

    # Nettoyer le contenu initialement
    contenu_nettoye = nettoyer_texte(contenu)

    # Diviser en segments pour le modèle
    segments = [contenu_nettoye[i:i + max_length] for i in range(0, len(contenu_nettoye), max_length)]

    texte_corrige = ""
    for i, segment in enumerate(segments):
        print(f"Traitement du segment {i + 1}/{len(segments)} pour {fichier_entree}...")
        texte_corrige += traiter_texte_par_modele_bloom(pipeline_model, segment, max_length) + "\n"
        
    return texte_corrige.strip()

def sauvegarder_texte(texte, chemin_sortie):
    """
    Sauvegarde le texte corrigé dans un fichier.
    """
    with open(chemin_sortie, "w", encoding="utf-8") as f:
        f.write(texte)

def traiter_fichiers_dossier(dossier_entree, dossier_sortie, pipeline_model, max_length=512):
    """
    Traite tous les fichiers texte dans un dossier, les corrige et les enregistre dans un autre dossier.
    """
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    fichiers = [f for f in os.listdir(dossier_entree) if f.endswith(".txt")]

    for fichier in fichiers:
        chemin_entree = os.path.join(dossier_entree, fichier)
        chemin_sortie = os.path.join(dossier_sortie, fichier)

        print(f"Traitement de {fichier}...")
        texte_corrige = lire_et_corriger_fichier(pipeline_model, chemin_entree, max_length)
        
        print(f"Sauvegarde de {fichier} corrigé...")
        sauvegarder_texte(texte_corrige, chemin_sortie)

if __name__ == "__main__":
    dossier_entree = "./fichiers_texte"
    dossier_sortie = "./fichiers_corriges"

    print("Chargement du modèle BLOOM...")
    pipeline_model = charger_modele_bloom()

    print("Correction des fichiers...")
    traiter_fichiers_dossier(dossier_entree, dossier_sortie, pipeline_model)
    print(f"Tous les fichiers ont été corrigés et sauvegardés dans {dossier_sortie}.")
