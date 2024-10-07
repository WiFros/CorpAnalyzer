from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.companies import companies_router
from app.core.config import settings
from app.db.mongo import connect_to_mongo, close_mongo_connection
from prometheus_fastapi_instrumentator import Instrumentator

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to the database
    await connect_to_mongo()
    yield
    # Shutdown: Close the database connection
    await close_mongo_connection()

app = FastAPI(
    title="Company Search API",
    description="An API for searching company information",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex="https?://localhost(:\d+)?",
)

# Uncomment to enable Prometheus
# Instrumentator().instrument(app).expose(app)

app.include_router(companies_router, prefix="/api/companies", tags=["companies"])

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred."}
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the Company Search API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)