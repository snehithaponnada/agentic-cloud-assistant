from app.services.llm import get_llm


llm = get_llm()

response = llm.invoke(
    "What is AWS S3? Explain it in one sentence."
)

print(response.content)