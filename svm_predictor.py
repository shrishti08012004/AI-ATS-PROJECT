import pickle

# Load model
with open("svm_model.pkl", "rb") as f:
    model, vectorizer = pickle.load(f)

def predict_score(text):
    X = vectorizer.transform([text])
    score = model.predict(X)[0]

    # Keep score between 0–100
    score = max(0, min(100, int(score)))
    return score