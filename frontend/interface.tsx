import React, { useState, useEffect } from 'react';
import './App.css';

// ==================== Types ====================

interface Link {
  gaza_links: string[];
  ukraine_links: string[];
  total_gaza: number;
  total_ukraine: number;
}

interface ScrapingStatus {
  running: boolean;
  completed: boolean;
  error: string | null;
}

interface AnalysisStatus {
  lexical: { running: boolean; completed: boolean };
  semantic: { running: boolean; completed: boolean };
  sentiment: { running: boolean; completed: boolean };
}

// ==================== Configuration ====================

const API_URL = 'http://localhost:8000';

// ==================== Composants ====================

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
      <h1>🎯 Analyse des Biais Médiatiques</h1>
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
          <h3>📰 Scraping</h3>
          <p>Collecte automatique d'articles depuis CNN, BBC, NYT</p>
        </div>
        <div className="feature-card">
          <h3>📊 Analyse Lexicale</h3>
          <p>Fréquences, TF-IDF, Log-odds, Cooccurrences</p>
        </div>
        <div className="feature-card">
          <h3>🧠 Analyse Sémantique</h3>
          <p>Concordances, Word2Vec, Clustering</p>
        </div>
        <div className="feature-card">
          <h3>😊 Sentiment</h3>
          <p>Analyse du ton émotionnel des articles</p>
        </div>
      </div>
    </div>
  );
};

