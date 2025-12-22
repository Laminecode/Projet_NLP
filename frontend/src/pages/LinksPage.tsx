import React, { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000';

interface Link {
  gaza_links: string[];
  ukraine_links: string[];
  total_gaza: number;
  total_ukraine: number;
}

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
      <h1>Gestion des Liens de Scraping</h1>
      
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

export default LinksPage;