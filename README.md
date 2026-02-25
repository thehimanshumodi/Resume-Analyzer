# 🎯 ResumeIQ — NLP-Powered Resume Analyzer

A smart **Resume ↔ Job Description Matcher** built with Python and NLP techniques.
This project demonstrates core NLP concepts: Named Entity Recognition (NER), TF-IDF, Semantic Similarity, and Skill Gap Analysis.

---

## 🚀 Features

| Feature | Description |
|---|---|
| **NER Extraction** | Extracts skills, organizations, education from both resume & JD using spaCy |
| **TF-IDF Scoring** | Keyword-based cosine similarity (baseline model) |
| **Semantic Scoring** | Context-aware similarity using `all-MiniLM-L6-v2` Sentence Transformers |
| **Skill Gap Analysis** | Shows matched, missing, and extra skills with visual breakdown |
| **Recommendations** | Personalized tips based on match score and gaps |
| **Interactive UI** | Clean Streamlit dashboard with dark theme |

---

## 🛠️ Tech Stack

- **NLP**: spaCy, Sentence Transformers, scikit-learn (TF-IDF)
- **ML**: Cosine Similarity, Weighted Score Fusion
- **UI**: Streamlit, Plotly
- **Language**: Python 3.10+

---

## 📁 Project Structure

```
resume-matcher/
├── app.py                  # Streamlit UI (main entry)
├── requirements.txt
├── src/
│   ├── ner_extractor.py    # NER + skill extraction (spaCy + custom patterns)
│   ├── scorer.py           # TF-IDF & Semantic similarity scoring
│   ├── gap_analyzer.py     # Skill gap computation
│   ├── text_cleaner.py     # Text preprocessing pipeline
│   └── visualizer.py       # Plotly charts
└── README.md
```

---

## ⚙️ Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/resume-matcher
cd resume-matcher

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download spaCy model
python -m spacy download en_core_web_sm

# 5. Run the app
streamlit run app.py
```

---

## 🧠 NLP Concepts Used

### 1. Named Entity Recognition (NER)
Using spaCy's `en_core_web_sm` model combined with a **custom keyword matching** approach to extract:
- Technical skills (Python, PyTorch, SQL, etc.)
- Organizations (companies, universities)
- Education level (Bachelor's, Master's, etc.)

### 2. TF-IDF Cosine Similarity
Traditional bag-of-words approach. Converts both texts into TF-IDF vectors (bigrams included) and computes cosine similarity. Fast and interpretable — serves as the **baseline**.

### 3. Sentence Transformers (Semantic Similarity)
Uses `all-MiniLM-L6-v2` from HuggingFace to encode both texts into dense embeddings and compute semantic similarity. **Context-aware** — understands that "ML engineer" and "machine learning developer" are similar.

### 4. Score Fusion
Final score = **40% TF-IDF + 60% Semantic**. Semantic gets higher weight as it captures meaning better.

---

## 📊 Model Comparison

| Model | Approach | Speed | Accuracy |
|---|---|---|---|
| TF-IDF | Keyword matching | ⚡ Fast | Medium |
| Sentence Transformers | Semantic embeddings | 🐢 Slower | High |
| **Combined** | Weighted fusion | Medium | **Best** |

---

## 💡 Future Improvements

- [ ] Cover letter generator using Groq/OpenAI API
- [ ] PDF resume parsing (PyMuPDF)
- [ ] Job scraping from LinkedIn/Indeed
- [ ] ATS keyword density analysis
- [ ] Skill recommendation with learning resources

---

## 🙋 Author

Built by Himanshu Modi as an NLP portfolio project for data science job applications.

---

## 📄 License

MIT License
