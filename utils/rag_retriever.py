
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class FinancialRAG:
    def __init__(self):
        self.chunks = []
        self.vectorizer = TfidfVectorizer()

    def add_chunks(self, chunks):
        self.chunks = chunks
        self.embeddings = self.vectorizer.fit_transform(chunks)

    def query(self, question, top_k=3):
        query_vec = self.vectorizer.transform([question])
        sim = cosine_similarity(query_vec, self.embeddings).flatten()
        top_indices = sim.argsort()[-top_k:][::-1]
        return [self.chunks[i] for i in top_indices]
