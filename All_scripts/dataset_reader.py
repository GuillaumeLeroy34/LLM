from datasets import load_dataset

# Essaye de charger le dataset
try:
    dataset = load_dataset("PtutISIS/train-dataset", split="train")
    print("Dataset chargé avec succès !")
    print(dataset)
except Exception as e:
    print(f"Erreur lors du chargement du dataset : {e}")
