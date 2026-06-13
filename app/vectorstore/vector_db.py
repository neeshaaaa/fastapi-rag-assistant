from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance
)
from uuid import uuid4

COLLECTION_NAME = "documents"

# SINGLE GLOBAL CLIENT
client = None

def get_client():
    global client
    if client is None:
        client = QdrantClient(
            path="./qdrant_data"
        )
    return client


def create_collection():

    client = get_client()
    collections = client.get_collections()

    names = [
        c.name
        for c in collections.collections
    ]

    if COLLECTION_NAME not in names:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )


def store_chunks(
    chunks,
    embeddings,
    filename
):

    points = []

    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        points.append(

            PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "filename": filename
                }
            )

        )

    client = get_client()
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )