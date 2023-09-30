import orjson

from fastapi import FastAPI

from embed import get_embedding
from search_text import search_embeddings

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/search/")
async def get_item(search_text: str):
    with open("test_data/test_grants.json") as f:
        grant_embeddings = orjson.loads(f.read())

    top_indices = search_embeddings(
        search_text, [g["embedding"] for g in grant_embeddings], top_n=10
    )
    print(top_indices)
    return {
        "Top matches": [
            {k: v for k, v in grant_embeddings[i].items() if k != "embedding"}
            for i in top_indices
        ]
    }
