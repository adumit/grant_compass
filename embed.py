import typing as ta

import openai
import numpy as np


def get_embedding(
    texts: ta.List[str], model="text-embedding-ada-002"
) -> ta.List[np.array]:
    split_texts = [text.replace("\n", " ") for text in texts]
    response = openai.Embedding.create(input=split_texts, model=model)["data"]
    return [resp["embedding"] for resp in response]
