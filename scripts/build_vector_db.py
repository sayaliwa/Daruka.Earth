from app.rag.vectorstore import build_vector_database


if __name__ == "__main__":
    print("Building scientific knowledge vector database...")
    collection = build_vector_database()

    print("Vector database build completed.")
    print(f"Total stored chunks: {collection.count()}")