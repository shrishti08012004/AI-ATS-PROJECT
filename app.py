import streamlit as st
import os
from read_resume import extract_text
from text_cleaner import clean_text
from matcher import calculate_score
from skill_gap import get_skill_gap

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI ATS Resume Screener",
    page_icon="📄",
    layout="wide"
)

# ---------------- HERO SECTION ----------------
def hero_section():
    st.markdown("""
    <div style='
        background: linear-gradient(135deg,#6C63FF,#4B0082);
        padding:50px;
        border-radius:18px;
        text-align:center;
        color:white;
        margin-bottom:25px;
    '>
        <h1>🚀 AI ATS Resume Screening System</h1>
        <p style='font-size:20px;'>Upload resumes • Match with job • Find best candidates instantly</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- PDF REPORT ----------------
def generate_pdf(score, matched, missing):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "ATS Resume Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"ATS Score: {score}%")
    c.drawString(50, height - 130, "Matched Skills: " + (", ".join(matched) if matched else "None"))
    c.drawString(50, height - 160, "Missing Skills: " + (", ".join(missing) if missing else "None"))

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📄 Single Resume", "📂 Bulk Resume Screening"]
)

# =========================================================
# 🏠 HOME PAGE
# =========================================================
if page == "🏠 Home":
    hero_section()
    st.markdown("### 💡 What this system does")
    st.info("""
    ✔ Checks ATS compatibility  
    ✔ Finds missing skills  
    ✔ Filters best candidates  
    ✔ Works on 1000+ resumes automatically
    """)

# =========================================================
# 📄 SINGLE RESUME ANALYZER
# =========================================================
elif page == "📄 Single Resume":

    st.header("📄 Single Resume ATS Analyzer")

    col1, col2 = st.columns([1,2])

    with col1:
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    with col2:
        job_desc = st.text_area("Paste Job Description")

    if st.button("Analyze Resume"):

        if uploaded_file is None or job_desc.strip() == "":
            st.warning("Please upload resume and paste job description")
        else:
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.read())

            resume_text = clean_text(extract_text("temp.pdf"))
            job_clean = clean_text(job_desc)

            score = calculate_score(resume_text, job_clean)
            matched, missing = get_skill_gap(resume_text, job_clean)

            st.subheader("ATS Match Score")
            st.progress(score/100)
            st.metric("Score", f"{score}%")

            c1, c2 = st.columns(2)
            with c1:
                st.success("Matched Skills")
                st.write(", ".join(matched) if matched else "None")

            with c2:
                st.error("Missing Skills")
                st.write(", ".join(missing) if missing else "None")

            pdf_buffer = generate_pdf(score, matched, missing)
            st.download_button("Download Report", pdf_buffer, "ATS_Report.pdf")

# =========================================================
# 📂 BULK RESUME ANALYZER
# =========================================================
elif page == "📂 Bulk Resume Screening":

    st.header("📂 Bulk Resume Screening (HR Mode)")

    uploaded_files = st.file_uploader(
        "Upload Multiple Resumes",
        type=["pdf"],
        accept_multiple_files=True
    )

    job_desc = st.text_area("Paste Job Description For All Candidates")

    if st.button("Analyze All Resumes"):

        if not uploaded_files or job_desc.strip()=="":
            st.warning("Upload resumes and paste job description")
        else:
            job_clean = clean_text(job_desc)

            results = []
            progress = st.progress(0)

            for i, file in enumerate(uploaded_files):

                filename = f"temp_{i}.pdf"
                with open(filename, "wb") as f:
                    f.write(file.read())

                resume_text = clean_text(extract_text(filename))
                score = calculate_score(resume_text, job_clean)
                matched, missing = get_skill_gap(resume_text, job_clean)

                results.append((file.name, score, matched, missing))

                progress.progress((i+1)/len(uploaded_files))

            st.success("Analysis Completed!")

            st.subheader("🏆 Top Candidates")

            results.sort(key=lambda x: x[1], reverse=True)

            for name, score, matched, missing in results:
                if score >= 60:
                    with st.expander(f"{name} — {score}%"):
                        st.write("Matched:", ", ".join(matched))
                        st.write("Missing:", ", ".join(missing))
