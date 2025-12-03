# 📌 Répartition des Tâches — Projet NLP (Détection des biais médiatiques)

Ce document décrit clairement les responsabilités de chaque membre de l’équipe pour assurer une organisation optimale du projet.

---

## 👤 **Membre 1 — Leader d’équipe + Collecte des données**

**Responsabilités :**

* Gestion du dépôt GitHub et organisation du répertoire.
* Coordiner les réunions, planification et suivi du travail.
* Développement des scripts de scraping pour :

  * Corpus Gaza (50–100 articles)
  * Corpus Ukraine (30–50 articles)
* Nettoyage initial des données collectées (formats JSON/TXT).
* Assurer la reconstruction automatique du corpus via un script.
* Vérification de la qualité des données collectées.
* Préparation de la partie “Méthodologie de collecte” dans le rapport.

---

## 👤 **Membre 2 — Prétraitement & Pipeline NLP**

**Responsabilités :**

* Mise en place du pipeline complet de prétraitement :

  * Normalisation (lowercase, suppression ponctuation…)
  * Tokenisation
  * Stopwords
  * Lemmatisation / Stemming
* Structuration des données dans `data/processed/`.
* Création des modules réutilisables dans `src/preprocessing/`.
* Documentation du pipeline dans le rapport.
* Collaboration avec Membre 3 pour fournir des textes prêts à analyser.

---

## 👤 **Membre 3 — Analyse lexicale & sémantique**

**Analyse lexicale :**

* Calcul des fréquences de mots (Gaza vs Ukraine).
* TF-IDF comparatif.
* Analyse des bigrammes et trigrammes.
* Études des cooccurrences.
* Identification des asymétries lexicales entre :

  * Palestiniens vs Israéliens
  * Gaza vs Ukraine

**Analyse sémantique :**

* Concordance des mots clés (context windows).
* Word2Vec / FastText (si autorisé).
* Clustering des termes sémantiquement proches.
* Production des visualisations pour la partie analyse.


---

## 👤 **Membre 4 — Interface utilisateur & Visualisations**

**Responsabilités :**

* Développement du tableau de bord Streamlit (`dashboard.py`) permettant :

  * exploration des corpus
  * visualisation des figures
  * comparaison Gaza/Ukraine
  * filtres par média
* Mise en place d’un serveur backend (optionnel) avec Flask/FastAPI (`server.py`).
* Génération et mise en forme des graphiques :

  * histogrammes
  * heatmaps
  * courbes de sentiment
  * word clouds
* Intégration des résultats dans l’interface finale.
* Section du rapport : présentation de l’application.

---


