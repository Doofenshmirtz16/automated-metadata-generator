import os
import fitz
import docx
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from odf.opendocument import load
from odf.text import P
from bs4 import BeautifulSoup
from striprtf.striprtf import rtf_to_text

# Paths (Update if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
poppler_path = r"C:\Program Files\poppler-24.08.0\Library\bin"

# Format-specific extractors
def extract_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_ocr_from_pdf(file_path):
    images = convert_from_path(file_path, poppler_path=poppler_path)
    return "\n".join([pytesseract.image_to_string(img) for img in images])

def extract_text_from_image(file_path):
    return pytesseract.image_to_string(Image.open(file_path))

def extract_from_odt(file_path):
    text = ""
    doc = load(file_path)
    for paragraph in doc.getElementsByType(P):
        text += paragraph.firstChild.data if paragraph.firstChild else ""
        text += "\n"
    return text

def extract_from_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    return soup.get_text(separator="\n")

def extract_from_rtf(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return rtf_to_text(f.read())

# Unified dispatcher with smart fallback
def extract_text(file_path, force_ocr=False):
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".txt":
        return extract_from_txt(file_path)
    elif ext == ".docx":
        return extract_from_docx(file_path)
    elif ext == ".odt":
        return extract_from_odt(file_path)
    elif ext in [".html", ".htm"]:
        return extract_from_html(file_path)
    elif ext == ".rtf":
        return extract_from_rtf(file_path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(file_path)
    elif ext == ".pdf":
        if force_ocr:
            print("🔁 Force OCR enabled.")
            return extract_text_ocr_from_pdf(file_path)

        # Heuristic 1: Check file size
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > 3.0:
            print(f"📦 Large file size ({size_mb:.2f} MB) — assuming scanned → OCR")
            return extract_text_ocr_from_pdf(file_path)

        # Heuristic 2: Check text density
        text = ""
        with fitz.open(file_path) as doc:
            total_chars = 0
            for page in doc:
                page_text = page.get_text()
                text += page_text
                total_chars += len(page_text)
            avg_chars = total_chars / len(doc)
            print(f"📊 Avg characters per page: {avg_chars:.2f}")

        if avg_chars < 50:
            print("🧠 Low content density — forcing OCR...")
            return extract_text_ocr_from_pdf(file_path)

        # Heuristic 3: Final fallback
        if len(text.strip()) < 100:
            print("🔁 Very little text extracted — final OCR fallback")
            return extract_text_ocr_from_pdf(file_path)

        return text
    else:
        raise ValueError(f"Unsupported file type: {ext}")
