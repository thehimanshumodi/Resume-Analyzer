import streamlit as st
import time
from src.ner_extractor import extract_entities
from src.scorer import compute_match_score, get_tfidf_score, get_semantic_score
from src.gap_analyzer import analyze_gaps
from src.text_cleaner import clean_text
from src.visualizer import plot_skill_match, plot_score_gauge

st.set_page_config(
    page_title="ResumeIQ — Smart Job Matcher",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

:root {
    --bg: #0b0c10;
    --surface: #13141a;
    --border: #1e2030;
    --accent: #00f5a0;
    --accent2: #00d4ff;
    --warn: #ff6b6b;
    --text: #e8eaf0;
    --muted: #6b7280;
}

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: var(--bg);
    color: var(--text);
}

.stApp { background-color: var(--bg); }

h1,h2,h3 { font-family: 'Syne', sans-serif; }

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
    line-height: 1.1;
}

.hero-sub {
    font-family: 'DM Mono', monospace;
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.5rem;
    letter-spacing: 0.5px;
}

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.score-badge {
    display: inline-block;
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.skill-tag {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    margin: 3px;
    font-family: 'DM Mono', monospace;
}

.tag-match {
    background: rgba(0,245,160,0.12);
    border: 1px solid rgba(0,245,160,0.4);
    color: var(--accent);
}

.tag-missing {
    background: rgba(255,107,107,0.12);
    border: 1px solid rgba(255,107,107,0.4);
    color: var(--warn);
}

.tag-extra {
    background: rgba(0,212,255,0.12);
    border: 1px solid rgba(0,212,255,0.4);
    color: var(--accent2);
}

.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1rem 0;
}

.metric-box {
    flex: 1;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}

.metric-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--accent);
}

.metric-label {
    font-size: 0.72rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 2px;
}

.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.8rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
}

.tip-box {
    background: rgba(0,245,160,0.05);
    border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.85rem;
    color: var(--text);
}

stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}

div[data-testid="stTextArea"] textarea {
    background-color: #13141a !important;
    color: #e8eaf0 !important;
    border-color: #1e2030 !important;
}

.stButton button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #0b0c10 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
}

.stButton button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px);
}

hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)


# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 2rem 0 1rem 0;">
    <div class="hero-title">ResumeIQ 🎯</div>
    <div class="hero-sub">// NLP-Powered Resume ↔ Job Description Analyzer & Skill Gap Detector</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── INPUT SECTION ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-header">📄 Your Resume</div>', unsafe_allow_html=True)
    resume_text = st.text_area(
        label="resume",
        placeholder="Paste your resume text here...\n\nInclude skills, experience, education, projects...",
        height=320,
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<div class="section-header">💼 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area(
        label="jd",
        placeholder="Paste the job description here...\n\nInclude required skills, responsibilities, qualifications...",
        height=320,
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)
analyze_btn = st.button("⚡  Analyze Match", use_container_width=True)

# ── ANALYSIS ─────────────────────────────────────────────────────────────────
if analyze_btn:
    if not resume_text.strip() or not jd_text.strip():
        st.error("⚠️  Please paste both your resume and the job description to continue.")
    else:
        with st.spinner("🔍 Extracting entities and computing scores..."):
            time.sleep(0.5)

            # Clean texts
            resume_clean = clean_text(resume_text)
            jd_clean = clean_text(jd_text)

            # Extract NER entities
            resume_entities = extract_entities(resume_text)
            jd_entities = extract_entities(jd_text)

            # Compute scores
            tfidf_score = get_tfidf_score(resume_clean, jd_clean)
            semantic_score = get_semantic_score(resume_clean, jd_clean)
            overall_score = compute_match_score(tfidf_score, semantic_score)

            # Gap analysis
            gaps = analyze_gaps(resume_entities, jd_entities)

        st.markdown("---")
        st.markdown('<div class="hero-title" style="font-size:1.8rem;">📊 Analysis Results</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # ── SCORE OVERVIEW ────────────────────────────────────────────────────
        c1, c2, c3, c4 = st.columns(4)
        score_color = "#00f5a0" if overall_score >= 70 else "#ffd166" if overall_score >= 45 else "#ff6b6b"

        with c1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val" style="color:{score_color};">{overall_score}%</div>
                <div class="metric-label">Overall Match</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{round(tfidf_score*100)}%</div>
                <div class="metric-label">TF-IDF Score</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{round(semantic_score*100)}%</div>
                <div class="metric-label">Semantic Score</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            matched = len(gaps["matched_skills"])
            missing = len(gaps["missing_skills"])
            total = matched + missing
            skill_pct = round(matched/total*100) if total > 0 else 0
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{skill_pct}%</div>
                <div class="metric-label">Skill Coverage</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── SKILL BREAKDOWN ────────────────────────────────────────────────────
        tab1, tab2, tab3 = st.tabs(["🎯 Skill Gap Analysis", "🔍 Entity Extraction", "💡 Recommendations"])

        with tab1:
            c_left, c_right = st.columns(2)

            with c_left:
                st.markdown('<div class="section-header">✅ Matched Skills</div>', unsafe_allow_html=True)
                if gaps["matched_skills"]:
                    tags = "".join([f'<span class="skill-tag tag-match">{s}</span>' for s in gaps["matched_skills"]])
                    st.markdown(tags, unsafe_allow_html=True)
                else:
                    st.markdown('<span style="color:#6b7280;">No direct skill matches found.</span>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-header">🔵 Extra Skills (not in JD)</div>', unsafe_allow_html=True)
                if gaps["extra_skills"]:
                    tags = "".join([f'<span class="skill-tag tag-extra">{s}</span>' for s in gaps["extra_skills"]])
                    st.markdown(tags, unsafe_allow_html=True)
                else:
                    st.markdown('<span style="color:#6b7280;">None found.</span>', unsafe_allow_html=True)

            with c_right:
                st.markdown('<div class="section-header">❌ Missing Skills (from JD)</div>', unsafe_allow_html=True)
                if gaps["missing_skills"]:
                    tags = "".join([f'<span class="skill-tag tag-missing">{s}</span>' for s in gaps["missing_skills"]])
                    st.markdown(tags, unsafe_allow_html=True)
                else:
                    st.markdown('<span style="color:#00f5a0; font-size:0.9rem;">🎉 Great! You seem to have all required skills.</span>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Bar chart
            if gaps["matched_skills"] or gaps["missing_skills"]:
                fig = plot_skill_match(gaps)
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="section-header">📄 Resume Entities</div>', unsafe_allow_html=True)
                for label, values in resume_entities.items():
                    if values:
                        st.markdown(f"**{label}**")
                        st.markdown(", ".join([f"`{v}`" for v in values[:10]]))
            with c2:
                st.markdown('<div class="section-header">💼 JD Entities</div>', unsafe_allow_html=True)
                for label, values in jd_entities.items():
                    if values:
                        st.markdown(f"**{label}**")
                        st.markdown(", ".join([f"`{v}`" for v in values[:10]]))

        with tab3:
            st.markdown('<div class="section-header">💡 Personalized Recommendations</div>', unsafe_allow_html=True)

            if overall_score >= 75:
                st.markdown('<div class="tip-box">🏆 <strong>Strong Match!</strong> Your resume aligns well with this job. Focus on tailoring your summary/objective to mirror the JD language.</div>', unsafe_allow_html=True)
            elif overall_score >= 50:
                st.markdown('<div class="tip-box">📈 <strong>Moderate Match.</strong> You have a decent foundation. Bridge the skill gaps listed above before applying.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="tip-box">🔧 <strong>Low Match.</strong> Significant gaps detected. Consider upskilling or targeting a different role.</div>', unsafe_allow_html=True)

            if gaps["missing_skills"]:
                st.markdown(f'<div class="tip-box">📚 <strong>Skills to add/learn:</strong> {", ".join(gaps["missing_skills"][:8])}. Consider adding relevant projects or certifications that demonstrate these.</div>', unsafe_allow_html=True)

            st.markdown('<div class="tip-box">✍️ <strong>Keyword Tip:</strong> Use exact keywords from the JD in your resume — ATS systems do exact matching. Even if you have the skill, use the same terminology.</div>', unsafe_allow_html=True)
            st.markdown('<div class="tip-box">📊 <strong>Quantify achievements:</strong> Add metrics to your bullet points. "Improved model accuracy by 15%" is stronger than "improved model accuracy".</div>', unsafe_allow_html=True)

        # ── SCORE VERDICT ─────────────────────────────────────────────────────
        st.markdown("---")
        verdict = "🟢 Strong Fit" if overall_score >= 75 else "🟡 Moderate Fit" if overall_score >= 50 else "🔴 Weak Fit"
        st.markdown(f"""
        <div style="text-align:center; padding: 1.5rem;">
            <div style="font-family:'DM Mono',monospace; color:#6b7280; font-size:0.85rem; letter-spacing:2px; text-transform:uppercase;">Overall Verdict</div>
            <div style="font-family:'Syne',sans-serif; font-size:2rem; font-weight:800; margin-top:0.5rem;">{verdict}</div>
            <div style="color:#6b7280; font-size:0.85rem; margin-top:0.5rem;">Match Score: <strong style="color:#00f5a0;">{overall_score}%</strong></div>
        </div>
        """, unsafe_allow_html=True)
