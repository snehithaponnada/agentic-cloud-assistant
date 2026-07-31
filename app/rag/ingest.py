import os

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


KNOWLEDGE_DIR = "knowledge"
CHROMA_DIR = "chroma_db"


def ingest_documents():

    loader = DirectoryLoader(
        KNOWLEDGE_DIR,
        glob="*.txt",
        loader_cls=TextLoader
    )

    documents = loader.load()

    print(f"Loaded {len(documents)} documents.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        collection_name="aws_troubleshooting",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR
    )

    vector_store.add_documents(chunks)

    print("Documents successfully stored in ChromaDB.")


if __name__ == "__main__":
    ingest_documents()