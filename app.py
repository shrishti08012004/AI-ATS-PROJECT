import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from read_resume import extract_text
from skill_gap import get_skill_gap
from svm_model import train_svm, predict_match

# ---------------- LOAD ML ----------------
model, vectorizer = train_svm()

# ---------------- PAGE ----------------
st.set_page_config(page_title="Smart ATS Dashboard", layout="wide")

st.markdown("""
<div style='background:linear-gradient(135deg,#667eea,#764ba2);
padding:35px;border-radius:18px;color:white;text-align:center'>
<h1>🤖 Smart ATS Resume Screening Dashboard</h1>
<p>ATS + Machine Learning + Analytics</p>
</div>
""", unsafe_allow_html=True)

# ---------------- MENU ----------------
# Using Streamlit builtin sidebar selectbox instead of external package
st.sidebar.title("Navigation")
selected = st.sidebar.selectbox("Mode", ["Single Resume", "Bulk Screening"]) 

# =========================================================
# 👤 SINGLE RESUME MODE
# =========================================================
if selected == "Single Resume":

    st.header("👤 Resume Analysis")

    col1, col2 = st.columns([1,2])

    with col1:
        file = st.file_uploader("Upload Resume", type=["pdf"])

    with col2:
        jd = st.text_area("Paste Job Description")

    if st.button("Analyze"):

        if file and jd:
            with open("temp.pdf", "wb") as f:
                f.write(file.read())

            resume_text = extract_text("temp.pdf")

            score, matched, missing = get_skill_gap(resume_text, jd)
            prediction, confidence = predict_match(model, vectorizer, resume_text, jd)

            st.metric("ATS Score", f"{score}%")

            if prediction == 1:
                st.success(f"ML Verdict: Good Match ({confidence}% confidence)")
            else:
                st.error(f"ML Verdict: Low Match ({confidence}% confidence)")

# =========================================================
# 👥 BULK SCREENING MODE
# =========================================================
elif selected == "Bulk Screening":

    st.header("👥 Bulk Resume Analyzer")

    files = st.file_uploader(
        "Upload Multiple Resumes",
        type=["pdf"],
        accept_multiple_files=True
    )

    jd_bulk = st.text_area("Paste Job Description")

    if st.button("Analyze All"):

        if files and jd_bulk:

            data = []
            progress = st.progress(0)

            for i, f in enumerate(files):

                name = f.name
                temp_file = f"temp_{i}.pdf"

                with open(temp_file, "wb") as file:
                    file.write(f.read())

                resume_text = extract_text(temp_file)

                score, matched, missing = get_skill_gap(resume_text, jd_bulk)
                prediction, confidence = predict_match(model, vectorizer, resume_text, jd_bulk)

                data.append({
                    "Resume": name,
                    "Score": score,
                    "Prediction": "Good Match" if prediction==1 else "Low Match",
                    "Confidence": confidence
                })

                progress.progress((i+1)/len(files))

            df = pd.DataFrame(data)

            st.dataframe(df)

            # ⭐ Candidate Ranking Chart
            st.subheader("📊 Candidate Ranking")

            fig = plt.figure()
            plt.bar(df["Resume"], df["Score"])
            plt.xticks(rotation=90)
            plt.ylabel("ATS Score")
            st.pyplot(fig)

            # ⭐ CSV Export
            csv = df.to_csv(index=False).encode()
            st.download_button("📥 Download Shortlist CSV", csv, "shortlist.csv")

            # ⭐ Heatmap
            st.subheader("🔥 Resume Score Heatmap")

            heatmap_fig = plt.figure()
            sns.heatmap(df[["Score", "Confidence"]], annot=True)
            st.pyplot(heatmap_fig)