import React, { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000';

const HomePage: React.FC = () => {
  const [serverStatus, setServerStatus] = useState<string>('Vérification...');

  useEffect(() => {
    fetch(`${API_URL}/`)
      .then(res => res.json())
      .then(data => setServerStatus(data.message))
      .catch(() => setServerStatus('Serveur non disponible'));
  }, []);

  return (
    <div className="page">
      <h1> Analyse des Biais Médiatiques</h1>
      <div className="hero">
        <h2>Gaza vs Ukraine - Couverture Médiatique</h2>
        <p>
          Ce projet utilise le traitement automatique du langage naturel (NLP) pour
          analyser et comparer la couverture médiatique occidentale de deux conflits majeurs.
        </p>
        <div className="status-card">
          <strong>Statut du serveur:</strong>
          <p className={serverStatus.includes('opérationnel') ? 'success' : 'error'}>
            {serverStatus}
          </p>
        </div>
      </div>

      <div className="features">
        <div className="feature-card">
          <h3> Scraping</h3>
          <p>Collecte automatique d'articles depuis CNN, BBC, NYT</p>
        </div>
        <div className="feature-card">
          <h3>Analyse Lexicale</h3>
          <p>Fréquences, TF-IDF, Log-odds, Cooccurrences</p>
        </div>
        <div className="feature-card">
          <h3> Analyse Sémantique</h3>
          <p>Concordances, Word2Vec, Clustering</p>
        </div>
        <div className="feature-card">
          <h3>Sentiment</h3>
          <p>Analyse du ton émotionnel des articles</p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;