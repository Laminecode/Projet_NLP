import React, { useState } from 'react';
import './App.css';
import HomePage from './pages/HomePage';
import LinksPage from './pages/LinksPage';
import CorpusPage from './pages/CorpusPage';
import LexicalAnalysisPage from './pages/LexicalPage';
import SemanticAnalysisPage from './pages/SemanticPage';
import SentimentPage from './pages/SentimentPage';

function App() {
  const [currentPage, setCurrentPage] = useState<string>('home');

  const renderPage = () => {
    switch (currentPage) {
      case 'home': return <HomePage />;
      case 'links': return <LinksPage />;
      case 'scraping': return <CorpusPage />;
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
          <button onClick={() => setCurrentPage('scraping')}>📚 Corpus</button>
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