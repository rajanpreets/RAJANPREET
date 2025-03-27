from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import forecast_router
from .api.test_router import router as test_router
from .core.config import settings

app = FastAPI(
    title=settings.api.title,
    description=settings.api.description,
    version=settings.api.version,
    docs_url=settings.api.docs_url,
    redoc_url=settings.api.redoc_url
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(forecast_router)
app.include_router(test_router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Pharma Forecasting API"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 