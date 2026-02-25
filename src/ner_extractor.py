"""
NER Extractor — uses spaCy blank model + custom keyword matching.
No en_core_web_sm needed — works on any environment including Streamlit Cloud.
"""

import spacy
import re
from typing import Dict, List

# Use blank English model — no download needed!
nlp = spacy.blank("en")


TECH_SKILLS = {
    "python", "java", "javascript", "typescript", "c++", "c#", "r", "scala",
    "go", "rust", "kotlin", "swift", "php", "ruby", "matlab",
    "machine learning", "deep learning", "neural networks", "nlp",
    "natural language processing", "computer vision", "reinforcement learning",
    "transfer learning", "generative ai", "llm", "large language models",
    "transformers", "bert", "gpt", "t5", "llama", "rag",
    "retrieval augmented generation", "fine-tuning",
    "scikit-learn", "sklearn", "tensorflow", "keras", "pytorch", "xgboost",
    "lightgbm", "catboost", "huggingface", "spacy", "nltk", "gensim",
    "fastai", "opencv",
    "pandas", "numpy", "matplotlib", "seaborn", "plotly", "tableau",
    "power bi", "excel", "sql", "nosql",
    "aws", "gcp", "azure", "docker", "kubernetes", "mlflow", "dvc",
    "airflow", "kafka", "spark", "hadoop", "databricks",
    "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "sqlite",
    "bigquery", "snowflake",
    "flask", "fastapi", "django", "streamlit", "gradio", "rest api", "graphql",
    "git", "github", "gitlab", "jupyter", "vs code", "linux", "bash",
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "agile", "scrum",
    "text classification", "sentiment analysis", "named entity recognition",
    "ner", "text summarization", "question answering", "information extraction",
    "word embeddings", "word2vec", "glove", "fasttext", "sentence transformers",
    "semantic similarity", "topic modeling", "lda", "tfidf", "tf-idf",
    "langchain", "faiss", "openai", "groq", "llama", "mistral",
}

EDUCATION_KEYWORDS = {
    "bachelor", "master", "phd", "b.tech", "m.tech", "b.e", "m.e",
    "b.sc", "m.sc", "mba", "computer science", "data science",
    "information technology", "statistics", "mathematics", "engineering"
}


def extract_tech_skills(text: str) -> List[str]:
    text_lower = text.lower()
    found = []
    for skill in TECH_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill.title() if len(skill) > 3 else skill.upper())
    return sorted(set(found))


def extract_education(text: str) -> List[str]:
    text_lower = text.lower()
    return sorted({kw.title() for kw in EDUCATION_KEYWORDS if kw in text_lower})


def extract_orgs_regex(text: str) -> List[str]:
    """Simple regex-based org extraction (no spaCy NER model needed)."""
    pattern = r'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){1,3})\b'
    matches = re.findall(pattern, text)
    stopwords = {"Responsibilities", "Requirements", "Experience", "Skills",
                 "Education", "Projects", "Summary", "About", "Role"}
    return list({m for m in matches if m not in stopwords})[:8]


def extract_years_experience(text: str) -> str:
    patterns = [
        r'(\d+)\+?\s+years?\s+(?:of\s+)?experience',
        r'experience\s+of\s+(\d+)\+?\s+years?',
    ]
    for pat in patterns:
        match = re.search(pat, text.lower())
        if match:
            return f"{match.group(1)}+ years"
    return "Not specified"


def extract_entities(text: str) -> Dict[str, List[str]]:
    tech_skills = extract_tech_skills(text)
    education = extract_education(text)
    orgs = extract_orgs_regex(text)
    exp = extract_years_experience(text)

    return {
        "Technical Skills": tech_skills,
        "Education": education,
        "Organizations": orgs,
        "Locations": [],
        "Experience": [exp] if exp != "Not specified" else [],
        "Dates": [],
    }