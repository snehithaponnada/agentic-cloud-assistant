from app.rag.retriever import retrieve_cloud_knowledge


query = """
My AWS application says I am not authorized
to download a file even though the file exists.
"""


documents = retrieve_cloud_knowledge(query)


print("\n===== RAG RESULTS =====\n")


for index, document in enumerate(documents, start=1):

    print(f"RESULT {index}")

    print("SOURCE:")
    print(document.metadata.get("source"))

    print("\nCONTENT:")
    print(document.page_content)

    print("\n" + "-" * 60)