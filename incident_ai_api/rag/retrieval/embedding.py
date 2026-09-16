import math
import re
from collections import Counter
 
 
class SimpleEmbeddingModel:
 
    def tokenize(self, text: str):
        return re.findall(r"\b[a-zA-Z0-9-]+\b", text.lower())
 
    def build_vocabulary(self, texts: list[str]):
        vocabulary = set()
 
        for text in texts:
            vocabulary.update(self.tokenize(text))
 
        return sorted(vocabulary)
 
    def embed_text(self, text: str, vocabulary: list[str]):
        tokens = self.tokenize(text)
        counts = Counter(tokens)
 
        total_words = len(tokens)
 
        if total_words == 0:
            return [0.0] * len(vocabulary)
 
        vector = []
 
        for word in vocabulary:
            frequency = counts[word] / total_words
            vector.append(frequency)
 
        return vector
 
    def embed_documents(self, texts: list[str]):
        vocabulary = self.build_vocabulary(texts)
 
        vectors = [
            self.embed_text(text, vocabulary)
            for text in texts
        ]
 
        return vocabulary, vectors
 
 
def cosine_similarity(vector_a, vector_b):
 
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )
 
    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )
 
    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )
 
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
 
    return dot_product / (magnitude_a * magnitude_b)