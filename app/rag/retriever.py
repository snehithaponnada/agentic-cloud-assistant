from pathlib import Path

from langchain_core.documents import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


KNOWLEDGE_DIR = Path("knowledge")

documents = []

for file_path in KNOWLEDGE_DIR.glob("*.txt"):
    text = file_path.read_text(encoding="utf-8")

    documents.append(
        Document(
            page_content=text,
            metadata={"source": file_path.name}
        )
    )


texts = [doc.page_content for doc in documents]

vectorizer = TfidfVectorizer(
    stop_words="english"
)

document_vectors = vectorizer.fit_transform(texts)


def retrieve_cloud_knowledge(query: str, k: int = 3):
    """
    Retrieve relevant AWS troubleshooting knowledge
    using lightweight TF-IDF similarity.
    """

    if not documents:
        return []

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        document_vectors
    )[0]

    ranked_indices = similarities.argsort()[::-1][:k]

    results = []

    for index in ranked_indices:
        if similarities[index] > 0:
            results.append(documents[index])

    return results