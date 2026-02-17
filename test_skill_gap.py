from read_resume import extract_text
from text_cleaner import clean_text
from skill_gap import find_skill_gap

resume = clean_text(extract_text("resume.pdf"))

job_description = """
Python SQL API debugging communication problem solving
"""

job_description = clean_text(job_description)

matched, missing = find_skill_gap(resume, job_description)

print("\nMATCHED SKILLS:")
print(matched)

print("\nMISSING SKILLS:")
print(missing)
