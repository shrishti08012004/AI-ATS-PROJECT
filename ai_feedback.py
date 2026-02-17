import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_feedback(resume, job):

    prompt = f"""
You are an ATS resume reviewer.

Compare the RESUME and JOB DESCRIPTION.

Give:
1) Missing skills explanation
2) Resume improvement tips
3) Project suggestions to add
4) Final HR advice

RESUME:
{resume}

JOB DESCRIPTION:
{job}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
