import pdfplumber

def extract_text(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


# testing
if __name__ == "__main__":
    resume_text = extract_text("resume.pdf")
    print(resume_text)
