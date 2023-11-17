import time

from openai import RateLimitError, OpenAI
from openai.types import Embedding
import numpy as np

from .document_types import (
    KeyedChunkedText,
    FileName,
    KeyedChunkedTextWithEmbeddings,
)


def get_embedding(texts: list[str], model="text-embedding-ada-002") -> list[np.array]:
    client = OpenAI()
    split_texts = [text.replace("\n", " ") for text in texts]
    num_batches = len(split_texts) // 250 + 1
    response_list: list[Embedding] = []
    for i in range(num_batches):
        try:
            response = client.embeddings.create(
                input=split_texts[i * 250 : (i + 1) * 250], model=model
            ).data
            response_list += response
        except RateLimitError:
            print("Rate limit exceeded, waiting 10 seconds...")
            time.sleep(60)
            response = client.embeddings.create(
                input=split_texts[i * 250 : (i + 1) * 250], model=model
            ).data
            response_list += response

    return [resp.embedding for resp in response_list]


def embed_chunks(
    filename_to_chunks: dict[FileName, KeyedChunkedText]
) -> KeyedChunkedTextWithEmbeddings:
    embeddings = {}
    batch_size = 200
    num_chunks = sum([len(file_chunks) for file_chunks in filename_to_chunks.values()])
    keyed_chunk_tuples = [
        (file_name, chunk_key, chunk)
        for file_name, file_chunks in filename_to_chunks.items()
        for chunk_key, chunk in file_chunks.items()
    ]
    for i in range(0, num_chunks, batch_size):
        print(f"Embedding {i} to {i+batch_size}...")
        batch = keyed_chunk_tuples[i : i + batch_size]
        batch_embeddings = get_embedding([chunk for _, _, chunk in batch])
        for j, (file_name, chunk_key, _) in enumerate(batch):
            embeddings[(file_name, chunk_key)] = batch_embeddings[j]
    return embeddings
