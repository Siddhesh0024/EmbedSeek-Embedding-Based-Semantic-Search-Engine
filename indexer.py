#cat > indexer.py << 'EOF'
import faiss, pickle, numpy as np, json, os
from encoder import Encoder

def build_index(model_name="BAAI/bge-small-en"):
    docs = []
    with open("data/documents.jsonl", "r") as f:
        for line in f:
            docs.append(json.loads(line)["text"])

    print(f"Loaded {len(docs)} documents")
    enc = Encoder(model_name)
    embeddings = np.array(enc.encode(docs), dtype="float32")

    os.makedirs("embeddings", exist_ok=True)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, "embeddings/index.faiss")
    with open("embeddings/doc_store.pkl", "wb") as f:
        pickle.dump(docs, f)
    print("Index built and saved.")

if __name__ == "__main__":
    build_index()
