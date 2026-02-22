from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app import models
from app.routers import users, posts

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Posts Service API",
    description="A simple blog API with user authentication and post management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(posts.router)

# Root endpoint
@app.get("/")
async def root():
    """API root with basic information"""
    return {
        "service": "Posts Service",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Check if API is running"""
    return {
        "status": "healthy",
        "database": "connected"
    }
