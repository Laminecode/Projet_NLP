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
          // Normalize and group clusters so the UI shows each cluster with its words
          const payload = data.data || {};
          const raw = payload.clusters || [];

          const groups: Record<string, Set<string>> = {};

          const addWord = (clusterKey: any, word: string) => {
            const key = String(clusterKey ?? '');
            if (!groups[key]) groups[key] = new Set();
            if (word && typeof word === 'string') groups[key].add(word.trim());
          };

          if (!Array.isArray(raw) && typeof raw === 'object') {
            // mapping like { '2': 'w1, w2' } or { '2': ['w1','w2'] }
            Object.entries(raw).forEach(([k, v]) => {
              if (typeof v === 'string') {
                v.split(',').map(s => s.trim()).filter(Boolean).forEach(w => addWord(k, w));
              } else if (Array.isArray(v)) {
                v.forEach(w => addWord(k, String(w)));
              }
            });
          } else if (Array.isArray(raw)) {
            raw.forEach((r: any) => {
              if (!r) return;

              // Exploded form: {cluster, word}
              if (r.cluster !== undefined && r.word !== undefined) {
                addWord(r.cluster, String(r.word));
                return;
              }

              // CSV rows: {cluster_id, keywords}
              const cid = r.cluster_id ?? r.cluster ?? r.clusterId ?? r.clusterId;
              const keywords = r.keywords ?? r.words ?? r.keyword;
              if (typeof keywords === 'string') {
                keywords.split(',').map((s: string) => s.trim()).filter(Boolean).forEach((w: string) => addWord(cid, w));
                return;
              }

              // rows like {cluster: 2, words: ['a','b']}
              if (cid !== undefined && Array.isArray(r.words)) {
                r.words.forEach((w: any) => addWord(cid, String(w)));
                return;
              }
            });
          }

          const clustered = Object.entries(groups).map(([cluster, set]) => ({
            cluster: isNaN(Number(cluster)) ? cluster : Number(cluster),
            words: Array.from(set)
          })).sort((a: any, b: any) => {
            // sort numerically when possible
            if (typeof a.cluster === 'number' && typeof b.cluster === 'number') return a.cluster - b.cluster;
            return String(a.cluster).localeCompare(String(b.cluster));
          });

          setResults({ ...payload, clusters: clustered });
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
      <h1>Analyse Sémantique</h1>
      
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
                        <li key={idx} className="concordance-item">
                          <span className="left">{item.left}</span>
                          <span className="kw"><mark>{item.keyword}</mark></span>
                          <span className="right">{item.right}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </details>
              ))
            )}
          </div>

          <div className="tables-side-by-side">
            <div className="result-section compact-table">
              <h3>Word2Vec - Mots Similaires</h3>
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

            <div className="result-section compact-table">
              <h3>Clusters Sémantiques</h3>
              {results.clusters.length === 0 ? (
                <p className="info">Aucun cluster disponible. Lancez l'analyse sémantique.</p>
              ) : (
                <div>
                  <p className="info">Affiche chaque cluster avec sa liste de termes (tous les clusters).</p>
                  <table>
                    <thead>
                      <tr><th>Cluster</th><th>Termes</th></tr>
                    </thead>
                    <tbody>
                      {results.clusters.map((c: any, idx: number) => (
                        <tr key={idx}>
                          <td><strong>Cluster {c.cluster}</strong></td>
                          <td>
                            {Array.isArray(c.words) ? (
                              <details>
                                <summary>{c.words.slice(0, 10).join(', ')}{c.words.length > 10 ? ` (+${c.words.length - 10})` : ''}</summary>
                                <ul>
                                  {c.words.map((w: string, i: number) => <li key={i}>{w}</li>)}
                                </ul>
                              </details>
                            ) : (
                              String(c.words || c.word || '')
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default SemanticAnalysisPage;