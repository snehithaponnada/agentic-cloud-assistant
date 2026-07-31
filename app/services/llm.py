import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


def get_llm():
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        #temperature=0
    )

    return llm