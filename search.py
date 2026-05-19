import faiss, pickle, numpy as np
from encoder import Encoder

class SearchEngine:
    def __init__(self, model_name="BAAI/bge-small-en"):
        self.enc = Encoder(model_name)
        self.index = faiss.read_index("embeddings/index.faiss")
        with open("embeddings/doc_store.pkl", "rb") as f:
            self.docs = pickle.load(f)

    def query(self, text: str, top_k=10):
        vec = self.enc.encode([text], show_progress=False).astype("float32")
        scores, indices = self.index.search(vec, top_k)
        return [{"doc": self.docs[i], "score": float(scores[0][j])}
                for j, i in enumerate(indices[0])]