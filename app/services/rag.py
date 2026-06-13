from app.vectorstore.vector_db import get_client
from app.services.embedding import generate_embedding

COLLECTION_NAME = "documents"


def search_similar_chunks(query: str, top_k: int = 5):

    client = get_client()

    query_vector = generate_embedding(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )

    chunks = []

    for r in results.points:
        chunks.append(r.payload["text"])

    return chunks