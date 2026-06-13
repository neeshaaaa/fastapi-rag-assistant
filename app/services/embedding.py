from sentence_transformers import SentenceTransformer
from typing import List

model = None


def get_model():
    global model
    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def generate_embedding(text: str) -> List[float]:
    m = get_model()
    return m.encode(text).tolist()


def generate_embeddings(chunks: List[str]) -> List[List[float]]:
    m = get_model()
    return m.encode(chunks).tolist()
