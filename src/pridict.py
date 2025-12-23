import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

# =========================
# CONFIGURATION
# =========================
RESULTS_DIR = "results/models"
MAX_LEN_CLASS = 200  # Doit correspondre à l'entraînement
SEQ_LENGTH = 20      # Doit correspondre à l'entraînement

# =========================
# CHARGEMENT DES MODÈLES
# =========================
def load_models():
    """Charge tous les modèles entraînés."""
    print("="*60)
    print("📂 CHARGEMENT DES MODÈLES")
    print("="*60)
    
    # Charger le classifier
    model_clf_path = f"{RESULTS_DIR}/lstm_gaza_ukraine_fixed.keras"
    tokenizer_clf_path = f"{RESULTS_DIR}/tokenizer_class.pkl"
    
    if not os.path.exists(model_clf_path):
        raise FileNotFoundError(f"❌ Modèle classifier non trouvé: {model_clf_path}")
    
    model_clf = tf.keras.models.load_model(model_clf_path)
    with open(tokenizer_clf_path, "rb") as f:
        data_clf = pickle.load(f)
        tokenizer_clf = data_clf['tokenizer']
        encoder = data_clf['encoder']
    
    print("✅ Classifier chargé")
    
    # Charger le générateur
    model_gen_path = f"{RESULTS_DIR}/lstm_textgen_universal.keras"
    tokenizer_gen_path = f"{RESULTS_DIR}/tokenizer_gen.pkl"
    
    if not os.path.exists(model_gen_path):
        raise FileNotFoundError(f"❌ Modèle générateur non trouvé: {model_gen_path}")
    
    model_gen = tf.keras.models.load_model(model_gen_path)
    with open(tokenizer_gen_path, "rb") as f:
        data_gen = pickle.load(f)
        tokenizer_gen = data_gen['tokenizer']
        seq_length = data_gen.get('seq_length', SEQ_LENGTH)
    
    print("✅ Générateur chargé")
    print("="*60)
    
    return model_clf, tokenizer_clf, encoder, model_gen, tokenizer_gen, seq_length

# =========================
# CLASSIFICATION
# =========================
def classify(text, model_clf, tokenizer_clf, encoder):
    """
    Classifie un texte comme Gaza ou Ukraine.
    
    Args:
        text: Le texte à classifier
        model_clf: Modèle de classification
        tokenizer_clf: Tokenizer du classifier
        encoder: Label encoder
    
    Returns:
        tuple: (label, confidence, raw_probability)
    """
    # Tokeniser et padder
    seq = tokenizer_clf.texts_to_sequences([text.lower()])
    padded = pad_sequences(seq, maxlen=MAX_LEN_CLASS, padding="post")
    
    # Prédire
    prob = model_clf.predict(padded, verbose=0)[0][0]
    
    # Décoder le label
    if prob >= 0.5:
        label_idx = 1
    else:
        label_idx = 0
    
    label = encoder.classes_[label_idx].upper()
    confidence = prob if label_idx == 1 else 1 - prob
    
    return label, confidence, prob

# =========================
# GÉNÉRATION DE TEXTE
# =========================
def generate(prompt, model_gen, tokenizer_gen, seq_length, num_words=20, temperature=0.7):
    """
    Génère du texte à partir d'un prompt.
    
    Args:
        prompt: Le texte de départ
        model_gen: Modèle de génération
        tokenizer_gen: Tokenizer du générateur
        seq_length: Longueur de séquence
        num_words: Nombre de mots à générer
        temperature: Contrôle la créativité (0.5=conservateur, 1.0=créatif)
    
    Returns:
        str: Le texte généré
    """
    result = prompt.lower()
    
    for _ in range(num_words):
        # Tokeniser
        tokens = tokenizer_gen.texts_to_sequences([result])[0]
        
        if len(tokens) == 0:
            break
        
        # Prendre les derniers tokens
        tokens = tokens[-seq_length:]
        tokens = pad_sequences([tokens], maxlen=seq_length, padding='pre')[0]
        
        # Prédire
        preds = model_gen.predict(np.array([tokens]), verbose=0)[0]
        
        # Sampling avec température
        preds = np.log(np.clip(preds, 1e-10, 1.0)) / temperature
        exp_preds = np.exp(preds - np.max(preds))
        preds = exp_preds / np.sum(exp_preds)
        
        # Choisir le prochain mot
        next_token = np.random.choice(len(preds), p=preds)
        
        if next_token == 0:  # Skip padding
            continue
        
        # Trouver le mot
        word = None
        for w, idx in tokenizer_gen.word_index.items():
            if idx == next_token:
                word = w
                break
        
        if word:
            result += " " + word
        else:
            break
    
    return result

# =========================
# EXEMPLES ET TESTS
# =========================
def run_examples(model_clf, tokenizer_clf, encoder, model_gen, tokenizer_gen, seq_length):
    """Exécute des exemples de classification et génération."""
    
    print("\n" + "="*60)
    print("📊 EXEMPLES DE CLASSIFICATION")
    print("="*60)
    
    test_texts = [
        "israeli forces attacked gaza city residential areas",
        "russian military invaded eastern ukraine regions",
        "hamas militants launched rockets from gaza strip",
        "nato countries provided weapons support ukraine",
        "humanitarian crisis civilians evacuated conflict zone",
        "military operation offensive defensive strategy",
    ]
    
    for text in test_texts:
        label, conf, prob = classify(text, model_clf, tokenizer_clf, encoder)
        print(f"\n📝 '{text}'")
        print(f"   → {label} (confiance: {conf:.1%}, raw: {prob:.4f})")
    
    print("\n" + "="*60)
    print("✍️  EXEMPLES DE GÉNÉRATION")
    print("="*60)
    
    prompts = [
        ("israeli forces", 20, 0.7),
        ("russian military", 20, 0.7),
        ("hamas militants", 15, 0.6),
        ("ukrainian troops", 15, 0.6),
        ("humanitarian crisis", 25, 0.8),
        ("military operation", 20, 0.7),
    ]
    
    for prompt, words, temp in prompts:
        generated = generate(prompt, model_gen, tokenizer_gen, seq_length, words, temp)
        print(f"\n🔹 Prompt: '{prompt}' ({words} mots, temp={temp})")
        print(f"   → {generated}")

