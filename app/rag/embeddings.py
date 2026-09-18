from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text):
    """
    Convert text into a numerical embedding.
    """

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    embedding = model.encode(text)

    return embedding


def generate_embeddings(texts):
    """
    Generate embeddings for multiple text documents.
    """

    if not texts:
        raise ValueError("Text list cannot be empty.")

    embeddings = model.encode(texts)

    return embeddings


if __name__ == "__main__":

    text = (
        "Soil organic matter contributes to soil condition "
        "and can support water retention."
    )

    embedding = generate_embedding(text)

    print("\nEmbedding Test")
    print("--------------")

    print(f"Model: {MODEL_NAME}")
    print(f"Embedding dimensions: {len(embedding)}")

    print("\nFirst 10 values:")
    print(embedding[:10])