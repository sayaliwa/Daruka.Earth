from pathlib import Path
from pypdf import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DOCUMENTS_PATH = PROJECT_ROOT / "knowledge" / "documents"


def extract_pages_from_pdf(pdf_path):
    """
    Extract text from a PDF page-by-page.
    """

    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            pages.append({
                "text": text.strip(),
                "page": page_number
            })

    return pages


def load_all_documents():
    """
    Load all PDF documents from the knowledge/document folders.
    """

    documents = []

    for pdf_path in DOCUMENTS_PATH.rglob("*.pdf"):

        organization = pdf_path.parent.name

        pages = extract_pages_from_pdf(pdf_path)

        for page in pages:

            documents.append({
                "text": page["text"],
                "metadata": {
                    "source": pdf_path.name,
                    "organization": organization,
                    "page": page["page"]
                }
            })

    return documents


if __name__ == "__main__":

    documents = load_all_documents()

    print("\nScientific Document Ingestion Test")
    print("----------------------------------")

    print(f"Documents/pages extracted: {len(documents)}")

    if documents:

        first_document = documents[0]

        print("\nFirst extracted page:")
        print("--------------------")

        print("Source:",
              first_document["metadata"]["source"])

        print("Organization:",
              first_document["metadata"]["organization"])

        print("Page:",
              first_document["metadata"]["page"])

        print("\nText preview:")
        print(first_document["text"][:1000])