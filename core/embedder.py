import torch
from sentence_transformers import SentenceTransformer
from core.config import ENCODER_MODEL_ID


embedding_model = SentenceTransformer(ENCODER_MODEL_ID)


def embed_text(text):
    embeddings = embedding_model.encode([text], show_progress_bar=True, 
                                        batch_size=32, 
                                        device='cuda' if torch.cuda.is_available() else 'cpu')[0]
    return embeddings