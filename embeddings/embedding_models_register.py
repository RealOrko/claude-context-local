"""Embedding models registry."""
from embeddings.gemma import GemmaEmbeddingModel
from embeddings.minilm import MiniLMEmbeddingModel

AVAILIABLE_MODELS = {
    "google/embeddinggemma-300m": GemmaEmbeddingModel,
    "sentence-transformers/all-MiniLM-L6-v2": MiniLMEmbeddingModel,
}

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
