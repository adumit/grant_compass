import time
import typing as ta

import openai
from openai.error import RateLimitError
import numpy as np


def get_embedding(
    texts: ta.List[str], model="text-embedding-ada-002"
) -> ta.List[np.array]:
    split_texts = [text.replace("\n", " ") for text in texts]
    num_batches = len(split_texts) // 250 + 1
    response_list = []
    for i in range(num_batches):
        try:
            response = openai.Embedding.create(
                input=split_texts[i * 250 : (i + 1) * 250], model=model
            )["data"]
            response_list += response
        except RateLimitError:
            print("Rate limit exceeded, waiting 10 seconds...")
            time.sleep(60)
            response = openai.Embedding.create(
                input=split_texts[i * 250 : (i + 1) * 250], model=model
            )["data"]
            response_list += response

    return [resp["embedding"] for resp in response_list]