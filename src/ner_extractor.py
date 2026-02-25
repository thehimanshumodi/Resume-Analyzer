"""
NER Extractor — Extracts skills, tools, organizations, education keywords
from resume and job description text using spaCy + custom skill patterns.
"""

import spacy
import re
from typing import Dict, List

# Load spaCy model (small English model)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


# ── MASTER SKILLS / TECH KEYWORD LIST ────────────────────────────────────────
TECH_SKILLS = {
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "r", "scala",
    "go", "rust", "kotlin", "swift", "php", "ruby", "matlab",

    # ML / AI
    "machine learning", "deep learning", "neural networks", "nlp",
    "natural language processing", "computer vision", "reinforcement learning",
    "transfer learning", "generative ai", "llm", "large language models",
    "transformers", "bert", "gpt", "t5", "llama", "rag",
    "retrieval augmented generation", "fine-tuning",

    # ML Libraries
    "scikit-learn", "sklearn", "tensorflow", "keras", "pytorch", "xgboost",
    "lightgbm", "catboost", "huggingface", "spacy", "nltk", "gensim",
    "fastai", "opencv",

    # Data / Analytics
    "pandas", "numpy", "matplotlib", "seaborn", "plotly", "tableau",
    "power bi", "excel", "sql", "nosql",

    # Cloud / MLOps
    "aws", "gcp", "azure", "docker", "kubernetes", "mlflow", "dvc",
    "airflow", "kafka", "spark", "hadoop", "databricks",

    # Databases
    "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "sqlite",
    "bigquery", "snowflake",

    # Web / API
    "flask", "fastapi", "django", "streamlit", "gradio", "rest api",
    "graphql",

    # Tools
    "git", "github", "gitlab", "jupyter", "vs code", "linux",
    "bash", "shell scripting",

    # Soft skills / roles
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "agile", "scrum",

    # NLP specific
    "text classification", "sentiment analysis", "named entity recognition",
    "ner", "text summarization", "question answering", "information extraction",
    "word embeddings", "word2vec", "glove", "fasttext", "sentence transformers",
    "semantic similarity", "topic modeling", "lda", "tfidf", "tf-idf",
}

EDUCATION_KEYWORDS = {
    "bachelor", "master", "phd", "b.tech", "m.tech", "b.e", "m.e",
    "b.sc", "m.sc", "mba", "computer science", "data science",
    "information technology", "statistics", "mathematics", "engineering"
}


def extract_tech_skills(text: str) -> List[str]:
    """Extract tech skills using keyword matching (case-insensitive)."""
    text_lower = text.lower()
    found = []
    for skill in TECH_SKILLS:
        # Use word boundary matching
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill.title() if len(skill) > 3 else skill.upper())
    return sorted(set(found))


def extract_education(text: str) -> List[str]:
    """Extract education-related keywords."""
    text_lower = text.lower()
    found = []
    for kw in EDUCATION_KEYWORDS:
        if kw in text_lower:
            found.append(kw.title())
    return sorted(set(found))


def extract_spacy_entities(text: str) -> Dict[str, List[str]]:
    """Use spaCy for ORG, GPE, DATE, PERSON entities."""
    doc = nlp(text[:10000])  # Limit for performance
    entities = {"ORG": [], "GPE": [], "DATE": [], "PERSON": []}
    for ent in doc.ents:
        if ent.label_ in entities:
            clean = ent.text.strip()
            if len(clean) > 1 and clean not in entities[ent.label_]:
                entities[ent.label_].append(clean)
    return entities


def extract_years_experience(text: str) -> str:
    """Extract years of experience mentioned."""
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
    """
    Main extraction function — returns structured entities dict.
    """
    spacy_ents = extract_spacy_entities(text)
    tech_skills = extract_tech_skills(text)
    education = extract_education(text)
    exp = extract_years_experience(text)

    return {
        "Technical Skills": tech_skills,
        "Education": education,
        "Organizations": spacy_ents.get("ORG", [])[:8],
        "Locations": spacy_ents.get("GPE", [])[:5],
        "Experience": [exp] if exp != "Not specified" else [],
        "Dates": spacy_ents.get("DATE", [])[:5],
    }
