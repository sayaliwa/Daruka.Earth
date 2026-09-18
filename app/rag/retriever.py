from app.rag.embeddings import generate_embedding
from app.rag.vectorstore import get_collection


def retrieve_scientific_evidence(
    query,
    top_k=5
):
    """
    Retrieve the most relevant scientific
    knowledge chunks for a user query.
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    collection = get_collection()

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    retrieved_documents = results.get(
        "documents",
        [[]]
    )[0]

    retrieved_metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    retrieved_distances = results.get(
        "distances",
        [[]]
    )[0]

    evidence = []

    for index in range(len(retrieved_documents)):

        evidence.append({
            "text": retrieved_documents[index],

            "metadata": retrieved_metadatas[index],

            "distance": retrieved_distances[index]
        })

    return evidence


if __name__ == "__main__":

    query = (
        "How can low soil moisture affect "
        "plants and biodiversity?"
    )

    evidence = retrieve_scientific_evidence(
        query,
        top_k=5
    )

    print("\nScientific Retrieval Test")
    print("=========================")

    print(f"\nQuery:\n{query}")

    print(
        f"\nRetrieved results: {len(evidence)}"
    )

    for index, result in enumerate(
        evidence,
        start=1
    ):

        print(
            f"\n--- Result {index} ---"
        )

        metadata = result["metadata"]

        print(
            f"Source: {metadata['source']}"
        )

        print(
            f"Organization: "
            f"{metadata['organization']}"
        )

        print(
            f"Page: {metadata['page']}"
        )

        print(
            f"Chunk: {metadata['chunk']}"
        )

        print(
            f"Distance: "
            f"{result['distance']:.4f}"
        )

        print("\nText:")
        print(
            result["text"][:700]
        )