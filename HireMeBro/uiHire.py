# 🌈 Gen Z Inspired Job Finder UI using Streamlit

import streamlit as st
from helpers import parse_cv, extract_keywords
import requests
st.set_page_config(page_title="HireMeBro 🚀", layout="centered")
# ----------------------------------------
# Function to fetch jobs from Remotive API
# ----------------------------------------

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
set_bg_from_local("img5.jpg")


def fetch_remotive_jobs(keywords, limit=10):
    jobs = []
    url = "https://www.arbeitnow.com/api/job-board-api"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        for job in data.get("data", []):  # The key is "data"
            title = job.get("title", "").lower()
            description = job.get("description", "").lower()

            # Check if any keyword appears in title or description
            if any(keyword.lower() in title or keyword.lower() in description for keyword in keywords):
                jobs.append({
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "location": job.get("location"),
                    "link": job.get("url")
                })

            if len(jobs) >= limit:
                break

    except requests.RequestException as e:
        st.warning(f"⚠️ Uh-oh! Couldn't fetch jobs: {e}")
    except ValueError:
        st.warning("⚠️ Received invalid JSON response from Arbeitnow API.")

    return jobs


# ----------------------------
# Main Streamlit UI starts here
# ----------------------------
def main():
    # 💫 Page Config
    

    # 💜 Gradient-style custom header
    st.markdown("""
        <div style='text-align:center'>
            <h1 style='font-size: 3em; background: linear-gradient(to right, #ff00cc, #3333ff); 
            -webkit-background-clip: text; color: transparent;'>HireMeBro 🔍✨</h1>
            <p style='font-size: 1.2em; color: #444;'>Your AI-powered bestie for job hunting 👯‍♀️</p>
        </div>
    """, unsafe_allow_html=True)

    # 📎 File Upload Section
    st.markdown("### 📤 Upload Your CV")
    st.caption("PDF only. We'll read it like a pro and match you to awesome jobs 💼")
    uploaded_file = st.file_uploader("Drop your CV here 👇", type=["pdf"])

    if uploaded_file:
        # Save the file
        cv_path = "uploaded_cv.pdf"
        with open(cv_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("🎉 CV uploaded successfully!")

        # 🧾 Step 1: Parse CV
        cv_text = parse_cv(cv_path)
        st.markdown("### 🔍 Extracted CV Text")
        st.text_area("Here's what we read from your resume ✨", cv_text, height=200)

        # 🧠 Step 2: Extract Keywords
        keywords = extract_keywords(cv_text)
        st.markdown("### 🧠 Top Keywords from Your CV")
        st.success("✨ " + ", ".join(keywords))

        # 🌐 Step 3: Fetch Jobs
        st.markdown("### 🚀 Remote Jobs Just for You")
        jobs = fetch_remotive_jobs(keywords)

        if jobs:
            for job in jobs:
                with st.expander(f"💼 {job['title']} at {job['company']}"):
                    st.write(f"📍 Location: {job['location']}")
                    st.markdown(f"[🔗 View Job Posting]({job['link']})", unsafe_allow_html=True)
        else:
            st.info("😓 No jobs matched. Try uploading a different CV or updating your skills!")

    else:
        st.info("📎 Upload your CV above to get started!")

# ----------------------------
# Run the app
# ----------------------------
if __name__ == "__main__":
    main()
