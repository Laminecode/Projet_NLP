import React, { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000';

const SemanticAnalysisPage: React.FC = () => {
  const [results, setResults] = useState<any>(null);
  const [corpus, setCorpus] = useState<'gaza' | 'ukraine'>('gaza');
  const [loading, setLoading] = useState(false);
  const [analysisRunning, setAnalysisRunning] = useState(false);

  const startAnalysis = () => {
    setAnalysisRunning(true);
    fetch(`${API_URL}/api/analysis/semantic/start`, { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
        // Attendre un peu puis recharger les résultats pour les deux corpus
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
    fetch(`${API_URL}/api/analysis/semantic/results?corpus=${corpus}`)
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
        // Créer des données vides pour éviter les erreurs
        setResults({
          concordances: {},
          word2vec_neighbors: [],
          clusters: []
        });
      });
  };

  useEffect(() => {
    loadResults();
  }, [corpus]);

  return (
    <div className="page">
      <h1>🧠 Analyse Sémantique</h1>
      
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
          <p className="info">⏳ Analyse sémantique en cours pour Gaza et Ukraine...</p>
        </div>
      )}

      {loading && <p className="info">⏳ Chargement des résultats...</p>}

      {results && !loading && (
        <>
          <div className="result-section">
            <h3>🔍 Concordances - {corpus === 'gaza' ? 'Gaza 🇵🇸' : 'Ukraine 🇺🇦'}</h3>
            <p>Contextes d'utilisation des mots-clés</p>
            {Object.keys(results.concordances).length === 0 ? (
              <p className="info">Aucune concordance disponible. Lancez l'analyse sémantique.</p>
            ) : (
              Object.entries(results.concordances).map(([keyword, items]: [string, any]) => (
                <details key={keyword}>
                  <summary><strong>{keyword}</strong> ({items.length} occurrences)</summary>
                  {items.length === 0 ? (
                    <p className="info">Aucune occurrence trouvée</p>
                  ) : (
                    <ul className="concordance-list">
                      {items.slice(0, 10).map((item: any, idx: number) => (
                        <li key={idx}>
                          {item.left} <mark>{item.keyword}</mark> {item.right}
                        </li>
                      ))}
                    </ul>
                  )}
                </details>
              ))
            )}
          </div>

          <div className="result-section">
            <h3>🤝 Word2Vec - Mots Similaires</h3>
            {results.word2vec_neighbors.length === 0 ? (
              <p className="info">Aucune donnée Word2Vec disponible. Lancez l'analyse sémantique.</p>
            ) : (
              <table>
                <thead>
                  <tr><th>Acteur</th><th>Voisin</th><th>Similarité</th></tr>
                </thead>
                <tbody>
                  {results.word2vec_neighbors.slice(0, 30).map((item: any, idx: number) => (
                    <tr key={idx}>
                      <td><strong>{item.actor}</strong></td>
                      <td>{item.neighbor}</td>
                      <td>{item.similarity?.toFixed(3) || 'N/A'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          <div className="result-section">
            <h3>🗂️ Clusters Sémantiques</h3>
            {results.clusters.length === 0 ? (
              <p className="info">Aucun cluster disponible. Lancez l'analyse sémantique.</p>
            ) : (
              <table>
                <thead>
                  <tr><th>Cluster</th><th>Terme</th></tr>
                </thead>
                <tbody>
                  {results.clusters.slice(0, 50).map((item: any, idx: number) => (
                    <tr key={idx}>
                      <td>Cluster {item.cluster}</td>
                      <td>{item.word}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default SemanticAnalysisPage;