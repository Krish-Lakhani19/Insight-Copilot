import os
import sys
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)
from config.config import Settings
from models.llm import get_chat_model
from models.embeddings import get_embedding_model
from utils.rag import extract_text_from_upload, split_text, build_rag_index, retrieve_relevant_chunks
from utils.web_search import search_web, should_search_web
from utils.logger import get_logger

logger = get_logger(__name__)


def build_system_prompt(response_mode):
    try:
        if response_mode == "Concise":
            style_hint = "Give short, direct answers with crisp bullet points when useful."
        else:
            style_hint = "Give thorough, well structured answers with clear reasoning."

        return (
            "You are the NeoStats Insight Copilot, a sports analytics assistant. "
            "Use provided context when available, and say when you are unsure. "
            f"{style_hint}"
        )
    except Exception as exc:
        logger.exception("Failed to build system prompt")
        raise RuntimeError(f"Failed to build system prompt: {exc}")


def format_context(label, chunks):
    try:
        if not chunks:
            return ""
        joined = "\n\n".join(chunks)
        return f"{label}:\n{joined}"
    except Exception as exc:
        logger.exception("Failed to format context")
        raise RuntimeError(f"Failed to format context: {exc}")


def get_chat_response(chat_model, messages, system_prompt):
    try:
        formatted_messages = [SystemMessage(content=system_prompt)]
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))

        response = chat_model.invoke(formatted_messages)
        return response.content
    except Exception as exc:
        logger.exception("Failed to get response")
        return f"Error getting response: {exc}"


def instructions_page():
    try:
        st.title("The Chatbot Blueprint")
        st.markdown("Follow these instructions to set up and use the chatbot.")
        st.markdown(
            """
## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## API Key Setup

Create API keys for your chosen provider and set them as environment variables:

- OpenAI: `OPENAI_API_KEY`
- Groq: `GROQ_API_KEY`
- Google Gemini: `GEMINI_API_KEY`

For web search, optionally set one of:

- Tavily: `TAVILY_API_KEY`
- Serper: `SERPER_API_KEY`

## How to Use

1. Go to the Chat page using the sidebar
2. Pick a provider and response mode
3. Upload documents to enable retrieval
4. Start chatting

## Troubleshooting

- No response: confirm your API keys are valid
- Model errors: double check the model name in the sidebar
- Web search errors: ensure a search provider is set or use DuckDuckGo fallback
"""
        )
    except Exception as exc:
        logger.exception("Failed to render instructions page")
        st.error(f"Failed to render instructions: {exc}")


def _build_rag_from_uploads(uploaded_files, settings):
    try:
        texts = []
        metadata = []
        for upload in uploaded_files:
            raw_text = extract_text_from_upload(upload)
            chunks = split_text(
                raw_text,
                chunk_size=settings.chunk_size,
                overlap=settings.chunk_overlap
            )
            texts.extend(chunks)
            metadata.extend([{"source": upload.name}] * len(chunks))
        embedding_model = get_embedding_model()
        return build_rag_index(texts, embedding_model, metadata)
    except Exception as exc:
        logger.exception("Failed to build RAG index from uploads")
        raise RuntimeError(f"Failed to build RAG index from uploads: {exc}")


def chat_page():
    try:
        st.title("Insight Copilot")
        settings = Settings()

        with st.sidebar:
            st.subheader("Assistant Settings")
            available_providers = []
            if settings.groq_api_key:
                available_providers.append("groq")
            if settings.openai_api_key:
                available_providers.append("openai")
            if settings.gemini_api_key:
                available_providers.append("gemini")
            if not available_providers:
                available_providers = ["groq", "openai", "gemini"]

            provider = st.selectbox("Provider", available_providers, index=0)

            default_model = {
                "groq": settings.groq_model,
                "openai": settings.openai_model,
                "gemini": settings.gemini_model,
            }.get(provider, "")
            model_name = st.text_input("Model name", value=default_model)

            response_mode = st.radio("Response mode", ["Concise", "Detailed"], index=1)
            allow_web_search = st.checkbox("Allow live web search", value=True)

            st.divider()
            st.subheader("Document Retrieval")
            uploads = st.file_uploader(
                "Upload documents",
                type=["pdf", "txt"],
                accept_multiple_files=True
            )
            if st.button("Build knowledge base", use_container_width=True):
                if uploads:
                    with st.spinner("Processing documents"):
                        st.session_state.rag_index = _build_rag_from_uploads(uploads, settings)
                    st.success("Knowledge base ready")
                else:
                    st.warning("Upload at least one document")

            st.divider()
            if st.button("Clear chat history", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

        chat_model = get_chat_model(provider=provider, model_name=model_name)
        if chat_model is None:
            st.info("Add a valid API key in your environment variables to start chatting.")
            return

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Type your message here"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            rag_context = ""
            if st.session_state.get("rag_index"):
                try:
                    chunks = retrieve_relevant_chunks(
                        prompt,
                        st.session_state.rag_index,
                        top_k=settings.max_context_chunks
                    )
                    rag_context = format_context("Knowledge base context", chunks)
                except Exception as exc:
                    rag_context = f"Knowledge base error: {exc}"

            web_context = ""
            if allow_web_search and should_search_web(prompt):
                try:
                    results = search_web(prompt, settings)
                    snippets = [
                        f"{item['title']}\n{item['snippet']}\n{item['url']}"
                        for item in results
                    ]
                    web_context = format_context("Web search context", snippets)
                except Exception as exc:
                    web_context = f"Web search error: {exc}"

            system_prompt = build_system_prompt(response_mode)
            if rag_context or web_context:
                system_prompt = f"{system_prompt}\n\n{rag_context}\n\n{web_context}"

            with st.chat_message("assistant"):
                with st.spinner("Getting response"):
                    response = get_chat_response(chat_model, st.session_state.messages, system_prompt)
                    st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as exc:
        logger.exception("Failed to render chat page")
        st.error(f"Chat page error: {exc}")


def main():
    try:
        st.set_page_config(
            page_title="LangChain Multi-Provider ChatBot",
            page_icon="chatbot",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        with st.sidebar:
            st.title("Navigation")
            page = st.radio("Go to:", ["Chat", "Instructions"], index=0)

        if page == "Instructions":
            instructions_page()
        if page == "Chat":
            chat_page()
    except Exception as exc:
        logger.exception("Failed to render main app")
        st.error(f"App error: {exc}")


if __name__ == "__main__":
    main()
