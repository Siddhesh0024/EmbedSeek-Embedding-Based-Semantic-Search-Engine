# EmbedSeek — Embedding-Based Semantic Search Engine

A semantic search pipeline over 500K+ documents using sentence-transformers, FAISS, and Flask.

## Tech Stack

- **Python** — core language
- **sentence-transformers** — document & query encoding
- **FAISS** — vector similarity search
- **HuggingFace** — model hub (`bge-small-en`)
- **Flask** — REST API

## Project Structure

```
embedseek/
├── data/
│   └── documents.jsonl
├── embeddings/
│   ├── index.faiss
│   └── doc_store.pkl
├── encoder.py
├── indexer.py
├── search.py
├── benchmark.py
├── app.py
└── requirements.txt
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**requirements.txt**
```
sentence-transformers
faiss-cpu
flask
numpy
scikit-learn
```

## Usage

### 1. Build the Index

```bash
python indexer.py
```

Encodes all documents and saves the FAISS index to `embeddings/`. One-time step.

### 2. Run the API

```bash
python app.py
```

### 3. Search

```bash
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "your search query", "top_k": 10}'
```

## Encoder

The encoder interface is modular — swap models without touching downstream code:

```python
from encoder import Encoder

enc = Encoder("BAAI/bge-small-en")   # default
# enc = Encoder("all-MiniLM-L6-v2") # alternative
```

## Benchmark Results

| Model | Recall@10 |
|---|---|
| TF-IDF baseline | — |
| all-MiniLM-L6-v2 | weaker on domain queries |
| **bge-small-en** | **+29% over TF-IDF** |

`bge-small-en` outperformed `all-MiniLM-L6-v2` on domain-specific queries with no meaningful latency penalty.

## M1 Mac Notes

MPS acceleration is supported. Set device in encoder:

```python
SentenceTransformer("BAAI/bge-small-en", device="mps")
```

Expected encoding time for 500K docs: ~20–40 minutes.

## API Reference

### `POST /search`

**Request**
```json
{
  "query": "string",
  "top_k": 10
}
```

**Response**
```json
[
  { "doc": "matched document text", "score": 0.91 },
  ...
]
```

