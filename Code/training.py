import json
import os
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset

# Disable oneDNN optimizations if necessary
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Load the processed data
with open('processed_linux_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Combine all the content from different sections
all_texts = []
for section, files in data.items():
    for file_data in files:
        all_texts.append(file_data['content'])

# Create a Hugging Face Dataset
dataset = Dataset.from_dict({"text": all_texts})

# Load pretrained GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Add a padding token to the tokenizer
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model.resize_token_embeddings(len(tokenizer))

# Move the model to GPU if available
if torch.cuda.is_available():
    device = torch.device("cuda")
    model.to(device)
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
else:
    device = torch.device("cpu")
    print("Using CPU")


# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Set up training arguments
training_args = TrainingArguments(
    output_dir="./gpt2-linux-model",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=10_000,
    save_total_limit=2,
    logging_dir="./logs",
    evaluation_strategy="steps",
    eval_steps=5000,
    fp16=True,  # Mixed precision (fp16) helps in using GPU efficiently
    dataloader_pin_memory=True,  # Pin memory for DataLoader to improve GPU utilization
    report_to="none",  # Reduce noise
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
