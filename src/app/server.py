
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import os
import sys
import json
from pathlib import Path
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.scraping.build_corpus import main as build_corpus_main
from src.preprocessing.clean_corpus import main as clean_corpus_main
from src.lexicale_analysis.compare_corpora import run_all as run_lexical_analysis
from src.semantic_analysis.run_semantic import run_semantic

app = FastAPI(
    title="NLP Media Bias Analysis API",
    description="API pour l'analyse des biais médiatiques Gaza vs Ukraine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite et React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Modèles Pydantic ====================

class StatusResponse(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None

class LinksResponse(BaseModel):
    gaza_links: List[str]
    ukraine_links: List[str]
    total_gaza: int
    total_ukraine: int

# ==================== Variables globales ====================

SCRAPING_STATUS = {"running": False, "completed": False, "error": None}
ANALYSIS_STATUS = {
    "lexical": {"running": False, "completed": False},
    "semantic": {"running": False, "completed": False},
    "sentiment": {"running": False, "completed": False}
}

# ==================== Fonctions utilitaires ====================

def read_links_file(filepath: str) -> List[str]:
    try:
        if not os.path.exists(filepath):
            return []
        with open(filepath, 'r', encoding='utf-8') as f:
            links = [line.strip() for line in f if line.strip()]
        return links
    except Exception as e:
        print(f"Erreur lecture {filepath}: {e}")
        return []

def read_csv_to_dict(filepath: str) -> List[Dict]:
    try:
        if not os.path.exists(filepath):
            return []
        df = pd.read_csv(filepath)
        return df.head(100).to_dict('records')  # Limite à 100 lignes pour la performance
    except Exception as e:
        print(f"Erreur lecture CSV {filepath}: {e}")
        return []

def read_freq_csv(filepath: str) -> List[Dict]:
    """Lit un CSV de fréquence et normalise les colonnes 'term' et 'count'"""
    try:
        if not os.path.exists(filepath):
            return []
        df = pd.read_csv(filepath)
        records = []
        # parcourir les lignes et normaliser
        for _, row in df.head(100).iterrows():
            term = None
            count = None
            for c in ['word', 'term', 'token']:
                if c in row.index and pd.notna(row[c]):
                    term = str(row[c])
                    break
            for c in ['count', 'frequency', 'freq']:
                if c in row.index and pd.notna(row[c]):
                    try:
                        count = int(row[c])
                    except Exception:
                        try:
                            count = int(float(row[c]))
                        except Exception:
                            count = row[c]
                    break
            records.append({'term': term or '', 'count': count or 0})
        return records
    except Exception as e:
        print(f"Erreur lecture CSV fréquence {filepath}: {e}")
        return []

def read_json_file(filepath: str) -> Dict:
    try:
        if not os.path.exists(filepath):
            return {}
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lecture JSON {filepath}: {e}")
        return {}

# ==================== Endpoints ====================

@app.get("/", response_model=StatusResponse)
async def root():
    return StatusResponse(
        status="success",
        message="API NLP Media Bias Analysis - Serveur opérationnel",
        data={"version": "1.0.0"}
    )

@app.get("/api/links", response_model=LinksResponse)
async def get_links():
    gaza_links = read_links_file("data/gaza_links.txt")
    ukraine_links = read_links_file("data/ukraine_links.txt")
    
    return LinksResponse(
        gaza_links=gaza_links,
        ukraine_links=ukraine_links,
        total_gaza=len(gaza_links),
        total_ukraine=len(ukraine_links)
    )

@app.post("/api/links/add")
async def add_link(corpus: str, url: str):
    if corpus not in ["gaza", "ukraine"]:
        raise HTTPException(status_code=400, detail="Corpus invalide. Utilisez 'gaza' ou 'ukraine'")
    
    filepath = f"data/{corpus}_links.txt"
    
    try:
        existing_links = read_links_file(filepath)
        if url in existing_links:
            raise HTTPException(status_code=400, detail="Ce lien existe déjà")
        
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(url + '\n')
        
        return {"status": "success", "message": f"Lien ajouté à {corpus}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/links/remove")
async def remove_link(corpus: str, url: str):
    if corpus not in ["gaza", "ukraine"]:
        raise HTTPException(status_code=400, detail="Corpus invalide. Utilisez 'gaza' ou 'ukraine'")
    
    filepath = f"data/{corpus}_links.txt"
    
    try:
        links = read_links_file(filepath)
        if url not in links:
            raise HTTPException(status_code=404, detail="Lien non trouvé")
        
        links.remove(url)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for link in links:
                f.write(link + '\n')
        
        return {"status": "success", "message": f"Lien supprimé de {corpus}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scraping/status")
async def get_scraping_status():
    return {
        "status": "success",
        "data": SCRAPING_STATUS
    }

async def run_scraping_task():
    global SCRAPING_STATUS
    try:
        SCRAPING_STATUS["running"] = True
        SCRAPING_STATUS["error"] = None
        
        # Étape 1: Scraping
        print("[BACKEND] Démarrage du scraping...")
        build_corpus_main()
        
        # Étape 2: Preprocessing
        print("[BACKEND] Démarrage du preprocessing...")
        clean_corpus_main()
        
        SCRAPING_STATUS["running"] = False
        SCRAPING_STATUS["completed"] = True
        print("[BACKEND] Scraping et preprocessing terminés avec succès")
        
    except Exception as e:
        SCRAPING_STATUS["running"] = False
        SCRAPING_STATUS["error"] = str(e)
        print(f"[BACKEND ERROR] Scraping échoué: {e}")

@app.post("/api/scraping/start")
async def start_scraping(background_tasks: BackgroundTasks):
    #Lance le scraping et le preprocessing en arrière-plan
    if SCRAPING_STATUS["running"]:
        raise HTTPException(status_code=400, detail="Le scraping est déjà en cours")
    
    background_tasks.add_task(run_scraping_task)
    
    return {
        "status": "success",
        "message": "Scraping démarré en arrière-plan"
    }

@app.get("/api/corpus/texts")
async def get_corpus_texts(corpus: str = "gaza", limit: int = 10, offset: int = 0):
    if corpus not in ["gaza", "ukraine"]:
        raise HTTPException(status_code=400, detail="Corpus invalide")
    
    corpus_dir = f"data/raw_text/{corpus}"
    
    if not os.path.exists(corpus_dir):
        return {"status": "success", "data": {"texts": [], "total": 0}}
    
    files = [f for f in os.listdir(corpus_dir) if f.endswith('.txt') and f != '_stats.json']
    files = sorted(files)
    if offset < 0:
        offset = 0
    texts = []
    
    for i, filename in enumerate(files[offset: offset + limit]):
        try:
            with open(os.path.join(corpus_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                texts.append({
                    "id": filename.replace('.txt', ''),
                    "filename": filename,
                    "preview": content[:500] + "..." if len(content) > 500 else content,
                    "word_count": len(content.split())
                })
        except Exception as e:
            print(f"Erreur lecture {filename}: {e}")
    
    return {
        "status": "success",
        "data": {
            "texts": texts,
            "total": len(files),
            "showing": len(texts),
            "offset": offset,
            "limit": limit
        }
    }

async def run_lexical_analysis_task():
    #Tâche de fond pour l'analyse lexicale
    global ANALYSIS_STATUS
    try:
        ANALYSIS_STATUS["lexical"]["running"] = True
        print("[BACKEND] Démarrage analyse lexicale...")
        run_lexical_analysis(data_base="data/processed_clean")
        ANALYSIS_STATUS["lexical"]["running"] = False
        ANALYSIS_STATUS["lexical"]["completed"] = True
        print("[BACKEND] Analyse lexicale terminée")
    except Exception as e:
        ANALYSIS_STATUS["lexical"]["running"] = False
        print(f"[BACKEND ERROR] Analyse lexicale échouée: {e}")

@app.post("/api/analysis/lexical/start")
async def start_lexical_analysis(background_tasks: BackgroundTasks):
    if ANALYSIS_STATUS["lexical"]["running"]:
        raise HTTPException(status_code=400, detail="Analyse lexicale déjà en cours")
    
    background_tasks.add_task(run_lexical_analysis_task)
    return {"status": "success", "message": "Analyse lexicale démarrée"}

@app.get("/api/analysis/lexical/results")
async def get_lexical_results():
    def read_freq_csv(filepath):
        data = read_csv_to_dict(filepath)
        cleaned_data = []
        for item in data:
            term = item.get('word') or item.get('term') or item.get('token') or ''
            count = item.get('count') or item.get('frequency') or item.get('freq') or 0
            cleaned_data.append({"term": term, "count": count})
        return cleaned_data
    
    results = {
        "summary": read_json_file("results/statistics/summary.json"),
        "gaza_wordfreq": read_freq_csv("results/statistics/gaza_wordfreq.csv"),
        "ukraine_wordfreq": read_freq_csv("results/statistics/ukraine_wordfreq.csv"),
        "logodds_top": read_csv_to_dict("results/statistics/gaza_vs_ukraine_logodds_top200.csv"),
        "logodds_bottom": read_csv_to_dict("results/statistics/gaza_vs_ukraine_logodds_bottom200.csv"),
        "logodds_full": read_csv_to_dict("results/statistics/gaza_vs_ukraine_logodds_full.csv"),
        "tfidf_gaza": read_csv_to_dict("results/statistics/tfidf_gaza.csv"),
        "tfidf_ukraine": read_csv_to_dict("results/statistics/tfidf_ukraine.csv"),
        "article_stats": read_csv_to_dict("results/statistics/article_stats.csv")
    }

    return {"status": "success", "data": results}


@app.get("/api/analysis/lexical/bigrams")
async def get_bigrams(corpus: str = "gaza"):
    """Retourne les bigrams pour le corpus demandé (gaza|ukraine)"""
    if corpus not in ["gaza", "ukraine"]:
        raise HTTPException(status_code=400, detail="Corpus invalide. Utilisez 'gaza' ou 'ukraine'")
    path = f"results/statistics/{corpus}_bigrams.csv"
    data = read_csv_to_dict(path)
    return {"status": "success", "data": data}


@app.get("/api/analysis/lexical/trigrams")
async def get_trigrams(corpus: str = "gaza"):
    """Retourne les trigrams pour le corpus demandé (gaza|ukraine)"""
    if corpus not in ["gaza", "ukraine"]:
        raise HTTPException(status_code=400, detail="Corpus invalide. Utilisez 'gaza' ou 'ukraine'")
    path = f"results/statistics/{corpus}_trigrams.csv"
    data = read_csv_to_dict(path)
    return {"status": "success", "data": data}


@app.get("/api/analysis/lexical/tfidf")
async def get_tfidf(corpus: str = "gaza"):
    """Retourne le TF-IDF pour le corpus demandé (tfidf_gaza.csv / tfidf_ukraine.csv)"""
    if corpus not in ["gaza", "ukraine"]:
        raise HTTPException(status_code=400, detail="Corpus invalide. Utilisez 'gaza' ou 'ukraine'")
    path = f"results/statistics/tfidf_{corpus}.csv"
    data = read_csv_to_dict(path)
    return {"status": "success", "data": data}


@app.get("/api/analysis/lexical/wordfreq")
async def get_wordfreq(corpus: str = "gaza"):
    """Retourne la fréquence des mots pour le corpus demandé"""
    if corpus not in ["gaza", "ukraine"]:
        raise HTTPException(status_code=400, detail="Corpus invalide. Utilisez 'gaza' ou 'ukraine'")
    path = f"results/statistics/{corpus}_wordfreq.csv"
    data = read_freq_csv(path)
    return {"status": "success", "data": data}


@app.get("/api/analysis/lexical/logodds")
async def get_logodds(variant: str = "top200"):
    """Retourne les résultats log-odds. Paramètre 'variant' : top200|bottom200|full"""
    mapping = {
        "top200": "results/statistics/gaza_vs_ukraine_logodds_top200.csv",
        "bottom200": "results/statistics/gaza_vs_ukraine_logodds_bottom200.csv",
        "full": "results/statistics/gaza_vs_ukraine_logodds_full.csv"
    }
    if variant not in mapping:
        raise HTTPException(status_code=400, detail="Variant invalide. Choisir: top200, bottom200, full")
    path = mapping[variant]
    data = read_csv_to_dict(path)
    return {"status": "success", "data": data}

@app.get("/api/analysis/lexical/actor/{actor}")
async def get_actor_analysis(actor: str, corpus: str = "gaza"):
    context = read_csv_to_dict(f"results/statistics/{corpus}_actor_{actor}_context.csv")
    adj = read_csv_to_dict(f"results/statistics/{corpus}_actor_{actor}_ADJ.csv")
    verb = read_csv_to_dict(f"results/statistics/{corpus}_actor_{actor}_VERB.csv")
    noun = read_csv_to_dict(f"results/statistics/{corpus}_actor_{actor}_NOUN.csv")
    
    return {
        "status": "success",
        "data": {
            "context": context,
            "adjectives": adj,
            "verbs": verb,
            "nouns": noun
        }
    }

async def run_semantic_analysis_task():
    global ANALYSIS_STATUS
    try:
        ANALYSIS_STATUS["semantic"]["running"] = True
        print("[BACKEND] Démarrage analyse sémantique...")
        run_semantic(data_base="data/processed_clean")
        ANALYSIS_STATUS["semantic"]["running"] = False
        ANALYSIS_STATUS["semantic"]["completed"] = True
        print("[BACKEND] Analyse sémantique terminée")
    except Exception as e:
        ANALYSIS_STATUS["semantic"]["running"] = False
        ANALYSIS_STATUS["semantic"]["completed"] = False
        print(f"[BACKEND ERROR] Analyse sémantique échouée: {e}")
        import traceback
        traceback.print_exc()

@app.post("/api/analysis/semantic/start")
async def start_semantic_analysis(background_tasks: BackgroundTasks):
    if ANALYSIS_STATUS["semantic"]["running"]:
        raise HTTPException(status_code=400, detail="Analyse sémantique déjà en cours")
    
    background_tasks.add_task(run_semantic_analysis_task)
    return {"status": "success", "message": "Analyse sémantique démarrée"}

@app.get("/api/analysis/semantic/results")
async def get_semantic_results(corpus: str = "gaza"):
    if corpus not in ["gaza", "ukraine"]:
        raise HTTPException(status_code=400, detail="Corpus invalide. Utilisez 'gaza' ou 'ukraine'")
    keywords = ["attack", "strike", "civilian", "resistance", "occupation"]
    concordances = {}

    for kw in keywords:
        path = f"results/semantic/{corpus}_concordance_{kw}.csv"
        rows = read_csv_to_dict(path)
        items = []
        for r in rows:
            items.append({
                'doc_id': r.get('doc_id') or r.get('id'),
                'left': r.get('left') or r.get('context_left') or '',
                'keyword': r.get('keyword') or kw,
                'right': r.get('right') or r.get('context_right') or ''
            })
        concordances[kw] = items

    # Lire les voisins word2vec
    neighbors_file = f"results/semantic/{corpus}_word2vec_neighbors.csv"
    neighbors_rows = read_csv_to_dict(neighbors_file)
    neighbors = []
    for r in neighbors_rows:
        try:
            sim = float(r.get('similarity') or r.get('sim') or 0)
        except Exception:
            sim = 0.0
        neighbors.append({
            'actor': r.get('actor') or r.get('entity'),
            'neighbor': r.get('neighbor') or r.get('word'),
            'similarity': sim
        })

    # Lire les clusters sémantiques et éclater les mots
    clusters_file = f"results/semantic/{corpus}_semantic_clusters.csv"
    clusters_rows = read_csv_to_dict(clusters_file)
    clusters = []
    for r in clusters_rows:
        cluster_id = r.get('cluster_id') or r.get('cluster') or r.get('cluster')
        keywords_str = r.get('keywords') or r.get('words') or ''
        if isinstance(keywords_str, str):
            words = [w.strip() for w in keywords_str.split(',') if w.strip()]
            for w in words:
                try:
                    cid = int(cluster_id)
                except Exception:
                    cid = cluster_id
                clusters.append({'cluster': cid, 'word': w})

    return {
        'status': 'success',
        'data': {
            'concordances': concordances,
            'word2vec_neighbors': neighbors,
            'clusters': clusters
        }
    }

@app.get("/api/analysis/sentiment/results")
async def get_sentiment_results(corpus: str = "gaza"):
    if corpus not in ["gaza", "ukraine"]:
        raise HTTPException(status_code=400, detail="Corpus invalide. Utilisez 'gaza' ou 'ukraine'")
    
    victims_file = f"results/sentiment/{corpus}_victims_sentiment.csv"
    actor_file = f"results/sentiment/{corpus}_actor_sentiment.csv"
    
    victims = read_csv_to_dict(victims_file)
    actors = []
    try:
        if os.path.exists(actor_file):
            df_actors = pd.read_csv(actor_file)
            if not df_actors.empty and 'actor' in df_actors.columns:
                grouped = df_actors.groupby('actor').agg(
                    mean_compound=pd.NamedAgg(column='compound', aggfunc='mean'),
                    occurrences=pd.NamedAgg(column='actor', aggfunc='count')
                ).reset_index()

                actors = []
                for _, row in grouped.iterrows():
                    actors.append({
                        'actor': row['actor'],
                        'mean_score': float(row['mean_compound']),
                        'count': int(row['occurrences']),
                        'sample_text': None
                    })
            else:
                actors = read_csv_to_dict(actor_file)
        else:
            actors = []
    except Exception as e:
        print(f"Erreur lors de l'agrégation des acteurs: {e}")
        actors = read_csv_to_dict(actor_file)
    
    return {
        "status": "success",
        "data": {
            "victims": victims,
            "actors": actors
        }
    }

async def run_sentiment_analysis_task():
    global ANALYSIS_STATUS
    try:
        ANALYSIS_STATUS["sentiment"]["running"] = True
        print("[BACKEND] Démarrage analyse de sentiment...")
        
        try:
            from src.sentiment.run_sentiment import run_sentiment
            run_sentiment(data_base="data/processed_clean")
            ANALYSIS_STATUS["sentiment"]["running"] = False
            ANALYSIS_STATUS["sentiment"]["completed"] = True
            print("[BACKEND] Analyse de sentiment terminée")
        except ImportError as ie:
            print(f"[BACKEND ERROR] Module sentiment non trouvé: {ie}")
            raise HTTPException(status_code=500, detail="Module d'analyse de sentiment non disponible")
            
    except Exception as e:
        ANALYSIS_STATUS["sentiment"]["running"] = False
        ANALYSIS_STATUS["sentiment"]["completed"] = False
        print(f"[BACKEND ERROR] Analyse de sentiment échouée: {e}")
        import traceback
        traceback.print_exc()

@app.post("/api/analysis/sentiment/start")
async def start_sentiment_analysis(background_tasks: BackgroundTasks):
    if ANALYSIS_STATUS["sentiment"]["running"]:
        raise HTTPException(status_code=400, detail="Analyse de sentiment déjà en cours")
    
    background_tasks.add_task(run_sentiment_analysis_task)
    return {"status": "success", "message": "Analyse de sentiment démarrée"}

@app.get("/api/analysis/status")
async def get_analysis_status():
    return {
        "status": "success",
        "data": ANALYSIS_STATUS
    }

# ==================== Lancement du serveur ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)