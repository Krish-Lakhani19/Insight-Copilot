from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfEmbeddingModel:
    def __init__(self, max_features=4096):
        try:
            self.vectorizer = TfidfVectorizer(
                max_features=max_features,
                stop_words="english"
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to initialize TF IDF vectorizer: {exc}")

    def fit_transform(self, texts):
        try:
            return self.vectorizer.fit_transform(texts)
        except Exception as exc:
            raise RuntimeError(f"Failed to fit and transform texts: {exc}")

    def transform(self, texts):
        try:
            return self.vectorizer.transform(texts)
        except Exception as exc:
            raise RuntimeError(f"Failed to transform texts: {exc}")


def get_embedding_model():
    try:
        return TfidfEmbeddingModel()
    except Exception as exc:
        raise RuntimeError(f"Failed to get embedding model: {exc}")
