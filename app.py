import streamlit as st
from read_resume import extract_text
from text_cleaner import clean_text
from matcher import calculate_score
from skill_gap import find_skill_gap
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Page config
st.set_page_config(
    page_title="AI ATS Resume Screener",
    page_icon="📄",
    layout="wide"
)

# Header
st.markdown("<h1 style='text-align: center; color: #4B0082;'>📄 AI ATS Resume Screener</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Upload your resume & paste job description to check ATS score and skill gaps</p>", unsafe_allow_html=True)
st.write("---")

# Columns for Upload & Job Description
col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("📁 Upload Resume (PDF)", type=["pdf"])
with col2:
    job_desc = st.text_area("📝 Paste Job Description Here")

st.write("---")

# PDF Generator function
def generate_pdf(score, matched, missing):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "📄 ATS Resume Report")

    # Score
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"✅ ATS Match Score: {score}%")

    # Matched Skills
    c.drawString(50, height - 130, "💡 Matched Skills: " + (", ".join(matched) if matched else "None"))

    # Missing Skills
    c.drawString(50, height - 160, "❌ Missing Skills: " + (", ".join(missing) if missing else "None"))

    # Finish
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# Analyze Button
if st.button("Analyze"):

    if uploaded_file is None or job_desc.strip() == "":
        st.warning("⚠️ Please upload resume and enter job description!")
    else:
        # Save uploaded resume temporarily
        with open("temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.read())

        # Step 1: Read resume
        resume_text = extract_text("temp_resume.pdf")

        # Step 2: Clean text
        resume_text = clean_text(resume_text)
        job_clean = clean_text(job_desc)

        # Step 3: Calculate ATS Score
        score = calculate_score(resume_text, job_clean)

        # Show Score
        st.subheader("✅ ATS Match Score")
        st.progress(score / 100)
        st.metric(label="Score (%)", value=f"{score}%")

        # Step 4: Skill Gap
        matched, missing = find_skill_gap(resume_text, job_clean)
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("💡 Matched Skills")
            st.write(", ".join(matched) if matched else "None")
        with col4:
            st.subheader("❌ Missing Skills")
            st.write(", ".join(missing) if missing else "None")

        # Step 5: PDF Download Button
        pdf_buffer = generate_pdf(score, matched, missing)
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_buffer,
            file_name="ATS_Report.pdf",
            mime="application/pdf"
        )

        # Step 6: Placeholder for AI Suggestions
        st.write("---")
        st.info("🤖 AI suggestions will appear here once API credits are added")
