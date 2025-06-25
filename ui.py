import streamlit as st
import os
import tempfile
import json
import pathlib
import pandas as pd

from extract import extract_text
from metadata import generate_metadata

SUPPORTED_TYPES = ["pdf", "docx", "txt", "jpg", "jpeg", "png", "odt", "html", "htm", "rtf"]

st.set_page_config(page_title="📄 Metadata Generator", layout="centered")

# --- Header ---
st.markdown("""
<style>
h1 {
    text-align: center;
    font-size: 2.4rem;
    color: #262730;
}
.stDownloadButton button {
    width: 100%;
    margin-bottom: 0.5rem;
}
.stTextArea textarea {
    font-size: 0.88rem;
    font-family: 'Courier New', monospace;
}
</style>
""", unsafe_allow_html=True)

st.title("📄 Automated Metadata Generator")
st.markdown("💡 Upload any document to extract **semantically rich metadata** using OCR + LLMs.")

# --- Upload Section ---
with st.sidebar:
    st.header("📁 Upload File")
    uploaded_file = st.file_uploader("Choose a document", type=SUPPORTED_TYPES)

    ocr_mode = st.radio(
        "OCR Mode",
        ["Auto (Recommended)", "Force OCR"],
        help="Force OCR if the document is scanned or image-based."
    )
    force_ocr = ocr_mode == "Force OCR"

if uploaded_file is not None:
    if uploaded_file.size == 0:
        st.warning("⚠️ Uploaded file is empty. Please select a valid document.")
        st.stop()

    suffix = pathlib.Path(uploaded_file.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    # --- Metadata Processing ---
    try:
        with st.spinner("🔍 Extracting and analyzing..."):
            text = extract_text(temp_path, force_ocr=force_ocr)

        if not text.strip():
            st.warning("⚠️ No text could be extracted from the file.")
        else:
            st.success("✅ Text extracted successfully!")

            # --- File Summary ---
            st.caption(f"📄 **File:** `{uploaded_file.name}` | Size: `{uploaded_file.size / 1024:.1f} KB` | OCR Mode: `{ocr_mode}`")

            # --- Text Preview ---
            with st.expander("📄 Preview Extracted Text"):
                st.text_area("Extracted Text", text, height=300)

            # --- Metadata Generation ---
            metadata = generate_metadata(text)

            st.markdown("---")
            st.subheader("🧠 Metadata Insights")

            for key, value in metadata.items():
                st.markdown(f"**🔹 {key.replace('_', ' ').title()}**")
                if isinstance(value, dict):
                    st.dataframe(pd.DataFrame(value.items(), columns=["Label", "Score"]))
                elif isinstance(value, list):
                    st.markdown(", ".join(value))
                else:
                    st.markdown(value)

            # --- Downloads ---
            json_data = json.dumps(metadata, indent=2)
            csv_df = pd.DataFrame(metadata.items(), columns=["Field", "Value"])

            st.markdown("---")
            st.subheader("📥 Download Metadata")
            st.download_button("⬇️ JSON Format", json_data, file_name="metadata.json", mime="application/json")
            st.download_button("⬇️ CSV Format", csv_df.to_csv(index=False).encode("utf-8"), file_name="metadata.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Error: {e}")

    finally:
        os.remove(temp_path)
