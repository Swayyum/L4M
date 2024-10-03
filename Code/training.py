import json
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset

# Load the processed data
with open('processed_linux_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Combine all the content from different sections
all_texts = []
for section, files in data.items():
    for file_data in files:
        all_texts.append(file_data['content'])

# Tokenize the texts
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True)

# Create a Hugging Face Dataset
dataset = Dataset.from_dict({"text": all_texts})

# Load pretrained GPT-2 model and tokenizer
model_name = "gpt2"  # You can also use 'gpt2-medium' or 'gpt2-large' if resources permit
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Tokenize the dataset
tokenized_dataset = dataset.map(lambda examples: tokenizer(examples["text"], padding="max_length", truncation=True), batched=True)

# Set up training arguments
training_args = TrainingArguments(
    output_dir="./gpt2-linux-model",
    overwrite_output_dir=True,
    num_train_epochs=3,  # You can adjust this
    per_device_train_batch_size=4,  # Adjust batch size based on your hardware
    save_steps=10_000,
    save_total_limit=2,
    logging_dir="./logs",
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("./gpt2-linux-model")
tokenizer.save_pretrained("./gpt2-linux-model")
