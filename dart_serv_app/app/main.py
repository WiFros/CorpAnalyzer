from fastapi import FastAPI
from routers import embedding, indexing, search

app = FastAPI()

app.include_router(embedding, prefix="/embed", tags=["embed"])
app.include_router(indexing, prefix="/index", tags=["index"])
app.include_router(search, prefix="/search", tags=["search"])

@app.get("/")
async def root():
    return {"message": "Welcome to AI2 Server"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)