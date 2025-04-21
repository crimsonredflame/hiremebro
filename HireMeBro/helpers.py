import fitz  # PyMuPDF
import re
import spacy
from collections import Counter

# Load the spaCy English language model
# You must install it first using: python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

def parse_cv(file_path):
    """
    Parses a PDF CV file and extracts raw text content.
    Returns the extracted text.
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()  # Extract text from each page
        doc.close()
        return text
    except Exception as e:
        print(f"Error while reading the CV file: {e}")
        return None  # Return None if file reading fails

def extract_keywords(text, num_keywords=10):
    """
    Extracts top N keywords using spaCy for tokenization and stop word removal.
    - Tokenizes using spaCy
    - Filters stop words, punctuation, and non-alphabetic tokens
    - Counts frequency of remaining words and returns top N
    """
    if not text:
        print("No text provided for keyword extraction.")
        return []

    doc = nlp(text.lower())  # Convert text to lowercase and process with spaCy

    # Keep tokens that are alphabetic, not stopwords, and not punctuations
    filtered_tokens = [
        token.text for token in doc 
        if token.is_alpha and not token.is_stop
    ]

    # Count the most common tokens
    token_freq = Counter(filtered_tokens)
    common_keywords = [word for word, freq in token_freq.most_common(num_keywords)]

    return common_keywords
