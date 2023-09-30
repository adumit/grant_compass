from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/search/")
async def get_item(search_text: str):
    return {"search_text": search_text}