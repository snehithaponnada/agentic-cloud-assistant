from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


CHROMA_DIR = "chroma_db"


# Load embedding model ONCE when the module starts
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Connect to ChromaDB ONCE
vector_store = Chroma(
    collection_name="aws_troubleshooting",
    embedding_function=embeddings,
    persist_directory=CHROMA_DIR
)


def get_vector_store():
    """
    Return the existing Chroma vector store.
    """
    return vector_store


def retrieve_cloud_knowledge(query: str, k: int = 3):
    """
    Retrieve the most relevant AWS troubleshooting documents.
    """

    documents = vector_store.similarity_search(
        query,
        k=k
    )

    return documents