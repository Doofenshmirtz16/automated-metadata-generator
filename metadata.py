import re
from keybert import KeyBERT
from transformers import pipeline

# Load NLP models
kw_model = KeyBERT(model="all-MiniLM-L6-v2")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
classifier = pipeline("zero-shot-classification")

def extract_title(text: str) -> str:
    """
    Extract a potential title from the first lines of text.
    """
    for line in text.split("\n"):
        line = line.strip()
        if 5 <= len(line.split()) <= 15:
            return line
    return "Untitled Document"

def extract_summary(text: str, max_chars: int = 1024) -> str:
    """
    Generate a short summary using a transformer model.
    """
    short_text = text[:max_chars]
    result = summarizer(short_text, max_length=130, min_length=30, do_sample=False)
    return result[0]['summary_text']

def extract_keywords(text: str, top_n: int = 5) -> list:
    """
    Use KeyBERT to extract important keywords.
    """
    keywords = kw_model.extract_keywords(text, top_n=top_n)
    return [kw[0] for kw in keywords]

def extract_date(text: str) -> str:
    """
    Extract a date from text using common formats.
    """
    pattern = r"\b(?:\d{1,2}[\-/th|st|nd|rd\s])?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\-]?\d{2,4}\b|\b\d{4}[-/]\d{2}[-/]\d{2}\b"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return match.group(0) if match else "Not found"

def detect_document_type(text: str) -> str:
    """
    Classify document type using zero-shot classification.
    """
    candidate_labels = [
        "research paper", "resume", "declaration form",
        "invoice", "application", "academic transcript",
        "report", "general document"
    ]
    result = classifier(text[:1024], candidate_labels)
    return result["labels"][0]

def generate_metadata(text: str) -> dict:
    """
    Generate all metadata fields from raw extracted text.
    """
    if not text.strip():
        return {
            "title": "No content",
            "summary": "No summary generated.",
            "keywords": [],
            "document_type": "Unknown",
            "detected_date": "Not found"
        }

    return {
        "title": extract_title(text),
        "summary": extract_summary(text),
        "keywords": extract_keywords(text),
        "document_type": detect_document_type(text),
        "detected_date": extract_date(text)
    }
