import faiss
import numpy as np
import pickle


class FAISSVectorStore:

    def __init__(self, dimension):

        self.dimension = dimension

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.documents = []

    def add_embeddings(
        self,
        embeddings,
        documents
    ):

        embeddings_array = np.array(
            embeddings,
            dtype="float32"
        )

        self.index.add(
            embeddings_array
        )

        self.documents.extend(
            documents
        )

    def search(
        self,
        query_embedding,
        top_k=3
    ):

        query_array = np.array(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query_array,
            top_k
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.documents):

                results.append(
                    self.documents[idx]
                )

        return results

    def save(self, index_path, docs_path):

        faiss.write_index(
            self.index,
            index_path
        )

        with open(docs_path, "wb") as f:

            pickle.dump(
                self.documents,
                f
            )

    def load(self, index_path, docs_path):

        self.index = faiss.read_index(
            index_path
        )

        with open(docs_path, "rb") as f:

            self.documents = pickle.load(f)