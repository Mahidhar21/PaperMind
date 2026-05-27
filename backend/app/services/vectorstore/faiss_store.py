import faiss
import numpy as np


class FAISSVectorStore:

    def __init__(self, dimension):

        self.dimension = dimension

        self.index = faiss.IndexFlatL2(dimension)

        self.chunks = []


    def add_embeddings(self, embeddings, chunks):

        embeddings_array = np.array(embeddings).astype("float32")

        self.index.add(embeddings_array)

        self.chunks.extend(chunks)


    def search(self, query_embedding, top_k=3):

        query_array = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_array, top_k)

        results = []

        for i in indices[0]:

            results.append(self.chunks[i])

        return results