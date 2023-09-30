import typing as ta

import openai
import numpy as np


def get_embedding(
    texts: ta.List[str], text_labels: ta.List[str], model="text-embedding-ada-002"
) -> ta.List[np.array]:
    assert len(texts) == len(text_labels)

    split_texts = [text.replace("\n", " ") for text in texts]
    response = openai.Embedding.create(input=split_texts, model=model)["data"]
    return {text_labels[i]: resp["embedding"] for i, resp in enumerate(response)}
