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

def extract_summary(text: str, max_chars: int = 2048) -> str:
    """
    Generate a short summary using a transformer model.
    """
    short_text = text[:max_chars]
    result = summarizer(short_text, max_length=250, min_length=60, do_sample=False)
    return result[0]['summary_text']

def extract_keywords(text: str, top_n: int = 15) -> list:
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
    return {label: score for label, score in zip(result["labels"], result["scores"])}

def generate_metadata(text):
    if not text.strip():
        return {
            "title": "No content",
            "summary": "",
            "keywords": [],
            "keyword_scores": {},
            "document_type_scores": {},
            "detected_date": "Not found"
        }

    title = extract_title(text)
    summary = extract_summary(text)
    keywords = extract_keywords(text, top_n=15)
    date = extract_date(text)
    doc_type_scores = detect_document_type(text)

    return {
        "title": title,
        "summary": summary,
        "keywords": list(doc_type_scores.keys())[:1],  # for backward compatibility
        "keyword_scores": {kw: round(score, 3) for kw, score in kw_model.extract_keywords(text, top_n=15)},
        "document_type_scores": doc_type_scores,
        "detected_date": date
    }
