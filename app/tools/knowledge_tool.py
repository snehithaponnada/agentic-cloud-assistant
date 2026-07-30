from langchain_core.tools import tool

from app.rag.retriever import retrieve_cloud_knowledge


@tool
def search_cloud_knowledge(query: str) -> str:
    """
    Search the AWS troubleshooting knowledge base using semantic
    vector retrieval. Use this tool when AWS troubleshooting
    information is required.
    """

    documents = retrieve_cloud_knowledge(
        query=query,
        k=3
    )

    if not documents:
        return "No relevant AWS troubleshooting information was found."

    results = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "unknown"
        )

        results.append(
            f"""
Source: {source}

{document.page_content}
"""
        )

    return "\n---\n".join(results)