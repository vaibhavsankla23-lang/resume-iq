from PyPDF2 import PdfReader

def extract_text_from_pdf(file_bytes) -> str:
    """Extract clean text from uploaded PDF resume."""
    reader = PdfReader(file_bytes)
    extracted_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text += text + "\n"
    return extracted_text.strip()