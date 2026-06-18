import os  # IMPORTANT: Fixes the 'os is not defined' error!
import chromadb
from pypdf import PdfReader

# Create ChromaDB client
client = chromadb.PersistentClient(
    path="./chroma_db"
)

# Create/Get collection
collection = client.get_or_create_collection(
    name="knowledge_base"
)


def chunk_text(text, chunk_size=1000):
    """
    Split large text into smaller chunks.
    """
    return [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]


def add_document(name, text):
    """
    Add a text document to ChromaDB using clean string names and metadata.
    """
    # Extract just the clean filename string (e.g., 'research-neps.pdf')
    clean_name = os.path.basename(name)

    try:
        delete_document(clean_name)
    except Exception:
        pass

    chunks = chunk_text(text)

    ids = [
        f"{clean_name}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {"source": clean_name}  # Ensures metadata is ALWAYS a clean string ✅
        for _ in chunks
    ]

    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas
    )


def add_pdf(file_path):
    """
    Extract text from a PDF file using pdfplumber and pass it to add_document.
    """
    import pdfplumber
    text_content = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text_content += page.extract_text() or ""
            
    # Pass it to our chunking function
    add_document(file_path, text_content)


def add_txt(file_path):
    """
    Extract text from a TXT file and pass it to add_document.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text_content = f.read()
        
    # Pass it to our chunking function
    add_document(file_path, text_content)


def search_documents(query, n_results=3):
    """
    Search relevant chunks from ChromaDB.
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    if results.get("documents"):
        return results["documents"][0]

    return []


def delete_document(name):
    """
    Delete all chunks belonging to a document.
    """
    clean_name = os.path.basename(name)
    data = collection.get()
    ids_to_delete = []

    for doc_id in data["ids"]:
        if doc_id.startswith(clean_name + "_"):
            ids_to_delete.append(doc_id)

    if ids_to_delete:
        collection.delete(ids=ids_to_delete)


def list_documents():
    """
    List all stored document IDs.
    """
    data = collection.get()
    return data["ids"] if data else []


def get_documents():
    """
    Returns the document IDs (wraps list_documents for app.py compatibility).
    """
    return list_documents()


def clear_knowledge_base():
    """
    Deletes all documents from the ChromaDB collection to fix app.py errors.
    """
    try:
        data = collection.get()
        if data and data["ids"]:
            collection.delete(ids=data["ids"])
            print("Knowledge base cleared successfully.")
    except Exception as e:
        print(f"Error clearing knowledge base: {str(e)}")