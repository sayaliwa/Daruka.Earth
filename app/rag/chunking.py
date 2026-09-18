from app.rag.ingestion import load_all_documents


def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Split text into overlapping chunks.

    chunk_size:
        Approximate maximum number of characters per chunk.

    overlap:
        Number of characters shared between consecutive chunks.
    """

    if not text or not text.strip():
        return []

    text = text.strip()

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def create_document_chunks():

    documents = load_all_documents()

    all_chunks = []

    for document in documents:

        chunks = chunk_text(document["text"])

        for chunk_number, chunk in enumerate(chunks, start=1):

            all_chunks.append({
                "text": chunk,
                "metadata": {
                    "source": document["metadata"]["source"],
                    "organization": document["metadata"]["organization"],
                    "page": document["metadata"]["page"],
                    "chunk": chunk_number
                }
            })

    return all_chunks


if __name__ == "__main__":

    chunks = create_document_chunks()

    print("\nDocument Chunking Test")
    print("---------------------")

    print(f"Total chunks created: {len(chunks)}")

    if chunks:

        first_chunk = chunks[0]

        print("\nFirst chunk metadata:")
        print("---------------------")

        print("Source:",
              first_chunk["metadata"]["source"])

        print("Organization:",
              first_chunk["metadata"]["organization"])

        print("Page:",
              first_chunk["metadata"]["page"])

        print("Chunk:",
              first_chunk["metadata"]["chunk"])

        print("\nChunk preview:")
        print("--------------")

        print(first_chunk["text"][:1000])