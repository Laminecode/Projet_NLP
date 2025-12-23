import React, { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000';

const LexicalAnalysisPage: React.FC = () => {
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState<'freq' | 'tfidf' | 'logodds' | 'bigrams' | 'trigrams' | 'actor'>('freq');
  const [actor, setActor] = useState<'israel' | 'palestin' | 'russia' | 'ukraine'>('israel');
  const [statType, setStatType] = useState<'context' | 'adjectives' | 'nouns' | 'verbs'>('context');
  const [actorDataGaza, setActorDataGaza] = useState<any>(null);
  const [actorDataUkraine, setActorDataUkraine] = useState<any>(null);

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

  const loadActorData = (actorToLoad: string, corpusToLoad: 'gaza' | 'ukraine') => {
    return fetch(`${API_URL}/api/analysis/lexical/actor/${actorToLoad}?corpus=${corpusToLoad}`)
      .then(r => r.json())
      .then(d => {
        if (d.status === 'success') return d.data || null;
        console.error('Erreur chargement acteur:', d);
        return null;
      })
      .catch(e => {
        console.error('Erreur fetch actor:', e);
        return null;
      });
  };

  const loadActorBoth = async (actorToLoad = actor) => {
    const [gazaData, ukrData] = await Promise.all([
      loadActorData(actorToLoad, 'gaza'),
      loadActorData(actorToLoad, 'ukraine')
    ]);
    setActorDataGaza(gazaData);
    setActorDataUkraine(ukrData);
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
            <button 
              className={tab === 'actor' ? 'active' : ''} 
              onClick={() => setTab('actor')}
            >
              Acteurs
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
                      {results.gaza_bigrams.map((item: any, idx: number) => (
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
                      {results.ukraine_bigrams.map((item: any, idx: number) => (
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
                      {results.gaza_trigrams.map((item: any, idx: number) => (
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
                      {results.ukraine_trigrams.map((item: any, idx: number) => (
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
          {tab === 'actor' && (
            <div className="result-section">
                <h3>Statistiques par Acteur</h3>
                <div style={{display: 'flex', gap: '8px', alignItems: 'center', margin: '0 auto 8px', flexWrap: 'wrap', justifyContent: 'flex-start', maxWidth: '900px'}}>
                  <label style={{fontWeight:600}}>Acteur:</label>
                  <select value={actor} onChange={(e) => setActor(e.target.value as any)}>
                    <option value="israel">Israel</option>
                    <option value="palestin">Palestin</option>
                    <option value="russia">Russia</option>
                    <option value="ukraine">Ukraine</option>
                  </select>

                  <label style={{fontWeight:600}}>Stat:</label>
                  <select value={statType} onChange={(e) => setStatType(e.target.value as any)}>
                    <option value="context">Context</option>
                    <option value="adjectives">Adjectives</option>
                    <option value="nouns">Nouns</option>
                    <option value="verbs">Verbs</option>
                  </select>

                  <button className="btn-secondary" onClick={() => loadActorBoth(actor)}>Charger</button>
                </div>

                <div style={{display: 'flex', gap: '12px'}}>
                  <div style={{flex: 1}}>
                    <h4><strong>🇵🇸 Gaza</strong></h4>
                    {actorDataGaza === null ? (
                      <p className="info">Aucun données Gaza chargées</p>
                    ) : (
                      <div>
                        {statType === 'context' && (
                          <>
                            <h5>Contexte </h5>
                            {Array.isArray(actorDataGaza.context) && actorDataGaza.context.length > 0 ? (
                              <div className="actor-table actor-table-gaza">
                                <table>
                                  <thead><tr><th>Term</th><th>Count</th></tr></thead>
                                  <tbody>
                                    {actorDataGaza.context.map((row: any, i: number) => (
                                      <tr key={i}><td>{row.token ?? row.term ?? row.left ?? ''}</td><td>{row.count ?? row.frequency ?? 0}</td></tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>
                            ) : <p className="info">Aucun contexte Gaza</p>}
                          </>
                        )}

                        {statType === 'adjectives' && (
                          <>
                            <h5>Adjectives </h5>
                            {Array.isArray(actorDataGaza.adjectives) && actorDataGaza.adjectives.length > 0 ? (
                              <div className="actor-table actor-table-gaza">
                                <table>
                                  <thead><tr><th>Token</th><th>Count</th></tr></thead>
                                  <tbody>{actorDataGaza.adjectives.map((r: any,i:number)=>(<tr key={i}><td>{r.token??r.term}</td><td>{r.count??r.frequency??0}</td></tr>))}</tbody>
                                </table>
                              </div>
                            ) : <p className="info">Aucun adjectif Gaza</p>}
                          </>
                        )}

                        {statType === 'nouns' && (
                          <>
                            <h5>Noms </h5>
                            {Array.isArray(actorDataGaza.nouns) && actorDataGaza.nouns.length > 0 ? (
                              <div className="actor-table actor-table-gaza">
                                <table>
                                  <thead><tr><th>Token</th><th>Count</th></tr></thead>
                                  <tbody>{actorDataGaza.nouns.map((r: any,i:number)=>(<tr key={i}><td>{r.token??r.term??r.word}</td><td>{r.count??r.frequency??0}</td></tr>))}</tbody>
                                </table>
                              </div>
                            ) : <p className="info">Aucun nom Gaza</p>}
                          </>
                        )}

                        {statType === 'verbs' && (
                          <>
                            <h5>Verbs </h5>
                            {Array.isArray(actorDataGaza.verbs) && actorDataGaza.verbs.length > 0 ? (
                              <div className="actor-table actor-table-gaza">
                                <table>
                                  <thead><tr><th>Token</th><th>Count</th></tr></thead>
                                  <tbody>{actorDataGaza.verbs.map((r: any,i:number)=>(<tr key={i}><td>{r.token??r.term??r.word}</td><td>{r.count??r.frequency??0}</td></tr>))}</tbody>
                                </table>
                              </div>
                            ) : <p className="info">Aucun verbe Gaza</p>}
                          </>
                        )}
                      </div>
                    )}
                  </div>

                  <div style={{flex: 1}}>
                    <h4><strong>🇺🇦 Ukraine</strong></h4>
                    {actorDataUkraine === null ? (
                      <p className="info">Aucun données Ukraine chargées</p>
                    ) : (
                      <div>
                        {statType === 'context' && (
                          <>
                            <h5>Contexte </h5>
                            {Array.isArray(actorDataUkraine.context) && actorDataUkraine.context.length > 0 ? (
                              <div className="actor-table actor-table-ukraine">
                                <table>
                                  <thead><tr><th>Term</th><th>Count</th></tr></thead>
                                  <tbody>
                                    {actorDataUkraine.context.map((row: any, i: number) => (
                                      <tr key={i}><td>{row.token ?? row.term ?? row.left ?? ''}</td><td>{row.count ?? row.frequency ?? 0}</td></tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>
                            ) : <p className="info">Aucun contexte Ukraine</p>}
                          </>
                        )}

                        {statType === 'adjectives' && (
                          <>
                            <h5>Adjectives </h5>
                            {Array.isArray(actorDataUkraine.adjectives) && actorDataUkraine.adjectives.length > 0 ? (
                              <div className="actor-table actor-table-ukraine">
                                <table>
                                  <thead><tr><th>Token</th><th>Count</th></tr></thead>
                                  <tbody>{actorDataUkraine.adjectives.map((r: any,i:number)=>(<tr key={i}><td>{r.token??r.term}</td><td>{r.count??r.frequency??0}</td></tr>))}</tbody>
                                </table>
                              </div>
                            ) : <p className="info">Aucun adjectif Ukraine</p>}
                          </>
                        )}

                        {statType === 'nouns' && (
                          <>
                            <h5>Noms </h5>
                            {Array.isArray(actorDataUkraine.nouns) && actorDataUkraine.nouns.length > 0 ? (
                              <div className="actor-table actor-table-ukraine">
                                <table>
                                  <thead><tr><th>Token</th><th>Count</th></tr></thead>
                                  <tbody>{actorDataUkraine.nouns.map((r: any,i:number)=>(<tr key={i}><td>{r.token??r.term??r.word}</td><td>{r.count??r.frequency??0}</td></tr>))}</tbody>
                                </table>
                              </div>
                            ) : <p className="info">Aucun nom Ukraine</p>}
                          </>
                        )}

                        {statType === 'verbs' && (
                          <>
                            <h5>Verbs </h5>
                            {Array.isArray(actorDataUkraine.verbs) && actorDataUkraine.verbs.length > 0 ? (
                              <div className="actor-table actor-table-ukraine">
                                <table>
                                  <thead><tr><th>Token</th><th>Count</th></tr></thead>
                                  <tbody>{actorDataUkraine.verbs.map((r: any,i:number)=>(<tr key={i}><td>{r.token??r.term??r.word}</td><td>{r.count??r.frequency??0}</td></tr>))}</tbody>
                                </table>
                              </div>
                            ) : <p className="info">Aucun verbe Ukraine</p>}
                          </>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
          )}
        </>
      )}
    </div>
  );
};

export default LexicalAnalysisPage;