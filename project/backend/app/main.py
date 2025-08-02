from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_tables
from .routers import todos

# Create database tables
create_tables()

app = FastAPI(
    title="Todo API",
    description="FastAPI backend for Todo application",
    version="1.0.0"
)

# CORS middleware - CRITICAL for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(todos.router)

@app.get("/")
async def root():
    return {"message": "Todo API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}