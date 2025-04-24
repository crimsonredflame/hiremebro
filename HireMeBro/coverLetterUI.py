import streamlit as st
import requests

# Set the base URL for OpenRouter
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = "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"
st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")

import base64

def set_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    background = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(background, unsafe_allow_html=True)

# Set background
set_bg_from_local("5. cm per second.jpg")


# Function to generate cover letter via OpenRouter
def generate_cover_letter(name, job_title, experience, skills, job_description):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Write a personalized cover letter for a job application.

    Name: {name}
    Job Title: {job_title}
    Experience: {experience}
    Skills: {skills}
    Job Description: {job_description}

    The tone should be professional, enthusiastic, and tailored to the job.
    """

    body = {
        "model": "openai/gpt-3.5-turbo",  # You can change this to another model available on OpenRouter
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(OPENROUTER_API_URL, headers=headers, json=body)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

# Streamlit UI

st.title("💌 AI Cover Letter Generator")
st.markdown("Generate a professional and tailored cover letter using your details.")

with st.form("cover_letter_form"):
    name = st.text_input("Your Name")
    job_title = st.text_input("Job Title You’re Applying For")
    experience = st.text_area("Brief Description of Your Experience")
    skills = st.text_area("Skills Relevant to the Job")
    job_description = st.text_area("Paste the Job Description")

    submitted = st.form_submit_button("Generate Cover Letter")

if submitted:
    with st.spinner("Generating your cover letter..."):
        letter = generate_cover_letter(name, job_title, experience, skills, job_description)
        st.subheader("📝 Your AI-Generated Cover Letter")
        st.text_area("Cover Letter", letter, height=300)
        st.download_button("📥 Download Cover Letter", letter, file_name="cover_letter.txt")
