"""MiniLM model implementation - non-gated alternative."""

from typing import Optional, Dict, Any
import numpy as np
from embeddings.sentence_transformer import SentenceTransformerModel


class MiniLMEmbeddingModel(SentenceTransformerModel):
    """MiniLM model - fast, non-gated SentenceTransformer implementation."""

    def __init__(
        self,
        cache_dir: Optional[str] = None,
        device: str = "auto"
    ):
        """Initialize MiniLMEmbeddingModel.

        Args:
            cache_dir: Directory to cache the model
            device: Device to load model on ("auto", "cuda", "mps", "cpu")
        """
        super().__init__(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            cache_dir=cache_dir,
            device=device
        )

    def encode(self, texts: list[str], **kwargs) -> np.ndarray:
        """Encode texts using MiniLM (ignores prompt_name as MiniLM doesn't use prompts)."""
        # Remove prompt_name if present since MiniLM doesn't use instruction prompts
        kwargs.pop('prompt_name', None)
        return self.model.encode(texts, **kwargs)
