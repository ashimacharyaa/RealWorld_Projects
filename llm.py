from langchain_google_genai import(
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from services.config import GEMINI_MODEL

def get_llm():

    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=0.2
    )

def get_embeddings():

    return GoogleGenerativeAIEmbeddings(
        model= "models/text-embedding-004"
    )