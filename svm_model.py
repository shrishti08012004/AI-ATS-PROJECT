import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC


def train_svm():
    data = pd.read_csv("training_data.csv")

    X = data["resume"] + " " + data["jd"]
    y = data["label"]

    vectorizer = TfidfVectorizer()
    X_vectors = vectorizer.fit_transform(X)

    model = SVC(kernel="linear", probability=True)
    model.fit(X_vectors, y)

    return model, vectorizer


def predict_match(model, vectorizer, resume_text, jd_text):
    combined = [resume_text + " " + jd_text]
    vector = vectorizer.transform(combined)

    prediction = model.predict(vector)
    probability = model.predict_proba(vector)

    confidence = round(max(probability[0]) * 100, 2)

    return prediction[0], confidence