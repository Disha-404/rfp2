from sentence_transformers import SentenceTransformer, util
import numpy as np
import torch

def find_most_similar(query, embeddings, texts, model):
    query_embedding = model.encode(query, device='cpu', convert_to_tensor=True).to('cpu')
    similarities = util.pytorch_cos_sim(query_embedding, embeddings)
    most_similar_idx = similarities.argsort(descending=True)[0][:3].cpu().numpy()
    return [texts[idx] for idx in most_similar_idx], most_similar_idx
