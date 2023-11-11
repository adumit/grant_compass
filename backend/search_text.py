import typing as ta

import numpy as np

from backend.embed import get_embedding


def search_embeddings(search_text: str, embeddings: ta.List[np.array], top_n: int = 10):
    search_embedding = get_embedding(
        texts=[search_text], model="text-embedding-ada-002"
    )[0]

    stacked_embeddings = np.array(embeddings)

    closeness = np.dot(search_embedding, stacked_embeddings.T).flatten()
    closest = np.argsort(closeness)[::-1]

    print(closest)

    return closest[:top_n]
