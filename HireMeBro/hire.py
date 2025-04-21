# app.py

import os
import requests
from helpers import parse_cv, extract_keywords

def fetch_remotive_jobs(keywords, limit=10):
    """
    Fetch remote jobs from Remotive API based on provided keywords.
    """
    jobs = []
    for keyword in keywords:
        # Construct the API URL with the search parameter
        url = f"https://remotive.io/api/remote-jobs?search={keyword}&limit={limit}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            # Extract job listings from the response
            for job in data.get("jobs", []):
                jobs.append({
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "location": job.get("candidate_required_location"),
                    "link": job.get("url")
                })
        except requests.RequestException as e:
            print(f"Error fetching jobs for keyword '{keyword}': {e}")
    return jobs

def main():
    # Path to your resume
    cv_path = "cv.pdf"  # Replace with the actual file name

    # Step 1: Parse the CV to extract raw text
    cv_text = parse_cv(cv_path)
    print("✅ CV Parsed Successfully.\n")

    # Step 2: Extract keywords using NLP
    keywords = extract_keywords(cv_text)
    print(f"🧠 Extracted Keywords: {keywords}\n")

    # Step 3: Fetch remote jobs from Remotive based on extracted keywords
    jobs = fetch_remotive_jobs(keywords)
    print("📄 Job Listings:\n")
    for job in jobs:
        print(f"- {job['title']} at {job['company']} | {job['location']}\n  Link: {job['link']}")

if __name__ == "__main__":
    main()
