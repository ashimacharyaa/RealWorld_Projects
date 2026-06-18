from google import genai  # Modern Google GenAI SDK
from memory import get_memories
from rag import search_documents
from dotenv import load_dotenv 

load_dotenv()

client = genai.Client()
MODEL_NAME = "gemini-2.5-flash"

def generate_response(user_input):
    docs = search_documents(user_input)
    memories = get_memories()

    memory_context = "\n".join(memories)
    knowledge_context = "\n".join(docs)

    prompt = f"""
You are an intelligent AI assistant.

Use the conversation memory and retrieved knowledge when relevant.

Conversation Memory:
{memory_context}

Knowledge Base:
{knowledge_context}

User Question:
{user_input}

Provide a helpful and natural answer.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        
        if response.text:
            return response.text
        return str(response)

    except Exception as e:
        return f"Gemini Error: {str(e)}"