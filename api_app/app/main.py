from fastapi import FastAPI
from app.api import companies

app = FastAPI(title="Company API", description="API for querying company information")

app.include_router(companies.router, prefix="/api/v1", tags=["companies"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)