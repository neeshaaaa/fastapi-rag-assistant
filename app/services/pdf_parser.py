from pypdf import PdfReader

# Extract text from PDF file
def extract_pdf_text(
    file_path: str
) -> str:

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# Extract text from TXT file
def extract_txt_text(
    file_path: str
) -> str:

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()