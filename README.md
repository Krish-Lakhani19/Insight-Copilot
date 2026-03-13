# Insight-Copilot[Link] (https://rag-chatbot-oa5yalndpqyldcugipt6em.streamlit.app)

This project is a Streamlit chatbot that combines document retrieval with live web search so sports teams can ask questions and get grounded answers quickly. It supports multiple LLM providers and lets the user choose between concise and detailed responses.

## What This App Does
- Answers questions with context from uploaded documents
- Pulls fresh information from the web when needed
- Lets you switch between concise and detailed response styles
- Works with Groq, OpenAI, or Gemini providers

## Project Structure
```
Insight-Copilot/
├── app.py
├── config/
│   └── config.py
├── models/
│   ├── llm.py
│   └── embeddings.py
├── utils/
│   ├── logger.py
│   ├── rag.py
│   └── web_search.py
├── requirements.txt
├── CASE_STUDY.md
└── RUNBOOK.md
```

## Setup
1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Set at least one provider key
```bash
export GROQ_API_KEY="your_key"
export GROQ_MODEL="llama-3.3-70b-versatile"
```

Optional web search keys:
```bash
export TAVILY_API_KEY="your_key"
export SERPER_API_KEY="your_key"
```

3. Run the app
```bash
streamlit run app.py
```

## How To Use
1. Open the app and go to the Chat page
2. Pick a provider and model
3. Upload documents and build the knowledge base
4. Ask questions and switch response modes as needed

## Notes
- Keep API keys out of Git by using environment variables
- If a model is retired, update the model name in your environment or sidebar

## Deployment
The app is ready for Streamlit Cloud. Push this repo to GitHub and deploy using `Insight-Copikot/app.py` as the entry point, then add your API keys in the Streamlit secrets panel.
