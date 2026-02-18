import streamlit as st

def hero_section():
    st.markdown("""
        <style>
        .hero {
            padding: 30px;
            border-radius: 18px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-align: center;
        }
        </style>

        <div class="hero">
            <h1>🤖 Smart ATS Resume Analyzer</h1>
            <p>Upload resume • Match skills • Get instant shortlist</p>
        </div>
    """, unsafe_allow_html=True)
