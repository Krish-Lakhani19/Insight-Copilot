import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv is optional, environment variables still work without it
    pass


class Settings:
    def __init__(self):
        try:
            self.openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
            self.groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
            self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()

            self.tavily_api_key = os.getenv("TAVILY_API_KEY", "").strip()
            self.serper_api_key = os.getenv("SERPER_API_KEY", "").strip()

            self.default_provider = os.getenv("DEFAULT_PROVIDER", "groq").strip().lower()
            self.search_provider = os.getenv("SEARCH_PROVIDER", "duckduckgo").strip().lower()

            self.groq_model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile").strip()
            self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
            self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()

            self.max_context_chunks = int(os.getenv("MAX_CONTEXT_CHUNKS", "5"))
            self.chunk_size = int(os.getenv("CHUNK_SIZE", "800"))
            self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "120"))
            self.search_results = int(os.getenv("SEARCH_RESULTS", "5"))
        except Exception as exc:
            raise RuntimeError(f"Failed to load settings: {exc}")
