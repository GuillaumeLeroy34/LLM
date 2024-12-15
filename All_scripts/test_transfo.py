from transformers import pipeline

# Charger un pipeline de génération de texte avec DistilGPT-2
generator = pipeline("text-generation", model="distilgpt2")

# Générer un texte
text = generator("What is the capital of France?", 
    max_length=50, 
    num_return_sequences=1,
    truncation=True,  # Assurer que le texte ne dépasse pas la longueur maximale
    temperature=0.7,  # Ajuste la diversité des résultats
    top_k=50,  # Limite la génération à 50 mots les plus probables
    no_repeat_ngram_size=2  # Evite la répétition de n-grams
    )

# Afficher le texte généré
print(text)
