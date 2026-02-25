"""
Text Cleaner — Preprocessing pipeline for resume and JD text.
"""

import re


def clean_text(text: str) -> str:
    """
    Clean and normalize text for NLP processing.
    - Lowercase
    - Remove special characters (keep alphanumeric + spaces)
    - Remove extra whitespace
    - Remove URLs and emails
    """
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    # Remove phone numbers
    text = re.sub(r'\+?\d[\d\s\-().]{7,}\d', '', text)
    # Keep letters, numbers, common punctuation
    text = re.sub(r'[^a-zA-Z0-9\s\+\#\.]', ' ', text)
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()
