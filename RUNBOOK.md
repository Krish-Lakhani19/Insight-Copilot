# Step by Step Execution

1. Open a terminal in `/Users/krishlakhani/Documents/neostats-chatbot/AI_UseCase`
2. Create a virtual environment if you want isolation
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set environment variables for at least one LLM provider:

```bash
export GROQ_API_KEY="your_key"
export GROQ_MODEL="llama-3.1-70b-versatile"
```

Optional web search keys:

```bash
export TAVILY_API_KEY="your_key"
export SERPER_API_KEY="your_key"
```

5. Start the app:

```bash
streamlit run app.py
```

6. Upload documents in the sidebar, build the knowledge base, then chat.
