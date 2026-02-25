"""
Scorer Module — Computes TF-IDF and Semantic Similarity scores between
resume and job description text.

Two approaches for model comparison:
1. TF-IDF Cosine Similarity  (keyword-based, fast)
2. Sentence Transformers     (semantic, context-aware)
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Lazy-load sentence transformer to avoid slow startup
_model = None

def _get_sentence_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_tfidf_score(resume_text: str, jd_text: str) -> float:
    """
    TF-IDF cosine similarity between resume and JD.
    Returns float between 0 and 1.
    """
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),  # unigrams + bigrams
        max_features=5000
    )
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(np.clip(score, 0, 1))
    except Exception:
        return 0.0


def get_semantic_score(resume_text: str, jd_text: str) -> float:
    """
    Semantic similarity using Sentence Transformers (all-MiniLM-L6-v2).
    Chunked approach for long texts.
    Returns float between 0 and 1.
    """
    try:
        model = _get_sentence_model()

        # Truncate to reasonable length
        resume_chunk = resume_text[:1500]
        jd_chunk = jd_text[:1500]

        embeddings = model.encode([resume_chunk, jd_chunk])
        score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return float(np.clip(score, 0, 1))
    except Exception:
        # Fallback to TF-IDF if sentence transformers unavailable
        return get_tfidf_score(resume_text, jd_text)


def compute_match_score(tfidf_score: float, semantic_score: float) -> int:
    """
    Weighted combination of both scores.
    Semantic score gets higher weight as it's more meaningful.
    Returns integer percentage 0-100.
    """
    # 40% TF-IDF + 60% Semantic
    combined = (0.4 * tfidf_score) + (0.6 * semantic_score)
    # Scale up a bit since raw cosine similarity tends to be conservative
    scaled = min(combined * 1.4, 1.0)
    return int(round(scaled * 100))
