import React, { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000';

interface ScrapingStatus {
  running: boolean;
  completed: boolean;
  error: string | null;
}

const CorpusPage: React.FC = () => {
  const [status, setStatus] = useState<ScrapingStatus>({
    running: false,
    completed: false,
    error: null
  });
  const [corpusData, setCorpusData] = useState<any>(null);
  const [selectedCorpus, setSelectedCorpus] = useState<'gaza' | 'ukraine'>('gaza');
  const [loading, setLoading] = useState(false);

  const checkStatus = () => {
    fetch(`${API_URL}/api/scraping/status`)
      .then(res => res.json())
      .then(data => setStatus(data.data))
      .catch(err => console.error(err));
  };

  const loadCorpusTexts = (corpus: 'gaza' | 'ukraine') => {
    setLoading(true);
    fetch(`${API_URL}/api/corpus/texts?corpus=${corpus}&limit=20`)
      .then(res => res.json())
      .then(data => {
        setCorpusData(data.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    checkStatus();
    loadCorpusTexts(selectedCorpus);
    const interval = setInterval(checkStatus, 3000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    loadCorpusTexts(selectedCorpus);
  }, [selectedCorpus]);

  const startScraping = () => {
    fetch(`${API_URL}/api/scraping/start`, { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
        checkStatus();
        setTimeout(() => loadCorpusTexts(selectedCorpus), 5000);
      })
      .catch(err => alert('Erreur: ' + err.message));
  };

  return (
    <div className="page">
      <h1> Corpus de Textes</h1>
      
      <div className="control-panel">
        <button 
          onClick={startScraping} 
          disabled={status.running}
          className="btn-primary"
        >
          {status.running ? '⏳ Scraping en cours...' : '▶️ Démarrer le Scraping'}
        </button>
        
        <select 
          value={selectedCorpus} 
          onChange={(e) => setSelectedCorpus(e.target.value as 'gaza' | 'ukraine')}
        >
          <option value="gaza">🇵🇸 Corpus Gaza</option>
          <option value="ukraine">🇺🇦 Corpus Ukraine</option>
        </select>
        
        <button onClick={() => loadCorpusTexts(selectedCorpus)} className="btn-secondary">
          🔄 Actualiser
        </button>
      </div>

      <div className="status-panel">
        <h3>Statut du Scraping:</h3>
        {status.running && <p className="info">⏳ Scraping en cours...</p>}
        {status.completed && !status.running && <p className="success">✅ Scraping terminé</p>}
        {status.error && <p className="error">❌ Erreur: {status.error}</p>}
      </div>

      {loading && <p className="info">⏳ Chargement du corpus...</p>}

      {corpusData && !loading && (
        <>
          <div className="corpus-stats">
            <div className="stat-box">
              <h3>{corpusData.total}</h3>
              <p>Articles Total</p>
            </div>
            <div className="stat-box">
              <h3>{corpusData.showing}</h3>
              <p>Affichés</p>
            </div>
          </div>

          <div className="corpus-list">
            <h3>📄 Articles du Corpus {selectedCorpus === 'gaza' ? 'Gaza 🇵🇸' : 'Ukraine 🇺🇦'}</h3>
            {corpusData.texts.length === 0 ? (
              <p className="info">Aucun article trouvé. Lancez le scraping pour collecter des articles.</p>
            ) : (
              corpusData.texts.map((text: any, idx: number) => (
                <div key={idx} className="corpus-item">
                  <div className="corpus-header">
                    <strong>📄 {text.filename}</strong>
                    <span className="word-count">{text.word_count} mots</span>
                  </div>
                  <div className="corpus-preview">
                    {text.preview}
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default CorpusPage;