import faiss
import numpy as np

# MiniLM produces 384-dimension vectors
index = faiss.IndexFlatL2(384)
metadata_store = []

def add_vector(embedding, metadata):
    vector = np.array([embedding]).astype("float32")
    index.add(vector)
    metadata_store.append(metadata)

def search_vector(embedding, k=5):
    vector = np.array([embedding]).astype("float32")
    _, indices = index.search(vector, k)

    results = []
    for i in indices[0]:
        if i < len(metadata_store):
            results.append(metadata_store[i])

    return results
