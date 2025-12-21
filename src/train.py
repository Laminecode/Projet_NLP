import os
import pandas as pd
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset

# Paths to data
semantic_data_path = "../results/semantic"
sentiment_data_path = "../results/sentiment"

# Load and preprocess data
def load_data():
    # Combine semantic and sentiment data
    semantic_files = [os.path.join(semantic_data_path, f) for f in os.listdir(semantic_data_path) if f.endswith(".csv")]
    sentiment_files = [os.path.join(sentiment_data_path, f) for f in os.listdir(sentiment_data_path) if f.endswith(".csv")]

    data = []
    for file in semantic_files + sentiment_files:
        df = pd.read_csv(file)
        # Assuming the text data is in a column named 'text'
        if 'text' in df.columns:
            data.extend(df['text'].tolist())
    return data

# Prepare dataset
def prepare_dataset(data):
    return Dataset.from_dict({"text": data})

# Main training function
def train_model():
    # Load data
    data = load_data()
    dataset = prepare_dataset(data)

    # Load tokenizer and model
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    # Tokenize data
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./results/trained_model",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        save_steps=500,
        save_total_limit=2,
        logging_dir="./logs",
        logging_steps=10,
        push_to_hub=False,
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        tokenizer=tokenizer,
    )

    # Train the model
    trainer.train()

    # Save the model
    trainer.save_model("./results/trained_model")
    tokenizer.save_pretrained("./results/trained_model")

if __name__ == "__main__":
    train_model()