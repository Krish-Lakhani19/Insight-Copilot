# NeoStats Insight Copilot Case Study

## Use Case Objective
Coaches, analysts, and scouts need fast, trustworthy answers that combine internal scouting reports with fresh public information. The goal is to build a chatbot that can answer performance questions, summarize reports, and retrieve recent updates in a single conversation.

## How I Approached The Problem
I framed the problem as a retrieval plus reasoning task. The assistant should:
1. Understand the question and choose the right response style.
2. Retrieve relevant excerpts from internal documents.
3. Optionally pull recent web information for time sensitive queries.
4. Answer clearly with traceable context.

## Solution Overview
The solution is a Streamlit chatbot with a modular architecture:
- `models/llm.py` initializes the LLM provider.
- `models/embeddings.py` contains the embedding model.
- `utils/rag.py` loads files, chunks text, builds a vector index, and retrieves relevant chunks.
- `utils/web_search.py` performs live web search with a provider fallback.
- `app.py` orchestrates UI, response modes, and context injection.

## Features Implemented
- Retrieval Augmented Generation using a TF IDF vector index built from uploaded documents.
- Live web search using Tavily, Serper, or DuckDuckGo with provider fallback.
- Response modes that toggle between concise and detailed answers.
- Structured error handling and logging for reliable operation.

## Challenges Faced
- Document variety required a simple, reliable chunking strategy.
- Web search can fail without API keys, so fallback logic was added.
- Different LLM providers have different model naming conventions, so the UI makes this explicit.

## Deployment
The app is designed for Streamlit Cloud. After pushing the repository, set the environment variables in the Streamlit Cloud settings and deploy using `streamlit run app.py`.
