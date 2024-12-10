from datasets import load_dataset
from transformers import DistilBertTokenizer, DistilBertForMaskedLM, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from transformers import AutoModelForSequenceClassification
from transformers.onnx import export #TODO enlever: code pour l'export du modèle vers un format compréhensible par lm studio
# Step 1: Load the dataset
dataset = load_dataset("PtutISIS/train-dataset")

# Step 2: Tokenize the dataset
def tokenize_data(dataset, tokenizer):
    def tokenize_function(examples):
        return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)
    return dataset.map(tokenize_function, batched=True, remove_columns=["text"])

# Load the tokenizer and model
model_name = "distilbert-base-uncased"  
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForMaskedLM.from_pretrained(model_name)

# Tokenize the dataset
tokenized_dataset = tokenize_data(dataset, tokenizer)

# Step 3: Prepare the data collator for masked language modeling
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)

# Step 4: Define training arguments
training_args = TrainingArguments(
    output_dir="./distilbert-finetuned",
    eval_strategy="epoch",
    eval_steps=500,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    save_steps=1000,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=100,
    learning_rate=5e-5,
    num_train_epochs=3,
    weight_decay=0.01,
    report_to="none",  # Disable reports (like to WandB or Tensorboard)
    push_to_hub=False,  # Disable hub pushing for this example
)

# Step 5: Create Trainer and start fine-tuning
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"] if "validation" in tokenized_dataset else None,
    data_collator=data_collator,
    processing_class=tokenizer,
)

trainer.train()

# Step 6: Save the fine-tuned model
model.save_pretrained("./distilbert-finetuned")
tokenizer.save_pretrained("./distilbert-finetuned")

print("Model fine-tuning complete!")

model = AutoModelForSequenceClassification.from_pretrained("C:/Users/guill/.cache/lm-studio/models/distilbert-finetuned/checkpoint-3000")

# Export to ONNX
onnx_path = "path_to_saved_model/model.onnx"
export(model, "text-classification", onnx_path)
