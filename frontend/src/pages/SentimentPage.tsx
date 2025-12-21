import React, { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000';

const SentimentPage: React.FC = () => {
  const [results, setResults] = useState<any>(null);
  const [corpus, setCorpus] = useState<'gaza' | 'ukraine'>('gaza');
  const [loading, setLoading] = useState(false);
  const [analysisRunning, setAnalysisRunning] = useState(false);

  const startAnalysis = () => {
    setAnalysisRunning(true);
    fetch(`${API_URL}/api/analysis/sentiment/start`, { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
        setTimeout(() => {
          loadResults();
          setAnalysisRunning(false);
        }, 5000);
      })
      .catch(err => {
        alert('Erreur: ' + err.message);
        setAnalysisRunning(false);
      });
  };

  const loadResults = () => {
    setLoading(true);
    fetch(`${API_URL}/api/analysis/sentiment/results?corpus=${corpus}`)
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setResults(data.data);
        } else {
          console.error('Erreur lors du chargement:', data);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error('Erreur de chargement:', err);
        setLoading(false);
        setResults({
          victims: [],
          actors: []
        });
      });
  };

  useEffect(() => {
    loadResults();
  }, [corpus]);

  const getSentimentColor = (score: number) => {
    if (score >= 0.05) return 'positive';
    if (score <= -0.05) return 'negative';
    return 'neutral';
  };

  const getSentimentLabel = (score: number) => {
    if (score >= 0.05) return '😊 Positif';
    if (score <= -0.05) return '😞 Négatif';
    return '😐 Neutre';
  };

  const extractVictimScore = (item: any) => {
    const raw = item.compound ?? item.score ?? item.sentiment ?? 0;
    const num = typeof raw === 'string' ? parseFloat(raw) : raw;
    return Number.isNaN(num) ? 0 : num;
  };

  const extractActorScore = (item: any) => {
    const raw = item.mean_score ?? item.avg_sentiment ?? item.mean ?? 0;
    const num = typeof raw === 'string' ? parseFloat(raw) : raw;
    return Number.isNaN(num) ? 0 : num;
  };

  return (
    <div className="page">
      <h1>😊 Analyse de Sentiment</h1>
      
      <div className="control-panel">
        <button 
          onClick={startAnalysis} 
          className="btn-primary"
          disabled={analysisRunning}
        >
          {analysisRunning ? '⏳ Analyse en cours...' : '▶️ Lancer l\'Analyse'}
        </button>
        <select value={corpus} onChange={(e) => setCorpus(e.target.value as 'gaza' | 'ukraine')}>
          <option value="gaza">🇵🇸 Gaza</option>
          <option value="ukraine">🇺🇦 Ukraine</option>
        </select>
        <button onClick={loadResults} className="btn-secondary" disabled={loading}>
          {loading ? '⏳ Chargement...' : '🔄 Actualiser'}
        </button>
      </div>

      {analysisRunning && (
        <div className="status-panel">
          <p className="info">⏳ Analyse de sentiment en cours pour Gaza et Ukraine...</p>
        </div>
      )}

      {loading && <p className="info">⏳ Chargement des résultats...</p>}

      {results && !loading && (
        <>
          <div className="result-section">
            <h3>👥 Sentiment envers les Victimes - {corpus === 'gaza' ? 'Gaza 🇵🇸' : 'Ukraine 🇺🇦'}</h3>
            {results.victims.length === 0 ? (
              <p className="info">Aucune donnée disponible. Lancez l'analyse de sentiment.</p>
            ) : (
              <>
                <p className="info">
                  Analyse du sentiment dans les contextes mentionnant les victimes civiles.
                  Score positif = empathie, Score négatif = déshumanisation
                </p>
                <table>
                  <thead>
                    <tr>
                      <th>Article</th>
                      <th>Contexte</th>
                      <th>Score</th>
                      <th>Sentiment</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.victims.slice(0, 20).map((item: any, idx: number) => (
                      <tr key={idx}>
                        <td>{item.doc_id || item.article_id || `Article ${idx + 1}`}</td>
                        <td className="context-text">
                          {(item.segment || item.context || item.text || 'N/A').toString().substring(0, 100)}...
                        </td>
                        <td className={getSentimentColor(extractVictimScore(item))}>
                          {extractVictimScore(item).toFixed(3)}
                        </td>
                        <td>{getSentimentLabel(extractVictimScore(item))}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </>
            )}
          </div>

          <div className="result-section">
            <h3>🎭 Sentiment par Acteur - {corpus === 'gaza' ? 'Gaza 🇵🇸' : 'Ukraine 🇺🇦'}</h3>
            {results.actors.length === 0 ? (
              <p className="info">Aucune donnée disponible. Lancez l'analyse de sentiment.</p>
            ) : (
              <>
                <p className="info">
                  Analyse du ton utilisé pour décrire chaque acteur du conflit.
                </p>
                <table>
                  <thead>
                    <tr>
                      <th>Acteur</th>
                      <th>Score Moyen</th>
                      <th>Sentiment</th>
                      <th>Occurrences</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.actors.slice(0, 30).map((item: any, idx: number) => (
                      <tr key={idx}>
                        <td><strong>{item.actor || item.entity || 'N/A'}</strong></td>
                        
                        <td className={getSentimentColor(extractActorScore(item))}>
                          {extractActorScore(item).toFixed(3)}
                        </td>
                        <td>{getSentimentLabel(extractActorScore(item))}</td>
                        <td>{item.count || item.occurrences || 1}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </>
            )}
          </div>

          {results.victims.length > 0 && results.actors.length > 0 && (
            <div className="result-section full-width">
              <h3>📊 Statistiques Globales</h3>
              <div className="stats-grid">
                <div className="stat-card">
                  <h4>Victimes</h4>
                  <p>Sentiment moyen: <strong className={getSentimentColor(
                    results.victims.reduce((acc: number, item: any) => 
                      acc + extractVictimScore(item), 0) / results.victims.length
                  )}>
                    {(results.victims.reduce((acc: number, item: any) => 
                      acc + extractVictimScore(item), 0) / results.victims.length).toFixed(3)}
                  </strong></p>
                  <p>Contextes analysés: {results.victims.length}</p>
                </div>
                <div className="stat-card">
                  <h4>Acteurs</h4>
                  <p>Acteurs identifiés: {results.actors.length}</p>
                  <p>Contextes totaux: {results.actors.reduce((acc: number, item: any) => 
                    acc + (item.count || item.occurrences || 1), 0)}</p>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default SentimentPage;