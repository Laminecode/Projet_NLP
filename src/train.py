import os
from pathlib import Path
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from collections import Counter

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras import regularizers

# =========================
# CONFIGURATION
# =========================
DATA_DIR = "data/processed_clean"
MODEL_CLASS_PATH = "results/models/classifier_fixed.keras"
MODEL_GEN_PATH = "results/models/generator_fixed.keras"
TOKENIZER_CLASS_PATH = "results/models/tokenizer_class.pkl"
TOKENIZER_GEN_PATH = "results/models/tokenizer_gen.pkl"

# Classification - Configuration pour éviter overfitting
MAX_WORDS_CLASS = 2000  # Vocabulaire TRÈS réduit
MAX_LEN_CLASS = 80      # Séquences plus courtes

# Generation
MAX_WORDS_GEN = 1500
SEQ_LENGTH = 8          # Très court
MIN_WORD_FREQ = 5

EMBEDDING_DIM = 32      # Très petit
EPOCHS_CLASS = 100
EPOCHS_GEN = 150

# =========================
# LOAD DATA
# =========================
def load_documents(data_dir):
    """Load documents and labels."""
    texts = []
    labels = []
    for label in ["gaza", "ukraine"]:
        folder = Path(data_dir) / label
        if not folder.exists():
            print(f"⚠️  Warning: Folder {folder} does not exist")
            continue
        
        count = 0
        for file in folder.glob("*.txt"):
            with open(file, "r", encoding="utf-8") as f:
                content = f.read().strip().lower()  # Lowercase dès le début
                if content and len(content.split()) > 10:
                    texts.append(content)
                    labels.append(label)
                    count += 1
        
        print(f"✅ Loaded {count} {label} documents")
    
    return texts, labels

# =========================
# CLASSIFICATION - SOLUTION AU PROBLÈME
# =========================
def train_classification_fixed():
    """
    Train classifier with HEAVY regularization to prevent overfitting.
    
    Le problème précédent:
    - 126 samples d'entraînement seulement
    - Modèle trop complexe → mémorise au lieu d'apprendre
    - 100% val_accuracy = overfitting sévère
    - En production, prédit toujours la même classe
    
    Solution:
    - Modèle BEAUCOUP plus simple
    - Régularisation agressive
    - Data augmentation implicite (lowercase, truncation)
    """
    print("\n" + "="*60)
    print("🔨 TRAINING FIXED CLASSIFIER")
    print("="*60)
    
    texts, labels = load_documents(DATA_DIR)
    
    if len(texts) == 0:
        raise ValueError("No documents found.")
    
    print(f"\n📊 Dataset: {len(texts)} documents")
    gaza_count = labels.count('gaza')
    ukraine_count = labels.count('ukraine')
    print(f"   - Gaza: {gaza_count} ({gaza_count/len(labels)*100:.1f}%)")
    print(f"   - Ukraine: {ukraine_count} ({ukraine_count/len(labels)*100:.1f}%)")
    
    # Encode labels
    encoder = LabelEncoder()
    y = encoder.fit_transform(labels)
    
    # Tokenization avec vocabulaire TRÈS réduit
    tokenizer = Tokenizer(num_words=MAX_WORDS_CLASS, oov_token='<UNK>')
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    X = pad_sequences(sequences, maxlen=MAX_LEN_CLASS, padding="post", truncating="post")
    
    print(f"\n📚 Vocabulary: {min(len(tokenizer.word_index), MAX_WORDS_CLASS)} words")
    print(f"📏 Sequence length: {MAX_LEN_CLASS}")
    
    # Split stratified
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y  # 25% validation
    )
    
    print(f"\n📦 Training: {len(X_train)} samples")
    print(f"📦 Validation: {len(X_val)} samples")
    print(f"   - Gaza val: {sum(y_val == 0)}")
    print(f"   - Ukraine val: {sum(y_val == 1)}")
    
    # Modèle ULTRA SIMPLE avec régularisation maximale
    model = Sequential([
        Embedding(
            MAX_WORDS_CLASS, 
            EMBEDDING_DIM, 
            input_length=MAX_LEN_CLASS,
            embeddings_regularizer=regularizers.l2(0.001)  # Régularisation L2
        ),
        GlobalAveragePooling1D(),  # Plus simple que LSTM !
        Dropout(0.6),  # Dropout élevé
        Dense(
            8, 
            activation="relu",
            kernel_regularizer=regularizers.l2(0.01)  # Régularisation forte
        ),
        Dropout(0.6),
        Dense(1, activation="sigmoid")
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),  # LR très bas
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )
    
    print(f"\n🏗️  Simple Model (to prevent overfitting):")
    model.summary()
    
    # Callbacks
    callbacks = [
        EarlyStopping(
            monitor='val_loss',
            patience=20,  # Beaucoup de patience
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            MODEL_CLASS_PATH,
            save_best_only=True,
            monitor='val_loss',
            verbose=1
        )
    ]
    
    print("\n🚀 Training (this will take longer but learn better)...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS_CLASS,
        batch_size=8,  # Petit batch pour meilleure généralisation
        callbacks=callbacks,
        verbose=2
    )
    
    # Save
    os.makedirs("results/models", exist_ok=True)
    model.save(MODEL_CLASS_PATH)
    with open(TOKENIZER_CLASS_PATH, "wb") as f:
        pickle.dump({'tokenizer': tokenizer, 'encoder': encoder}, f)
    
    # Evaluation détaillée
    print("\n" + "="*60)
    print("📊 DETAILED EVALUATION")
    print("="*60)
    
    train_loss, train_acc = model.evaluate(X_train, y_train, verbose=0)
    val_loss, val_acc = model.evaluate(X_val, y_val, verbose=0)
    
    print(f"\n✅ Training Accuracy: {train_acc:.4f}")
    print(f"✅ Validation Accuracy: {val_acc:.4f}")
    
    gap = abs(train_acc - val_acc)
    print(f"\n📊 Overfitting Gap: {gap:.4f}")
    if gap < 0.10:
        print("   ✅ Good generalization!")
    elif gap < 0.20:
        print("   ⚠️  Some overfitting")
    else:
        print("   🚨 Severe overfitting!")
    
    # Test predictions distribution
    val_preds = (model.predict(X_val, verbose=0) > 0.5).astype(int).flatten()
    print(f"\n📊 Validation Predictions Distribution:")
    print(f"   Predicted Gaza: {sum(val_preds == 0)} / {sum(y_val == 0)} actual")
    print(f"   Predicted Ukraine: {sum(val_preds == 1)} / {sum(y_val == 1)} actual")
    
    # Per-class accuracy
    print(f"\n🧪 Per-class accuracy:")
    for idx, label_name in enumerate(encoder.classes_):
        mask = y_val == idx
        if mask.sum() > 0:
            class_preds = val_preds[mask]
            class_acc = np.mean(class_preds == y_val[mask])
            print(f"   {label_name}: {class_acc:.4f} ({mask.sum()} samples)")
    
    # Test avec quelques exemples
    print(f"\n🧪 Quick sanity check:")
    test_samples = [
        ("gaza strip israeli forces", 0),  # Should be Gaza
        ("ukraine russian military invasion", 1),  # Should be Ukraine
    ]
    
    for text, expected in test_samples:
        seq = tokenizer.texts_to_sequences([text])
        padded = pad_sequences(seq, maxlen=MAX_LEN_CLASS, padding="post")
        prob = model.predict(padded, verbose=0)[0][0]
        pred_label = encoder.classes_[1 if prob > 0.5 else 0]
        expected_label = encoder.classes_[expected]
        
        status = "✅" if (prob > 0.5) == expected else "❌"
        print(f"   {status} '{text}' → {pred_label} (prob: {prob:.3f}, expected: {expected_label})")
    
    return model, tokenizer, encoder

