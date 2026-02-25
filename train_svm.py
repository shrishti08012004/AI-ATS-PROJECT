import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVR

# Dummy training data (simple examples)
resumes = [
    "python machine learning data analysis pandas numpy",
    "java spring boot microservices backend api",
    "html css javascript react frontend ui",
    "python flask api backend sql",
    "react javascript frontend web development"
]

scores = [90, 75, 80, 85, 70]  # Example ATS scores

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(resumes)

model = SVR()
model.fit(X, scores)

# Save model
with open("svm_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("✅ ML Model Trained & Saved!")