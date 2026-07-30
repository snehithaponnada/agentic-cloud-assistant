from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


CHROMA_DIR = "chroma_db"

_vector_store = None


def get_vector_store():
    """
    Lazily initialize the embedding model and Chroma vector store.

    The model is loaded only when knowledge retrieval is actually
    requested instead of during FastAPI startup.
    """

    global _vector_store

    if _vector_store is None:

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        _vector_store = Chroma(
            collection_name="aws_troubleshooting",
            embedding_function=embeddings,
            persist_directory=CHROMA_DIR
        )

    return _vector_store


def retrieve_cloud_knowledge(query: str, k: int = 3):
    """
    Retrieve relevant AWS troubleshooting documents.
    """

    vector_store = get_vector_store()

    documents = vector_store.similarity_search(
        query,
        k=k
    )

    return documents