# =========================
# GÉNÉRATION SIMPLIFIÉE
# =========================
def train_text_generation_optimized():
    """Train simple generator."""
    print("\n" + "="*60)
    print("🔨 TRAINING TEXT GENERATOR")
    print("="*60)
    
    texts, labels = load_documents(DATA_DIR)
    
    print(f"\n📚 Total: {len(texts)} documents")
    
    # Tokenization très réduite
    tokenizer = Tokenizer(num_words=MAX_WORDS_GEN)
    tokenizer.fit_on_texts(texts)
    
    # Filter vocabulary
    word_freq = tokenizer.word_counts
    common_words = [(word, freq) for word, freq in word_freq.items() 
                    if freq >= MIN_WORD_FREQ]
    common_words.sort(key=lambda x: x[1], reverse=True)
    common_words = common_words[:MAX_WORDS_GEN-1]
    
    print(f"📊 Original vocabulary: {len(word_freq)}")
    print(f"📊 Filtered vocabulary: {len(common_words)}")
    
    # Recreate tokenizer
    tokenizer.word_index = {}
    for i, (word, _) in enumerate(common_words, start=1):
        tokenizer.word_index[word] = i
    
    vocab_size = len(tokenizer.word_index) + 1
    print(f"📚 Final vocabulary: {vocab_size}")
    
    # Create sequences
    sequences = []
    for text in texts:
        tokens = tokenizer.texts_to_sequences([text])[0]
        if len(tokens) > SEQ_LENGTH:
            for i in range(0, len(tokens) - SEQ_LENGTH, 2):
                seq = tokens[i:i + SEQ_LENGTH + 1]
                sequences.append(seq)
    
    sequences = np.array(sequences)
    X, y = sequences[:, :-1], sequences[:, -1]
    
    # Filter valid
    valid_mask = (y > 0) & (y < vocab_size)
    X, y = X[valid_mask], y[valid_mask]
    
    print(f"📊 Training sequences: {len(X)}")
    
    y = to_categorical(y, num_classes=vocab_size)
    
    # Simple model
    model = Sequential([
        Embedding(vocab_size, 32, input_length=SEQ_LENGTH),
        LSTM(32, dropout=0.3),
        Dense(vocab_size, activation='softmax')
    ])
    
    model.compile(
        loss='categorical_crossentropy',
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.003),
        metrics=['accuracy']
    )
    
    print(f"\n🏗️  Model:")
    model.summary()
    
    callbacks = [
        EarlyStopping(monitor='loss', patience=15, restore_best_weights=True, verbose=1),
        ModelCheckpoint(MODEL_GEN_PATH, save_best_only=True, monitor='loss', verbose=1)
    ]
    
    print("\n🚀 Training...")
    history = model.fit(
        X, y,
        epochs=EPOCHS_GEN,
        batch_size=256,
        callbacks=callbacks,
        verbose=2
    )
    
    model.save(MODEL_GEN_PATH)
    
    with open(TOKENIZER_GEN_PATH, "wb") as f:
        pickle.dump({'tokenizer': tokenizer, 'seq_length': SEQ_LENGTH}, f)
    
    final_acc = history.history['accuracy'][-1]
    print(f"\n✅ Saved (accuracy: {final_acc:.4f})")
    
    return model, tokenizer

