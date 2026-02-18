import nltk
from nltk.corpus import stopwords
import re

nltk.download('stopwords')

STOPWORDS = set(stopwords.words('english'))

# 🔥 IMPORTANT: Skill database (you can expand later)
SKILL_DATABASE = {
    "python","java","c","c++","sql","mysql","mongodb",
    "html","css","javascript","react","node","flask","django",
    "machine","learning","data","analysis","api","git",
    "github","communication","problem","solving","debugging"
}

def clean_text(text):
    text = text.lower()
    text = re.findall(r'\b[a-zA-Z]+\b', text)
    return [word for word in text if word not in STOPWORDS]

def extract_skills(text):
    words = clean_text(text)
    return set(word for word in words if word in SKILL_DATABASE)

def get_skill_gap(resume_text, job_desc):

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_desc)

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    # ⭐ Correct ATS Score
    if len(jd_skills) == 0:
        score = 0
    else:
        score = round((len(matched) / len(jd_skills)) * 100, 2)

    return score, list(matched), list(missing)