const LinksPage: React.FC = () => {
  const [links, setLinks] = useState<Link | null>(null);
  const [loading, setLoading] = useState(true);
  const [newLink, setNewLink] = useState({ corpus: 'gaza', url: '' });
  const [message, setMessage] = useState<{type: 'success' | 'error', text: string} | null>(null);

  const loadLinks = () => {
    setLoading(true);
    fetch(`${API_URL}/api/links`)
      .then(res => res.json())
      .then(data => {
        setLinks(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadLinks();
  }, []);

  const handleAddLink = () => {
    if (!newLink.url.trim()) {
      setMessage({ type: 'error', text: 'Veuillez entrer une URL' });
      return;
    }

    fetch(`${API_URL}/api/links/add?corpus=${newLink.corpus}&url=${encodeURIComponent(newLink.url)}`, {
      method: 'POST'
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setMessage({ type: 'success', text: data.message });
          setNewLink({ ...newLink, url: '' });
          loadLinks();
        } else {
          setMessage({ type: 'error', text: data.detail || 'Erreur lors de l\'ajout' });
        }
      })
      .catch(err => {
        setMessage({ type: 'error', text: err.message });
      });
  };

  const handleRemoveLink = (corpus: string, url: string) => {
    if (!confirm(`Voulez-vous vraiment supprimer ce lien ?`)) return;

    fetch(`${API_URL}/api/links/remove?corpus=${corpus}&url=${encodeURIComponent(url)}`, {
      method: 'DELETE'
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setMessage({ type: 'success', text: data.message });
          loadLinks();
        } else {
          setMessage({ type: 'error', text: data.detail || 'Erreur lors de la suppression' });
        }
      })
      .catch(err => {
        setMessage({ type: 'error', text: err.message });
      });
  };

  if (loading) return <div className="page"><p>Chargement...</p></div>;
  if (!links) return <div className="page"><p>Erreur de chargement</p></div>;

  return (
    <div className="page">
      <h1>📑 Gestion des Liens de Scraping</h1>
      
      {message && (
        <div className={`message ${message.type}`}>
          {message.text}
          <button onClick={() => setMessage(null)}>✕</button>
        </div>
      )}

      <div className="add-link-section">
        <h3>➕ Ajouter un Nouveau Lien</h3>
        <div className="add-link-form">
          <select 
            value={newLink.corpus} 
            onChange={(e) => setNewLink({ ...newLink, corpus: e.target.value })}
          >
            <option value="gaza">🇵🇸 Gaza</option>
            <option value="ukraine">🇺🇦 Ukraine</option>
          </select>
          <input 
            type="text" 
            placeholder="https://exemple.com/article"
            value={newLink.url}
            onChange={(e) => setNewLink({ ...newLink, url: e.target.value })}
            onKeyPress={(e) => e.key === 'Enter' && handleAddLink()}
          />
          <button onClick={handleAddLink} className="btn-primary">
            ➕ Ajouter
          </button>
        </div>
      </div>
      
      <div className="stats">
        <div className="stat-box">
          <h3>{links.total_gaza}</h3>
          <p>Liens Gaza</p>
        </div>
        <div className="stat-box">
          <h3>{links.total_ukraine}</h3>
          <p>Liens Ukraine</p>
        </div>
      </div>

      <div className="links-container">
        <div className="links-section">
          <h2>🇵🇸 Liens Gaza</h2>
          <div className="links-list">
            {links.gaza_links.map((link, idx) => (
              <div key={idx} className="link-item">
                <a href={link} target="_blank" rel="noopener noreferrer">
                  {link}
                </a>
                <button 
                  onClick={() => handleRemoveLink('gaza', link)}
                  className="btn-remove"
                  title="Supprimer ce lien"
                >
                  🗑️
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="links-section">
          <h2>🇺🇦 Liens Ukraine</h2>
          <div className="links-list">
            {links.ukraine_links.map((link, idx) => (
              <div key={idx} className="link-item">
                <a href={link} target="_blank" rel="noopener noreferrer">
                  {link}
                </a>
                <button 
                  onClick={() => handleRemoveLink('ukraine', link)}
                  className="btn-remove"
                  title="Supprimer ce lien"
                >
                  🗑️
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

const ScrapingPage: React.FC = () => {
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
      <h1>📚 Corpus de Textes</h1>
      
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

const LexicalAnalysisPage: React.FC = () => {
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState<'freq' | 'tfidf' | 'logodds'>('freq');

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
    fetch(`${API_URL}/api/analysis/lexical/results`)
      .then(res => res.json())
      .then(data => {
        setResults(data.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadResults();
  }, []);

  return (
    <div className="page">
      <h1>📊 Analyse Lexicale</h1>
      
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
        </>
      )}
    </div>
  );
};

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

const SentimentPage: React.FC = () => {
  return (
    <div className="page">
      <h1>😊 Analyse de Sentiment</h1>
      <div className="info-box">
        <p>⚠️ Cette section est en cours de développement</p>
        <p>Implémentez vos scripts d'analyse de sentiment et créez un endpoint dans le backend</p>
      </div>
    </div>
  );
};

// ==================== Application Principale ====================

function App() {
  const [currentPage, setCurrentPage] = useState<string>('home');

  const renderPage = () => {
    switch (currentPage) {
      case 'home': return <HomePage />;
      case 'links': return <LinksPage />;
      case 'scraping': return <ScrapingPage />;
      case 'lexical': return <LexicalAnalysisPage />;
      case 'semantic': return <SemanticAnalysisPage />;
      case 'sentiment': return <SentimentPage />;
      default: return <HomePage />;
    }
  };

  return (
    <div className="App">
      <nav className="navbar">
        <div className="nav-brand">📊 NLP Media Bias</div>
        <div className="nav-links">
          <button onClick={() => setCurrentPage('home')}>🏠 Accueil</button>
          <button onClick={() => setCurrentPage('links')}>📑 Liens</button>
          <button onClick={() => setCurrentPage('scraping')}>🔄 Scraping</button>
          <button onClick={() => setCurrentPage('lexical')}>📊 Lexical</button>
          <button onClick={() => setCurrentPage('semantic')}>🧠 Sémantique</button>
          <button onClick={() => setCurrentPage('sentiment')}>😊 Sentiment</button>
        </div>
      </nav>

      <main className="container">
        {renderPage()}
      </main>

      <footer>
        <p>Projet NLP - USTHB 2025/2026 | Master 2 HPC</p>
      </footer>
    </div>
  );
}

export default App;