import streamlit as st
import requests
import base64
from helpers import parse_cv, extract_keywords

# -------------------- CONFIG -------------------
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = "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"

st.set_page_config(page_title="HireMeBro 🚀", layout="centered")

# Set background
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

set_bg_from_local("img6.jpg")

# ----------------- FUNCTIONS -------------------

def fetch_remotive_jobs(keywords, limit=10):
    jobs = []
    url = "https://www.arbeitnow.com/api/job-board-api"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        for job in data.get("data", []):
            title = job.get("title", "").lower()
            description = job.get("description", "").lower()

            if any(keyword.lower() in title or keyword.lower() in description for keyword in keywords):
                jobs.append({
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "location": job.get("location"),
                    "description": job.get("description"),
                    "link": job.get("url")
                })

            if len(jobs) >= limit:
                break

    except requests.RequestException as e:
        st.warning(f"⚠️ Uh-oh! Couldn't fetch jobs: {e}")
    except ValueError:
        st.warning("⚠️ Received invalid JSON response from Arbeitnow API.")

    return jobs

def generate_cover_letter(name, job_title, experience, skills, job_description):
    headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://yourappname.streamlit.app",
    "X-Title": "HireMeBro App"
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
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(OPENROUTER_API_URL, headers=headers, json=body)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

# ----------------- MAIN APP -------------------

def main():
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style="
            font-size: 3.5em;
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364); 
            -webkit-background-clip: text;
            color: white;
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            text-shadow: 1px 1px 2px #000000;
            animation: fadeIn 2s;
        ">
            HireMeBro
        </h1>
        <p style='font-size: 1.2em; color: #555;'>Your AI-powered bestie for job hunting </p>
    </div>

    <style>
    @keyframes fadeIn {
      from {opacity: 0;}
      to {opacity: 1;}
    }
    </style>
""", unsafe_allow_html=True)

    st.markdown("### Upload Your CV")
    uploaded_file = st.file_uploader("Drop your CV here 👇", type=["pdf"])

    if uploaded_file:
        cv_path = "uploaded_cv.pdf"
        with open(cv_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("🎉 CV uploaded successfully!")

        cv_text = parse_cv(cv_path)
        st.markdown("<h4 style='color: #f5f5f5;'>🔍 Extracted CV Text</h4>", unsafe_allow_html=True)
        st.text_area("Here's what we read from your resume ✨", cv_text, height=200)

        # ⬇️ Detect name automatically from CV
        cv_lines = cv_text.strip().split("\n")
        name = cv_lines[0] if cv_lines else ""
        
        # Capitalize name properly (if it exists)
        name = " ".join([word.capitalize() for word in name.split()]) if name else ""
        st.success(f"👤 Detected Name: {name}")

        keywords = extract_keywords(cv_text)

        st.markdown("### 🧠 Top Keywords from Your CV")
        st.success("✨ " + ", ".join(keywords))

        st.markdown("### 🚀 Remote Jobs Just for You")
        jobs = fetch_remotive_jobs(keywords)

        if jobs:
            for idx, job in enumerate(jobs):
                with st.expander(f"💼 {job['title']} at {job['company']}"):
                    st.write(f"📍 Location: {job['location']}")
                    st.markdown(f"[🔗 View Job Posting]({job['link']})", unsafe_allow_html=True)
                    
                    if st.button(f"Generate Cover Letter for {job['title']} ({idx})"):
                        if not name:
                            st.warning("⚠️ Please upload a valid CV to auto-detect your name.")
                        else:
                            with st.spinner("Generating your awesome cover letter..."):
                                cover_letter = generate_cover_letter(
                                    name=name,
                                    job_title=job['title'],
                                    experience="Based on my CV and past experience.",
                                    skills=", ".join(keywords),
                                    job_description=job['description']
                                )
                                st.subheader("📝 Your AI-Generated Cover Letter")
                                st.text_area("Cover Letter", cover_letter, height=300)
                                st.download_button("📥 Download Cover Letter", cover_letter, file_name=f"{job['title']}_cover_letter.txt")
        else:
            st.info("😓 No jobs matched. Try uploading a different CV or updating your skills!")

    else:
        st.info("📎 Upload your CV above to get started!")

# ---------------- RUN APP ----------------

if __name__ == "__main__":
    main()
