import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Spécifie le modèle correct
model_name = "almanach/camembertav2-base"

try:
    print("Chargement du tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print("Tokenizer chargé.")

    print("Chargement du modèle...")
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    print("Modèle chargé.")
except Exception as e:
    print(f"Une erreur s'est produite lors du chargement du modèle ou du tokenizer: {e}")
