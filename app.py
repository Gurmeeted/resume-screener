import streamlit as st
import openai
import PyPDF2

st.set_page_config(page_title="AI Resume Screener", layout="centered")

st.title("AI Resume Screener")
st.markdown("Upload your resume + enter the job title to get a match score and suggestions.")

openai.api_key = st.secrets["OPENAI_API_KEY"]

uploaded_file = st.file_uploader("Upload PDF Resume", type="pdf")
job_title = st.text_input("Job title you're applying for")

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    return "\n".join(page.extract_text() for page in pdf_reader.pages)

if uploaded_file and job_title:
    resume_text = extract_text_from_pdf(uploaded_file)

    prompt = f"""
    Evaluate the resume below for the job: {job_title}. 
    Give a match score (0–100), strengths, weaknesses, and 3 improvements.

    Resume:
    {resume_text}
    """

    with st.spinner("Analyzing..."):
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        st.success("Analysis Ready!")
        st.write(res['choices'][0]['message']['content'])
