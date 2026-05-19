from sentence_transformers import SentenceTransformer

class Encoder:
    def __init__(self, model_name="BAAI/bge-small-en"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts, batch_size=64, show_progress=True):
        return self.model.encode(
            texts, batch_size=batch_size,
            show_progress_bar=show_progress,
            normalize_embeddings=True
        )