from qdrant_client import QdrantClient

client = QdrantClient(path="./qdrant_data")

print(dir(client))