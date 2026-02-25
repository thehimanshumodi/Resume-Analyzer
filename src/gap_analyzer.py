"""
Gap Analyzer — Compares skills extracted from resume vs. job description
and categorizes them as: matched, missing, or extra.
"""

from typing import Dict, List
from src.ner_extractor import extract_tech_skills


def normalize(skill: str) -> str:
    """Lowercase and strip for comparison."""
    return skill.lower().strip()


def analyze_gaps(resume_entities: Dict, jd_entities: Dict) -> Dict[str, List[str]]:
    """
    Compare skills between resume and JD.

    Returns:
        - matched_skills: skills in both resume and JD
        - missing_skills: skills in JD but NOT in resume  ← most important
        - extra_skills:   skills in resume but NOT in JD  (good to know)
    """
    resume_skills = set(normalize(s) for s in resume_entities.get("Technical Skills", []))
    jd_skills = set(normalize(s) for s in jd_entities.get("Technical Skills", []))

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    extra = resume_skills - jd_skills

    def prettify(skill_set):
        return sorted([s.title() if len(s) > 3 else s.upper() for s in skill_set])

    return {
        "matched_skills": prettify(matched),
        "missing_skills": prettify(missing),
        "extra_skills":   prettify(extra),
        "jd_skill_count": len(jd_skills),
        "resume_skill_count": len(resume_skills),
    }