# =========================
# PREDICTION & GENERATION
# =========================
def predict_text_class(model, tokenizer, encoder, text):
    """Classify text."""
    seq = tokenizer.texts_to_sequences([text.lower()])
    padded = pad_sequences(seq, maxlen=MAX_LEN_CLASS, padding="post")
    prob = model.predict(padded, verbose=0)[0][0]
    
    if prob >= 0.5:
        label_idx = 1
    else:
        label_idx = 0
    
    label = encoder.classes_[label_idx].upper()
    confidence = prob if label_idx == 1 else 1 - prob
    
    return label, confidence, prob

def generate_text(model, tokenizer, seed_text, max_words=15, temperature=0.4):
    """Generate text."""
    result = seed_text.lower()
    
    for _ in range(max_words):
        tokens = tokenizer.texts_to_sequences([result])[0]
        if len(tokens) == 0:
            break
            
        tokens = tokens[-SEQ_LENGTH:]
        tokens = pad_sequences([tokens], maxlen=SEQ_LENGTH, padding='pre')[0]
        
        preds = model.predict(np.array([tokens]), verbose=0)[0]
        preds = np.log(np.clip(preds, 1e-10, 1.0)) / temperature
        exp_preds = np.exp(preds - np.max(preds))
        preds = exp_preds / np.sum(exp_preds)
        
        predicted_id = np.random.choice(len(preds), p=preds)
        
        if predicted_id == 0:
            continue
        
        word = None
        for w, idx in tokenizer.word_index.items():
            if idx == predicted_id:
                word = w
                break
        
        if word:
            result += " " + word
        else:
            break
    
    return result

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("="*60)
    print("🔧 FIXED PIPELINE - NO MORE OVERFITTING!")
    print("="*60)
    
    # Classification
    if not os.path.exists(MODEL_CLASS_PATH):
        model_clf, tokenizer_clf, encoder = train_classification_fixed()
    else:
        print("\n📂 Loading classifier...")
        model_clf = tf.keras.models.load_model(MODEL_CLASS_PATH)
        with open(TOKENIZER_CLASS_PATH, "rb") as f:
            data = pickle.load(f)
            tokenizer_clf = data['tokenizer']
            encoder = data['encoder']
        print("✅ Loaded")
    
    # Generation
    if not os.path.exists(MODEL_GEN_PATH):
        model_gen, tok_gen = train_text_generation_optimized()
    else:
        print("\n📂 Loading generator...")
        model_gen = tf.keras.models.load_model(MODEL_GEN_PATH)
        with open(TOKENIZER_GEN_PATH, "rb") as f:
            data = pickle.load(f)
            tok_gen = data['tokenizer']
        print("✅ Loaded")
    
    # EXTENSIVE TESTS
    print("\n" + "="*60)
    print("🧪 EXTENSIVE CLASSIFICATION TESTS")
    print("="*60)
    
    test_samples = [
        # Gaza samples
        "israeli forces attacked gaza strip",
        "hamas militants launched rockets",
        "gaza city residential buildings destroyed",
        "palestinian civilians evacuated",
        
        # Ukraine samples
        "russian military invaded ukraine",
        "ukrainian army defended territory",
        "nato provided weapons support",
        "zelensky addressed parliament",
        
        # Ambiguous
        "humanitarian crisis worsened",
        "military operation continued"
    ]
    
    print("\n📊 Testing classifier:")
    for sample in test_samples:
        label, conf, prob = predict_text_class(model_clf, tokenizer_clf, encoder, sample)
        print(f"\n'{sample}'")
        print(f"  → {label} ({conf:.1%}) [prob={prob:.3f}]")
    
    # Generation
    if model_gen and tok_gen:
        print("\n" + "="*60)
        print("📝 GENERATION TESTS")
        print("="*60)
        
        prompts = ["israeli", "russian", "hamas", "ukrainian", "military"]
        
        for prompt in prompts:
            gen = generate_text(model_gen, tok_gen, prompt, 12, 0.4)
            print(f"\n'{prompt}' → {gen}")
    
    print("\n" + "="*60)
    print("✅ Done!")
    print("="*60)