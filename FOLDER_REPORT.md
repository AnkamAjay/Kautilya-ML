# Semantic Search Folder Report

## 📋 Overview
This workspace contains a semantic search engine for Twitter API v2 Postman documentation.

---

## 📁 Folder Structure

```
semantic_search/
├── semantic_search.py                          (Main script)
├── requirements.txt                            (Dependencies)
├── output.txt                                  (Latest query results)
├── twitter_doc_index.faiss                     (Cached FAISS vector index)
├── twitter_doc_metadata.json                   (Metadata for chunks)
├── postman-twitter-api-master/                 (Twitter API docs)
│   ├── README.md
│   ├── CODE_OF_CONDUCT.md
│   ├── CONTRIBUTING.md
│   ├── LICENSE
│   ├── Twitter API v2.postman_collection.json  (Main API doc - JSON)
│   ├── Twitter API v2.postman_environment.json (Environment config)
│   └── .github/
├── venv/                                       (Virtual environment)
└── FOLDER_REPORT.md                            (This file)
```

---

## 📄 File Descriptions

### **semantic_search.py** (Main Application)
- **Purpose**: CLI tool for semantic search over Twitter API documentation
- **Features**:
  - Loads JSON documentation from `postman-twitter-api-master/`
  - Chunks documents intelligently (filters fragments < 20 chars)
  - Builds FAISS vector index using `sentence-transformers` embeddings
  - Supports queries with configurable top-k results
- **CLI Args**:
  - `--query` (required): Search query string
  - `--top_k` (optional, default=5): Number of top results to return
- **Output Fields**:
  - `rank`: Position in results (1-N)
  - `score`: Distance metric (lower = better match)
  - `chunk_id`: Unique chunk identifier
  - `source`: Source file path
  - `text`: Documentation snippet

### **requirements.txt**
- Dependencies for the project:
  - `faiss-cpu==1.7.4` — Vector similarity search
  - `sentence-transformers==2.7.0` — Embeddings model
  - `numpy==1.26.4` — Numerical operations
  - `scikit-learn==1.5.0` — ML utilities
  - `python-dateutil==2.9.0` — Date handling
  - `tqdm==4.66.4` — Progress bars

### **output.txt**
- Latest query results (from first test run)
- Contains JSON array with rank, score, chunk_id, source, and text fields

### **twitter_doc_index.faiss**
- Cached FAISS index (binary file, ~18MB)
- Pre-built vector index for fast similarity search
- Avoids rebuilding index on each run

### **twitter_doc_metadata.json**
- Metadata mapping for all indexed chunks
- Maps `chunk_id` → `source` file path and original `text`
- Used for result attribution

### **postman-twitter-api-master/**
- Official Twitter API v2 Postman collection
- Contains:
  - `Twitter API v2.postman_collection.json` — Full API documentation (~2MB)
  - `Twitter API v2.postman_environment.json` — Auth environment setup
  - Documentation files (README, LICENSE, etc.)

### **venv/**
- Python virtual environment
- Contains installed packages (sentence-transformers, faiss-cpu, torch, etc.)
- Isolated environment to avoid conflicts with system Python

---

## 🚀 Quick Usage

### Run a search query:
```powershell
cd 'C:\Users\ajaya\OneDrive\Documents\Desktop\semantic_search'
& '.\venv\Scripts\python.exe' semantic_search.py --query "How do I fetch tweets?" --top_k 5
```

### Save output to file:
```powershell
& '.\venv\Scripts\python.exe' semantic_search.py --query "user timeline" --top_k 3 | Out-File -Encoding UTF8 results.json
```

### Example queries:
```powershell
# Fetch tweets with expansions
& '.\venv\Scripts\python.exe' semantic_search.py --query "How do I fetch tweets with expansions?" --top_k 5

# Search for authentication
& '.\venv\Scripts\python.exe' semantic_search.py --query "bearer token authentication" --top_k 3

# Find user endpoints
& '.\venv\Scripts\python.exe' semantic_search.py --query "get user by id" --top_k 5
```

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Total JSON chunks indexed | ~1,500+ |
| Embedding model | `all-MiniLM-L6-v2` (384 dims) |
| Index type | FAISS IndexFlatL2 (Euclidean) |
| Source files | `Twitter API v2.postman_collection.json` |
| Latest query | "How do I fetch tweets with expansions?" |
| Top result score | 0.7596 |

---

## ✅ Status

- ✅ Semantic search engine working
- ✅ FAISS index built and cached
- ✅ Metadata tracking (rank, score, chunk_id, source, text)
- ✅ CLI interface functional
- ⏳ Next: Implement `narrative_builder.py` for second challenge (70 points)

---

## 🔧 Troubleshooting

### Script takes long time on first run?
- Downloads embedding model (~30MB) from HuggingFace
- Builds FAISS index from all chunks (~few minutes depending on CPU)
- Subsequent runs use cached index (instant)

### Import errors?
- Ensure venv is activated: `& '.\venv\Scripts\activate'`
- Reinstall deps: `pip install -r requirements.txt`

### Results not relevant?
- Chunking currently splits on any text > 20 chars
- Can improve by using intelligent sentence/paragraph splitting
- Consider larger embedding model (e.g., `all-mpnet-base-v2`) for better quality

---

## 📝 Next Steps

1. Implement `narrative_builder.py` for Task 2 (70 points)
2. Optimize chunking strategy (avoid tiny JSON fragments)
3. Add caching for embeddings to speed up queries
4. Consider hybrid search (semantic + keyword BM25)
5. Add unit tests and edge case handling
