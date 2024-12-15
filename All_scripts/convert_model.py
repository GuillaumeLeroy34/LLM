from transformers import AutoModelForSequenceClassification
from transformers.onnx import export #TODO enlever: code pour l'export du modèle vers un format compréhensible par lm studio


model = AutoModelForSequenceClassification.from_pretrained("C:/Users/guill/.cache/lm-studio/models/distilbert-finetuned")

# Export to ONNX
onnx_path = "path_to_saved_model/model.onnx"
export(model, "text-classification", onnx_path)
