import chromadb

from app.rag.chunking import create_document_chunks
from app.rag.embeddings import generate_embeddings


VECTOR_DB_PATH = "knowledge/vector_db"

COLLECTION_NAME = "environmental_knowledge"

BATCH_SIZE = 4000


def get_collection():
    """
    Create or load the ChromaDB collection.
    """

    client = chromadb.PersistentClient(
        path=VECTOR_DB_PATH
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def build_vector_database():
    """
    Create embeddings for document chunks
    and store them in ChromaDB in batches.
    """

    chunks = create_document_chunks()

    if not chunks:
        raise ValueError(
            "No document chunks found."
        )

    collection = get_collection()

    print(
        f"\nTotal chunks to process: {len(chunks)}"
    )

    for start in range(
        0,
        len(chunks),
        BATCH_SIZE
    ):

        end = min(
            start + BATCH_SIZE,
            len(chunks)
        )

        batch = chunks[start:end]

        print(
            f"\nProcessing chunks "
            f"{start + 1}-{end}..."
        )

        texts = [
            chunk["text"]
            for chunk in batch
        ]

        print("Generating embeddings...")

        embeddings = generate_embeddings(texts)

        ids = []

        metadatas = []

        for index, chunk in enumerate(
            batch,
            start=start
        ):

            ids.append(
                f"chunk_{index}"
            )

            metadatas.append(
                chunk["metadata"]
            )

        print("Storing batch in ChromaDB...")

        collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

        print(
            f"Stored {end} / {len(chunks)} chunks"
        )

    return collection


if __name__ == "__main__":

    collection = build_vector_database()

    print("\nVector Database")
    print("----------------")

    print(
        f"Collection: {COLLECTION_NAME}"
    )

    print(
        f"Total stored chunks: "
        f"{collection.count()}"
    )