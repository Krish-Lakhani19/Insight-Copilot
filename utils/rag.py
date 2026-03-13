from dataclasses import dataclass
from typing import List, Dict, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader

from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class RAGIndex:
    texts: List[str]
    embeddings: Any
    embedding_model: Any
    metadata: List[Dict[str, Any]]


def extract_text_from_upload(uploaded_file):
    try:
        filename = uploaded_file.name.lower()
        if filename.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(pages)

        content = uploaded_file.read()
        try:
            return content.decode("utf-8")
        except Exception:
            return content.decode("latin-1", errors="ignore")
    except Exception as exc:
        logger.exception("Failed to extract text from upload")
        raise RuntimeError(f"Failed to extract text from file: {exc}")


def split_text(text, chunk_size=800, overlap=120):
    try:
        if not text:
            return []

        cleaned = " ".join(text.split())
        chunks = []
        start = 0
        while start < len(cleaned):
            end = min(start + chunk_size, len(cleaned))
            chunks.append(cleaned[start:end])
            if end >= len(cleaned):
                break
            start = end - overlap
            if start < 0:
                start = 0
        return chunks
    except Exception as exc:
        logger.exception("Failed to split text")
        raise RuntimeError(f"Failed to split text: {exc}")


def build_rag_index(texts, embedding_model, metadata=None):
    try:
        if metadata is None:
            metadata = [{} for _ in texts]
        embeddings = embedding_model.fit_transform(texts)
        return RAGIndex(
            texts=texts,
            embeddings=embeddings,
            embedding_model=embedding_model,
            metadata=metadata
        )
    except Exception as exc:
        logger.exception("Failed to build RAG index")
        raise RuntimeError(f"Failed to build RAG index: {exc}")


def retrieve_relevant_chunks(query, rag_index, top_k=5):
    try:
        if not rag_index or not rag_index.texts:
            return []

        query_embedding = rag_index.embedding_model.transform([query])
        scores = cosine_similarity(query_embedding, rag_index.embeddings).flatten()
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [rag_index.texts[i] for i in top_indices]
    except Exception as exc:
        logger.exception("Failed to retrieve relevant chunks")
        raise RuntimeError(f"Failed to retrieve relevant chunks: {exc}")
