from read_resume import extract_text
from text_cleaner import clean_text
from ai_feedback import get_ai_feedback

resume = clean_text(extract_text("resume.pdf"))

job = """
Looking for Python developer with SQL, API, debugging and communication skills
"""

job = clean_text(job)

result = get_ai_feedback(resume, job)

print(result)
