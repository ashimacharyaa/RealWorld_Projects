import streamlit as st

from database import (
    save_message,
    get_conversations,
    clear_conversations
)

from memory import (
    save_memory,
    clear_memory
)

from rag import (
    add_pdf,
    add_txt,
    get_documents,
    delete_document,
    clear_knowledge_base,  
)

from chatbot import generate_response

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="AI Chatbot",
    layout="wide"
)

# ======================================
# HEADER
# ======================================

st.title(" Basic AI Chatbot by Ashim and Aashika")

st.write(
    "Hello. how can I assist you?"
)

# ======================================
# DISPLAY CHAT HISTORY
# ======================================

messages = get_conversations()

for role, message in messages:

    with st.chat_message(role):
        st.write(message)

# ======================================
# USER INPUT
# ======================================

user_input = st.chat_input(
    "Type your message..."
)

if user_input:

    # Save User Message
    save_message(
        "user",
        user_input
    )

    with st.chat_message("user"):
        st.write(user_input)

    # ==================================
    # MEMORY DETECTION
    # ==================================

    text = user_input.lower()

    memory_patterns = [
        "my name is",
        "i am",
        "i like",
        "my favorite",
        "i live in",
        "i study",
        "i work",
        "my age is"
    ]

    for pattern in memory_patterns:

        if pattern in text:

            save_memory(
                user_input
            )

            break

    # ==================================
    # GENERATE AI RESPONSE
    # ==================================

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            bot_response = generate_response(
                user_input
            )

            st.write(
                bot_response
            )

    save_message(
        "assistant",
        bot_response
    )

# ======================================
# SIDEBAR
# ======================================

with st.sidebar:

    st.header("⚙ Settings")

    # ==================================
    # DOCUMENT UPLOAD
    # ==================================

    st.subheader(
        "Knowledge Base"
    )

    uploaded_file = st.file_uploader(
        "Upload PDF or TXT",
        type=["pdf", "txt"]
    )

    if uploaded_file:

        try:

            if uploaded_file.name.lower().endswith(
                ".pdf"
            ):

                add_pdf(
                    uploaded_file
                )

            elif uploaded_file.name.lower().endswith(
                ".txt"
            ):

                add_txt(
                    uploaded_file
                )

            st.success(
                f"{uploaded_file.name} uploaded successfully."
            )

        except Exception as e:

            st.error(
                f"Upload Error: {e}"
            )

    # ==================================
    # DOCUMENT LIST
    # ==================================

    st.subheader(
        "Uploaded Documents"
    )

    documents = get_documents()

    if len(documents) == 0:

        st.info(
            "No documents uploaded."
        )

    else:

        for doc in documents:

            col1, col2 = st.columns(
                [4, 1]
            )

            col1.write(doc)

            if col2.button(
                "❌",
                key=f"delete_{doc}"
            ):

                delete_document(
                    doc
                )

                st.rerun()

    # ==================================
    # CLEAR KNOWLEDGE BASE
    # ==================================

    if st.button(
        "🗑 Clear Knowledge Base"
    ):

        clear_knowledge_base()

        st.success(
            "Knowledge Base Cleared"
        )

        st.rerun()

    st.divider()

    # ==================================
    # MEMORY / CHAT CONTROLS
    # ==================================

    if st.button(
        "🗑 Clear Conversations"
    ):

        clear_conversations()

        st.rerun()

    if st.button(
        "Clear Memory"
    ):

        clear_memory()

        st.rerun()

    if st.button(
        "Full Reset"
    ):

        clear_conversations()

        clear_memory()

        clear_knowledge_base()

        st.success(
            "Everything Reset Successfully"
        )

        st.rerun()

    st.divider()

    # ==================================
    # STATUS PANEL
    # ==================================

    st.subheader(
        "Status"
    )

    st.write(
        f"Documents Loaded: {len(documents)}"
    )

    st.write(
        f"Chat Messages: {len(messages)}"
    )

   