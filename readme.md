# 📄 Automated Metadata Generator using LLMs + OCR

This project is a Streamlit-based web app that automates **metadata extraction** from a wide range of documents using a combination of:

- ✅ Text extraction (PDF, DOCX, TXT, HTML, ODT, RTF, Images)
- 🔍 Intelligent OCR fallback (Tesseract + Poppler)
- 🧠 LLM/NLP models for:
  - Summarization (DistilBART)
  - Keyword extraction (KeyBERT)
  - Document classification (Zero-shot using BART)
  - Title and date detection

---

## Key Highlights
- Multi-format support: Extracts text from .pdf, .docx, .txt, .odt, .rtf, .html, and even .jpg/.png.

- LLM-powered intelligence: Uses state-of-the-art transformer models for summary, keywords, and classification.

- Automatic OCR fallback: If text extraction fails (e.g., scanned PDFs), the system automatically triggers OCR.

- Confidence scores: Includes classification and keyword relevance scores for transparency and analysis.

- Interactive web interface: User-friendly Streamlit app lets anyone upload and explore documents instantly.

- Notebook + API-ready: Modular design makes this pipeline reusable for backend, research, or production.

---

## 🚀 Live Demo Link

Try the deployed app here:  
👉 [View Streamlit App](https://automated-metadata-generator-pupnxetwvt3n2ektsetvzo.streamlit.app/)

---

## Video Demo Link
(in the form of google drive):
👉

---

## ✨ Features and their breakdown

| Feature                   | Description                                                                   |
| ------------------------- | ----------------------------------------------------------------------------- |
| 📂 Upload any document    | Choose from over 8 formats: PDF, DOCX, TXT, ODT, HTML, RTF, PNG, JPG          |
| 🔍 Smart OCR fallback     | If text length is short or content is scanned, OCR is triggered automatically |
| 🧠 LLM Metadata Generator | Generates: `title`, `summary`, `keywords`, `document type`, `date`            |
| 📊 Confidence Tables      | Keyword relevance + classification scores exported to CSV                     |
| 📥 Export Results         | JSON and CSV download buttons — perfect for further analysis                  |
| 🧪 Notebook Included      | End-to-end Jupyter notebook version with full explanations                    |
| 🚀 Live App Deployed      | Public Streamlit Cloud deployment with styled UI and sidebar controls         |


---

## 📁 Project Structure

automated-metadata-generator/

├── extract.py # Text extraction logic + OCR fallback

├── metadata.py # Metadata generation using LLMs

├── ui.py # Streamlit frontend app

├── notebook.ipynb # Jupyter notebook version of pipeline

├── requirements.txt # All dependencies

├── sample_docs/ # Example files

└── README.md # This file

---

## 🔧 Installation & Usage

### ⚙️ Requirements

- Python ≥ 3.8
- pip
- Tesseract OCR (optional if not using local OCR)
- Poppler (for `pdf2image`)

---

### 🛠️ Setup Instructions

#### 🖥️ Local (manual)
```
git clone https://github.com/yourusername/automated-metadata-generator.git
cd automated-metadata-generator
pip install -r requirements.txt
streamlit run ui.py
```

#### ☁️ Deployed
No setup needed — just open the web app link.

#### 📓 Run Notebook Instead
```
jupyter notebook notebook.ipynb
```
(Change the notebook name in your local computer as "notebook" and then run.)

Useful for exploring the pipeline, debugging, or submitting in academic settings.

---

### 🧠 Models Used
| Task                    | Model Used                     | Why It Was Chosen                        |
| ----------------------- | ------------------------------ | ---------------------------------------- |
| Keyword Extraction      | `KeyBERT` (`all-MiniLM-L6-v2`) | Lightweight yet semantically powerful    |
| Text Summarization      | `facebook/bart-large-cnn`      | High-quality abstractive summaries       |
| Document Classification | `facebook/bart-large-mnli`     | Zero-shot classification with 90+ labels |
| OCR                     | `Tesseract` + `Poppler`        | Industry-standard for image/PDF OCR      |

---

### 📥 Outputs Example
```
{
  "title": "Research Paper on ML for FRBs",
  "summary": "This study evaluates ML methods for classifying Fast Radio Bursts...",
  "keywords": ["Fast Radio Bursts", "ML", "clustering", "Spectral Clustering"],
  "keyword_scores": {
    "clustering": 0.845,
    "classification": 0.812,
    ...
  },
  "document_type_scores": {
    "research paper": 0.974,
    "resume": 0.021,
    ...
  },
  "detected_date": "23 Jun 2025"
}
```
### Please remember that we have set the limit on the number of values for each features so that it is easy for interpretation. If you want, you can easily extend the limits in metadata.py from finite to 'None' to include all.

---

### Example Use Cases
1. Academic paper analysis — auto-summarize research PDFs

2. Form/document classification — detect type of uploaded file

3. Knowledge indexing — generate keywords + summary for document search

4. Resume filtering — extract info from CVs in various formats

5. AI preprocessing — enrich raw text documents with semantic metadata

---

## Contributors
Sumit Sharma, Engineering Physics
23123042

---

## LICENSE
MIT License. Free for academic and personal use.
