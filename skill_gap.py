def find_skill_gap(resume_text, job_text):

    resume_words = set(resume_text.split())
    job_words = set(job_text.split())

    matched = resume_words.intersection(job_words)
    missing = job_words - resume_words

    return list(matched), list(missing)
