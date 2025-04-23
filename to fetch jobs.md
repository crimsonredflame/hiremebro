Import necessary libraries
 import streamlit as st
 from helpers import parse_cv, extract_keywords
 import requests
 
 # ----------------------------------------
 # Function to fetch jobs from Remotive API
 # ----------------------------------------
 def fetch_remotive_jobs(keywords, limit=10):
     """
     Fetch jobs from Remotive based on extracted keywords.
     """
     jobs = []
     for keyword in keywords:
         # API call to Remotive job board
         url = f"https://wellfound.com//api/remote-jobs?search={keyword}&limit={limit}"
         try:
             response = requests.get(url)
             response.raise_for_status()
             data = response.json()
 
             # Append each job to the jobs list
             for job in data.get("jobs", []):
                 jobs.append({
                     "title": job.get("title"),
                     "company": job.get("company_name"),
                     "location": job.get("candidate_required_location"),
                     "link": job.get("url")
                 })
         except requests.RequestException as e:
             st.warning(f"❌ Error fetching jobs for '{keyword}': {e}")
     return jobs
 
 # ----------------------------
 # Main Streamlit UI starts here
 # ----------------------------
 def main():
     # Set the app title
     st.title("💼 AI-Powered Job Finder from Your CV")
     st.write("Upload your resume and get matched with remote jobs based on your profile.")
 
     # Upload section
     uploaded_file = st.file_uploader("📄 Upload your CV (PDF format only)", type=["pdf"])
 
     if uploaded_file is not None:
         # Save the uploaded file to disk
         cv_path = "uploaded_cv.pdf"
         with open(cv_path, "wb") as f:
             f.write(uploaded_file.read())
         st.success("✅ CV uploaded successfully!")
 
         # Step 1: Parse the CV text
         cv_text = parse_cv(cv_path)
         st.subheader("📄 CV Content (Extracted Text)")
         st.text_area("Extracted Text", cv_text, height=200)
 
         # Step 2: Extract keywords
         keywords = extract_keywords(cv_text)
         st.subheader("🧠 Extracted Keywords from CV")
         st.write(", ".join(keywords))
 
         # Step 3: Fetch jobs from Remotive
         st.subheader("🌍 Matching Remote Job Listings")
         jobs = fetch_remotive_jobs(keywords)
 
         if jobs:
             for job in jobs:
                 with st.expander(f"{job['title']} at {job['company']}"):
                     st.write(f"📍 Location: {job['location']}")
                     st.markdown(f"[🔗 View Job Posting]({job['link']})")
         else:
             st.info("No jobs found for the extracted keywords. Try uploading a more detailed CV.")
 
 # ----------------------------
 # Run the app
 # ----------------------------
 if __name__ == "__main__":
     main()