# =========================
# MODE INTERACTIF
# =========================
def interactive_mode(model_clf, tokenizer_clf, encoder, model_gen, tokenizer_gen, seq_length):
    """Mode interactif pour tester les modèles."""
    
    print("\n" + "="*60)
    print("💬 MODE INTERACTIF")
    print("="*60)
    print("\n📖 Commandes disponibles:")
    print("  1. Tapez un texte pour le CLASSIFIER")
    print("  2. Tapez 'gen: votre prompt' pour GÉNÉRER du texte")
    print("  3. Tapez 'help' pour voir l'aide")
    print("  4. Tapez 'quit' pour quitter")
    print("\n" + "-"*60)
    
    while True:
        try:
            user_input = input("\n>>> ").strip()
            
            if not user_input:
                continue
            
            # Commande quit
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Au revoir!")
                break
            
            # Commande help
            if user_input.lower() == 'help':
                print("\n📖 AIDE:")
                print("  Classification: tapez simplement votre texte")
                print("    Ex: 'israeli attacks on gaza'")
                print("\n  Génération: utilisez 'gen:' suivi de votre prompt")
                print("    Ex: 'gen: russian forces'")
                print("    Ex: 'gen: humanitarian' pour texte court")
                print("    Ex: 'gen: military operation' pour texte long")
                continue
            
            # Mode génération
            if user_input.lower().startswith('gen:'):
                prompt = user_input[4:].strip()
                if not prompt:
                    print("❌ Erreur: Veuillez fournir un prompt après 'gen:'")
                    print("   Exemple: gen: israeli forces")
                    continue
                
                print(f"\n⏳ Génération en cours...")
                generated = generate(prompt, model_gen, tokenizer_gen, seq_length, 
                                   num_words=25, temperature=0.7)
                print(f"\n✍️  Texte généré:")
                print(f"   {generated}")
            
            # Mode classification
            else:
                print(f"\n⏳ Classification en cours...")
                label, conf, prob = classify(user_input, model_clf, tokenizer_clf, encoder)
                print(f"\n📊 Résultat:")
                print(f"   Label: {label}")
                print(f"   Confiance: {conf:.1%}")
                print(f"   Probabilité brute: {prob:.4f}")
                
                # Afficher une interprétation
                if conf > 0.9:
                    print(f"   💯 Très confiant - C'est clairement {label}")
                elif conf > 0.7:
                    print(f"   ✅ Confiant - Probablement {label}")
                elif conf > 0.5:
                    print(f"   ⚠️  Incertain - Peut-être {label}")
                else:
                    print(f"   ❓ Très incertain")
        
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir!")
            break
        except Exception as e:
            print(f"\n❌ Erreur: {e}")

# =========================
# FONCTIONS RAPIDES
# =========================
def quick_classify(text):
    """Classification rapide (charge les modèles automatiquement)."""
    models = load_models()
    model_clf, tokenizer_clf, encoder = models[0], models[1], models[2]
    return classify(text, model_clf, tokenizer_clf, encoder)

def quick_generate(prompt, num_words=20):
    """Génération rapide (charge les modèles automatiquement)."""
    models = load_models()
    model_gen, tokenizer_gen, seq_length = models[3], models[4], models[5]
    return generate(prompt, model_gen, tokenizer_gen, seq_length, num_words)

# =========================
# MAIN
# =========================
def main():
    """Fonction principale."""
    print("="*60)
    print("🤖 UTILISATION DES MODÈLES ENTRAÎNÉS")
    print("="*60)
    
    # Charger tous les modèles
    try:
        model_clf, tokenizer_clf, encoder, model_gen, tokenizer_gen, seq_length = load_models()
    except FileNotFoundError as e:
        print(f"\n{e}")
        print("\n💡 Conseil: Entraînez d'abord les modèles avec:")
        print("   python pipeline_single_generator.py")
        return
    
    # Lancer les exemples
    run_examples(model_clf, tokenizer_clf, encoder, model_gen, tokenizer_gen, seq_length)
    
    # Lancer le mode interactif
    print("\n" + "="*60)
    interactive_mode(model_clf, tokenizer_clf, encoder, model_gen, tokenizer_gen, seq_length)

# =========================
# EXEMPLES D'UTILISATION
# =========================
if __name__ == "__main__":
    # Mode 1: Lancer le programme complet (exemples + interactif)
    main()
    
    # Mode 2: Utilisation directe dans un script
    """
    # Charger les modèles une fois
    models = load_models()
    model_clf, tokenizer_clf, encoder, model_gen, tokenizer_gen, seq_length = models
    
    # Classifier
    label, conf, prob = classify("israeli forces gaza", model_clf, tokenizer_clf, encoder)
    print(f"{label}: {conf:.0%}")
    
    # Générer
    text = generate("russian military", model_gen, tokenizer_gen, seq_length, num_words=20)
    print(text)
    """
    
    # Mode 3: Fonctions rapides (chargent les modèles automatiquement)
    """
    # Classification rapide
    label, conf, prob = quick_classify("hamas attacks israel")
    
    # Génération rapide
    text = quick_generate("humanitarian crisis", num_words=25)
    """