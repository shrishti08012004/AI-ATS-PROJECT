# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# def calculate_score(resume_text, job_text):

#     documents = [resume_text, job_text]

#     vectorizer = TfidfVectorizer()
#     vectors = vectorizer.fit_transform(documents)

#     similarity = cosine_similarity(vectors[0], vectors[1])

#     score = similarity[0][0] * 100

#     return round(score, 2)

from svm_predictor import predict_score

def calculate_score(resume_text, job_desc):
    combined_text = resume_text + " " + job_desc
    return predict_score(combined_text)