import React, { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000';

const LexicalAnalysisPage: React.FC = () => {
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState<'freq' | 'tfidf' | 'logodds' | 'bigrams' | 'trigrams'>('freq');

  const startAnalysis = () => {
    setLoading(true);
    fetch(`${API_URL}/api/analysis/lexical/start`, { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
        setTimeout(loadResults, 3000);
      })
      .catch(err => {
        alert('Erreur: ' + err.message);
        setLoading(false);
      });
  };

  const loadResults = () => {
    setLoading(true);
    // Récupère les résultats principaux puis bigrams/trigrams pour Gaza et Ukraine
    Promise.all([
      fetch(`${API_URL}/api/analysis/lexical/results`).then(r => r.json()),
      fetch(`${API_URL}/api/analysis/lexical/bigrams?corpus=gaza`).then(r => r.json()),
      fetch(`${API_URL}/api/analysis/lexical/bigrams?corpus=ukraine`).then(r => r.json()),
      fetch(`${API_URL}/api/analysis/lexical/trigrams?corpus=gaza`).then(r => r.json()),
      fetch(`${API_URL}/api/analysis/lexical/trigrams?corpus=ukraine`).then(r => r.json())
    ]).then(([mainRes, gazaBig, ukrBig, gazaTri, ukrTri]) => {
      const mainData = mainRes.data || {};
      // Attacher les n-grams
      mainData.gaza_bigrams = (gazaBig.data) || [];
      mainData.ukraine_bigrams = (ukrBig.data) || [];
      mainData.gaza_trigrams = (gazaTri.data) || [];
      mainData.ukraine_trigrams = (ukrTri.data) || [];
      setResults(mainData);
      setLoading(false);
    }).catch(err => {
      console.error('Erreur loadResults:', err);
      setLoading(false);
    });
  };

  useEffect(() => {
    loadResults();
  }, []);

  return (
    <div className="page">
      <h1> Analyse Lexicale</h1>
      
      <div className="control-panel">
        <button onClick={startAnalysis} className="btn-primary">
          ▶️ Lancer l'Analyse
        </button>
        <button onClick={loadResults} className="btn-secondary">
          🔄 Actualiser
        </button>
      </div>

      {loading && <p>⏳ Chargement...</p>}

      {results && (
        <>
          <div className="tabs">
            <button 
              className={tab === 'freq' ? 'active' : ''} 
              onClick={() => setTab('freq')}
            >
              Fréquences
            </button>
            <button 
              className={tab === 'tfidf' ? 'active' : ''} 
              onClick={() => setTab('tfidf')}
            >
              TF-IDF
            </button>
            <button 
              className={tab === 'logodds' ? 'active' : ''} 
              onClick={() => setTab('logodds')}
            >
              Log-Odds
            </button>
            <button 
              className={tab === 'bigrams' ? 'active' : ''} 
              onClick={() => setTab('bigrams')}
            >
              Bigrams
            </button>
            <button 
              className={tab === 'trigrams' ? 'active' : ''} 
              onClick={() => setTab('trigrams')}
            >
              Trigrams
            </button>
          </div>

          {tab === 'freq' && (
            <div className="results-grid">
              <div className="result-section">
                <h3>🇵🇸 Fréquences Gaza</h3>
                {results.gaza_wordfreq.length === 0 ? (
                  <p className="info">Aucune donnée disponible. Lancez l'analyse lexicale.</p>
                ) : (
                  <table>
                    <thead>
                      <tr><th>Terme</th><th>Fréquence</th></tr>
                    </thead>
                    <tbody>
                      {results.gaza_wordfreq.slice(0, 20).map((item: any, idx: number) => (
                        <tr key={idx}>
                          <td>{item.term || item.word || '-'}</td>
                          <td>{item.count || item.frequency || 0}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>

              <div className="result-section">
                <h3>🇺🇦 Fréquences Ukraine</h3>
                {results.ukraine_wordfreq.length === 0 ? (
                  <p className="info">Aucune donnée disponible. Lancez l'analyse lexicale.</p>
                ) : (
                  <table>
                    <thead>
                      <tr><th>Terme</th><th>Fréquence</th></tr>
                    </thead>
                    <tbody>
                      {results.ukraine_wordfreq.slice(0, 20).map((item: any, idx: number) => (
                        <tr key={idx}>
                          <td>{item.term || item.word || '-'}</td>
                          <td>{item.count || item.frequency || 0}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </div>
          )}

          {tab === 'tfidf' && (
            <div className="results-grid">
              <div className="result-section">
                <h3>🇵🇸 TF-IDF Gaza</h3>
                <table>
                  <thead>
                    <tr><th>Terme</th><th>Score</th></tr>
                  </thead>
                  <tbody>
                    {results.tfidf_gaza.slice(0, 20).map((item: any, idx: number) => (
                      <tr key={idx}>
                        <td>{item.term}</td>
                        <td>{item.score?.toFixed(4)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="result-section">
                <h3>🇺🇦 TF-IDF Ukraine</h3>
                <table>
                  <thead>
                    <tr><th>Terme</th><th>Score</th></tr>
                  </thead>
                  <tbody>
                    {results.tfidf_ukraine.slice(0, 20).map((item: any, idx: number) => (
                      <tr key={idx}>
                        <td>{item.term}</td>
                        <td>{item.score?.toFixed(4)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {tab === 'logodds' && (
            <div className="result-section full-width">
              <h3>⚖️ Log-Odds Ratio (Gaza vs Ukraine)</h3>
              <p className="info">Termes plus fréquents à Gaza (score positif) vs Ukraine (score négatif)</p>
              <table>
                <thead>
                  <tr>
                    <th>Terme</th>
                    <th>Gaza</th>
                    <th>Ukraine</th>
                    <th>Log-Odds</th>
                    <th>Z-Score</th>
                  </tr>
                </thead>
                <tbody>
                  {results.logodds_top.slice(0, 30).map((item: any, idx: number) => (
                    <tr key={idx}>
                      <td><strong>{item.term}</strong></td>
                      <td>{item.count_a}</td>
                      <td>{item.count_b}</td>
                      <td className={item.logodds > 0 ? 'positive' : 'negative'}>
                        {item.logodds?.toFixed(3)}
                      </td>
                      <td>{item.z?.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {tab === 'bigrams' && (
            <div className="results-grid">
              <div className="result-section">
                <h3>🇵🇸 Bigrams Gaza</h3>
                {(!results.gaza_bigrams || results.gaza_bigrams.length === 0) ? (
                  <p className="info">Aucune donnée disponible. Lancez l'analyse lexicale.</p>
                ) : (
                  <table>
                    <thead>
                      <tr><th>Bigram</th><th>Count</th></tr>
                    </thead>
                    <tbody>
                      {results.gaza_bigrams.slice(0, 30).map((item: any, idx: number) => (
                        <tr key={idx}>
                          <td>{item.term || item["term"] || item.word || '-'}</td>
                          <td>{item.count ?? item.count_a ?? item.count_b ?? 0}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>

              <div className="result-section">
                <h3>🇺🇦 Bigrams Ukraine</h3>
                {(!results.ukraine_bigrams || results.ukraine_bigrams.length === 0) ? (
                  <p className="info">Aucune donnée disponible. Lancez l'analyse lexicale.</p>
                ) : (
                  <table>
                    <thead>
                      <tr><th>Bigram</th><th>Count</th></tr>
                    </thead>
                    <tbody>
                      {results.ukraine_bigrams.slice(0, 30).map((item: any, idx: number) => (
                        <tr key={idx}>
                          <td>{item.term || item["term"] || item.word || '-'}</td>
                          <td>{item.count ?? item.count_a ?? item.count_b ?? 0}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </div>
          )}

          {tab === 'trigrams' && (
            <div className="results-grid">
              <div className="result-section">
                <h3>🇵🇸 Trigrams Gaza</h3>
                {(!results.gaza_trigrams || results.gaza_trigrams.length === 0) ? (
                  <p className="info">Aucune donnée disponible. Lancez l'analyse lexicale.</p>
                ) : (
                  <table>
                    <thead>
                      <tr><th>Trigram</th><th>Count</th></tr>
                    </thead>
                    <tbody>
                      {results.gaza_trigrams.slice(0, 30).map((item: any, idx: number) => (
                        <tr key={idx}>
                          <td>{item.term || item["term"] || item.word || '-'}</td>
                          <td>{item.count ?? 0}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>

              <div className="result-section">
                <h3>🇺🇦 Trigrams Ukraine</h3>
                {(!results.ukraine_trigrams || results.ukraine_trigrams.length === 0) ? (
                  <p className="info">Aucune donnée disponible. Lancez l'analyse lexicale.</p>
                ) : (
                  <table>
                    <thead>
                      <tr><th>Trigram</th><th>Count</th></tr>
                    </thead>
                    <tbody>
                      {results.ukraine_trigrams.slice(0, 30).map((item: any, idx: number) => (
                        <tr key={idx}>
                          <td>{item.term || item["term"] || item.word || '-'}</td>
                          <td>{item.count ?? 0}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default LexicalAnalysisPage;