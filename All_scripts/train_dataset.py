from datasets import load_dataset
from transformers import DistilBertTokenizer, DistilBertForMaskedLM, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

# Step 1: Load the dataset
dataset = load_dataset("PtutISIS/train-dataset")

# Step 2: Tokenize the dataset
def tokenize_data(dataset, tokenizer):
    def tokenize_function(examples):
        return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)
    return dataset.map(tokenize_function, batched=True, remove_columns=["text"])

# Load the tokenizer and model
model_name = "almanach/camembertav2-base"  
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
    output_dir="./camembert-finetuned",
    eval_strategy="no",
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

# Étape 6 : Sauvegarder le modèle fine-tuné
output_model_dir = "C:/Users/Utilisateur/Documents/Devoirs et Cours 5A/PTUT/Train" # Répertoire où le modèle sera sauvegardé
model.save_pretrained(output_model_dir)
tokenizer.save_pretrained(output_model_dir)

print(f"Fine-tuning du modèle terminé et modèle sauvegardé dans : {output_model_dir}")
