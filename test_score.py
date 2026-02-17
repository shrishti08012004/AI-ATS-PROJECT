from read_resume import extract_text
from text_cleaner import clean_text
from matcher import calculate_score

# Step 1: read resume
resume = extract_text("resume.pdf")

# Step 2: clean resume
resume = clean_text(resume)

# Step 3: write job description
job_description = """
We are looking for a Python developer with SQL, APIs,
problem solving, debugging and communication skills.
"""

job_description = clean_text(job_description)

# Step 4: calculate ATS score
score = calculate_score(resume, job_description)

print("\nATS MATCH SCORE:", score, "%")
