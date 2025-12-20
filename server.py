from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

# Define request models
class CorpusRequest(BaseModel):
    corpus: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the NLP Project API"}

# Preprocessing endpoint
@app.post("/preprocess")
def preprocess_corpus(request: CorpusRequest):
    corpus = request.corpus
    script_path = "src/preprocessing/pipeline.py"
    
    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail="Preprocessing script not found")
    
    try:
        result = subprocess.run(
            ["python", script_path, "--corpus", corpus],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return {"message": "Preprocessing completed", "output": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Lexical analysis endpoint
@app.post("/lexical-analysis")
def lexical_analysis(request: CorpusRequest):
    corpus = request.corpus
    script_path = "src/lexicale_analysis/compare_corpora.py"
    
    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail="Lexical analysis script not found")
    
    try:
        result = subprocess.run(
            ["python", script_path, "--corpus", corpus],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return {"message": "Lexical analysis completed", "output": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Semantic analysis endpoint
@app.post("/semantic-analysis")
def semantic_analysis():
    script_path = "src/semantic_analysis/run_semantic.py"
    
    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail="Semantic analysis script not found")
    
    try:
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return {"message": "Semantic analysis completed", "output": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))