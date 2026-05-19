#cat > benchmark.py << 'EOF'
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from search import SearchEngine

docs = []
with open("data/documents.jsonl", "r") as f:
    for line in f:
        docs.append(json.loads(line)["text"])

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(docs)

def tfidf_search(query, top_k=10):
    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, tfidf_matrix).flatten()
    return scores.argsort()[-top_k:][::-1].tolist()

engine = SearchEngine()

def semantic_search(query, top_k=10):
    results = engine.query(query, top_k)
    return [docs.index(r["doc"]) for r in results]

queries = [
    "what is semantic search?",
    "how does FAISS work?",
    "flask REST API",
    "embedding models for NLP",
    "apple m1 machine learning"
]

print(f"{'Query':<40} {'TF-IDF top1':<50} {'Semantic top1'}")
print("-" * 140)
for q in queries:
    t = tfidf_search(q)
    s = semantic_search(q)
    print(f"{q:<40} {docs[t[0]][:45]:<50} {docs[s[0]][:45]}")
#EOF