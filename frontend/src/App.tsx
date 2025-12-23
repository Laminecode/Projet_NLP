import React, { useState } from 'react';
import './App.css';
import {
  Home,
  FileText,
  Book,
  BarChart3,
  Search,
  MessageSquare,
} from 'lucide-react';

import HomePage from './pages/HomePage';
import LinksPage from './pages/LinksPage';
import CorpusPage from './pages/CorpusPage';
import LexicalAnalysisPage from './pages/LexicalPage';
import SemanticAnalysisPage from './pages/SemanticPage';
import SentimentPage from './pages/SentimentPage';

const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<
    'home' | 'links' | 'scraping' | 'lexical' | 'semantic' | 'sentiment'
  >('home');

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage />;
      case 'links':
        return <LinksPage />;
      case 'scraping':
        return <CorpusPage />;
      case 'lexical':
        return <LexicalAnalysisPage />;
      case 'semantic':
        return <SemanticAnalysisPage />;
      case 'sentiment':
        return <SentimentPage />;
      default:
        return <HomePage />;
    }
  };

  return (
    <div className="App">
      {/* ===== NAVBAR ===== */}
      <nav className="navbar">
        <div className="nav-brand">📊 NLP Media Bias</div>

        <div className="nav-links">
          <button
            className={`nav-btn ${currentPage === 'home' ? 'active' : ''}`}
            onClick={() => setCurrentPage('home')}
          >
            <Home size={20} className="icon" />
            Accueil
          </button>

          <button
            className={`nav-btn ${currentPage === 'links' ? 'active' : ''}`}
            onClick={() => setCurrentPage('links')}
          >
            <FileText size={20} className="icon" />
            Liens
          </button>

          <button
            className={`nav-btn ${currentPage === 'scraping' ? 'active' : ''}`}
            onClick={() => setCurrentPage('scraping')}
          >
            <Book size={20} className="icon" />
            Corpus
          </button>

          <button
            className={`nav-btn ${currentPage === 'lexical' ? 'active' : ''}`}
            onClick={() => setCurrentPage('lexical')}
          >
            <BarChart3 size={20} className="icon" />
            Lexical
          </button>

          <button
            className={`nav-btn ${currentPage === 'semantic' ? 'active' : ''}`}
            onClick={() => setCurrentPage('semantic')}
          >
            <Search size={20} className="icon" />
            Sémantique
          </button>

          <button
            className={`nav-btn ${currentPage === 'sentiment' ? 'active' : ''}`}
            onClick={() => setCurrentPage('sentiment')}
          >
            <MessageSquare size={20} className="icon" />
            Sentiment
          </button>
        </div>
      </nav>

      {/* ===== CONTENT ===== */}
      <main className="container">{renderPage()}</main>

      {/* ===== FOOTER ===== */}
      <footer>
        <p>Projet NLP - USTHB 2025/2026 | Master 2 HPC</p>
      </footer>
    </div>
  );
};

export default App;
