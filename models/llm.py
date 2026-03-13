import os
import sys
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.config import Settings


def get_chat_model(provider=None, model_name=None, temperature=0.2):
    try:
        settings = Settings()
        selected_provider = (provider or settings.default_provider).lower()

        if selected_provider == "openai" and settings.openai_api_key:
            return ChatOpenAI(
                api_key=settings.openai_api_key,
                model=model_name or settings.openai_model,
                temperature=temperature,
            )

        if selected_provider == "groq" and settings.groq_api_key:
            return ChatGroq(
                api_key=settings.groq_api_key,
                model=model_name or settings.groq_model,
                temperature=temperature,
            )

        if selected_provider in {"gemini", "google", "google-gemini"} and settings.gemini_api_key:
            return ChatGoogleGenerativeAI(
                google_api_key=settings.gemini_api_key,
                model=model_name or settings.gemini_model,
                temperature=temperature,
            )

        return None
    except Exception as exc:
        raise RuntimeError(f"Failed to initialize chat model: {exc}")
