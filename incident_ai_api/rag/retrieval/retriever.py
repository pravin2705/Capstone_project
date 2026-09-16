import json
import re
 
from pathlib import Path
 
from rag.retrieval.embedding import (
    SimpleEmbeddingModel,
    cosine_similarity,
)
 
 
# Location of the vector index
INDEX_FILE = Path("rag/retrieval/vector_index.json")
 
 
class Retriever:
 
    def __init__(self):
 
        # Load the vector index
        index_data = json.loads(
            INDEX_FILE.read_text(
                encoding="utf-8"
            )
        )
 
        # Vocabulary used for embeddings
        self.vocabulary = index_data["vocabulary"]
 
        # All document chunks
        self.chunks = index_data["chunks"]
 
        # Embedding model
        self.embedding_model = SimpleEmbeddingModel()
 
    # -------------------------------------------------
    # Convert text into important words
    # -------------------------------------------------
    def _tokenize(self, text: str):
 
        return set(
            re.findall(
                r"\b[a-zA-Z0-9-]+\b",
                text.lower(),
            )
        )
 
    # -------------------------------------------------
    # Calculate keyword matching score
    # -------------------------------------------------
    def _keyword_score(
        self,
        query: str,
        metadata: dict,
        text: str,
    ):
 
        # Words that are not useful for retrieval
        stop_words = {
            "what",
            "should",
            "i",
            "the",
            "a",
            "an",
            "is",
            "be",
            "for",
            "on",
            "to",
            "of",
            "and",
            "in",
            "do",
        }
 
        # Get query words
        query_words = {
            word
            for word in self._tokenize(query)
            if word not in stop_words
        }
 
        # Get section name
        section = str(
            metadata.get(
                "section",
                ""
            )
        )
 
        # Convert section and text to words
        section_words = self._tokenize(
            section
        )
 
        text_words = self._tokenize(
            text
        )
 
        # No useful query words
        if not query_words:
            return 0.0
 
        # Words matching section name
        section_matches = (
            query_words & section_words
        )
 
        # Words matching chunk text
        text_matches = (
            query_words & text_words
        )
 
        # Section matching score
        section_score = (
            len(section_matches)
            / len(query_words)
        )
 
        # Text matching score
        text_score = (
            len(text_matches)
            / len(query_words)
        )
 
        # Section title is more important
        keyword_score = (
            0.8 * section_score
            + 0.2 * text_score
        )
 
        return keyword_score
 
    # -------------------------------------------------
    # Search documents
    # -------------------------------------------------
    def search(
        self,
        query: str,
        top_k: int = 3,
        machine_model: str | None = None,
        manual_version: str | None = None,
    ):
 
        # ---------------------------------------------
        # Create embedding for the query
        # ---------------------------------------------
 
        query_vector = (
            self.embedding_model.embed_text(
                query,
                self.vocabulary,
            )
        )
 
        results = []
 
        # ---------------------------------------------
        # Check every document chunk
        # ---------------------------------------------
 
        for chunk in self.chunks:
 
            metadata = chunk["metadata"]
 
            # -----------------------------------------
            # Metadata filtering - machine model
            # -----------------------------------------
 
            if machine_model is not None:
 
                if (
                    metadata["machine_model"]
                    != machine_model
                ):
                    continue
 
            # -----------------------------------------
            # Metadata filtering - manual version
            # -----------------------------------------
 
            if manual_version is not None:
 
                stored_version = str(
                    metadata["manual_version"]
                ).rstrip(".")
 
                requested_version = str(
                    manual_version
                ).rstrip(".")
 
                if (
                    stored_version
                    != requested_version
                ):
                    continue
 
            # -----------------------------------------
            # Semantic similarity
            # -----------------------------------------
 
            semantic_score = (
                cosine_similarity(
                    query_vector,
                    chunk["vector"],
                )
            )
 
            # -----------------------------------------
            # Keyword matching
            # -----------------------------------------
 
            keyword_score = (
                self._keyword_score(
                    query,
                    metadata,
                    chunk["text"],
                )
            )
 
            # -----------------------------------------
            # Hybrid retrieval score
            # -----------------------------------------
            #
            # 75% semantic similarity
            # 25% keyword matching
            #
            # This combines:
            # - semantic understanding
            # - exact keyword matching
            # -----------------------------------------
 
            final_score = (
                0.75 * semantic_score
                + 0.25 * keyword_score
            )
 
            # -----------------------------------------
            # Store result
            # -----------------------------------------
 
            results.append(
                {
                    "chunk_id": chunk[
                        "chunk_id"
                    ],
                    "text": chunk["text"],
                    "metadata": metadata,
 
                    # Final ranking score
                    "score": final_score,
 
                    # Individual scores
                    "semantic_score": semantic_score,
                    "keyword_score": keyword_score,
                }
            )
 
        # ---------------------------------------------
        # Sort by highest score
        # ---------------------------------------------
 
        results.sort(
            key=lambda x: x["score"],
            reverse=True,
        )
 
        # ---------------------------------------------
        # Return Top-K results
        # ---------------------------------------------
 
        return results[:top_k]