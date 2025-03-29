# src/backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Assuming your routers are structured like this relative to main.py
# If forecast_router is directly in 'api', it should be '.api.forecast_router'
# Adjust imports based on your exact file structure if needed.
# Assuming forecast_router is an APIRouter instance (like test_router)
# Example: from .api.forecast_router import router as forecast_api_router
from .api import forecast_router # Assuming forecast_router is an APIRouter instance in api/__init__.py or similar
from .api.test_router import router as test_router
from .core.config import settings # Imports the settings instance from config.py

# Initialize FastAPI using the nested settings from config.py (Option 2)
# This reads settings like settings.api.title, settings.api.version etc.
app = FastAPI(
    title=settings.api.title,
    description=settings.api.description,
    version=settings.api.version,
    docs_url=settings.api.docs_url,
    redoc_url=settings.api.redoc_url,
    # You might want to control OpenAPI URL via settings too:
    # openapi_url=f"{settings.api_prefix}/openapi.json" # Example using api_prefix
)

# Configure CORS Middleware
# WARNING: allow_origins=["*"] is insecure for production.
# Replace "*" with your frontend URL(s) in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust for production environments
    allow_credentials=True,
    allow_methods=["*"], # Allow all standard methods
    allow_headers=["*"], # Allow all standard headers
)

# Include your API routers
# Make sure the prefix here aligns with your overall API strategy
# Routers defined within forecast_router and test_router will be relative to these prefixes
app.include_router(forecast_router, prefix=settings.api_prefix, tags=["Forecast"])
app.include_router(test_router, prefix=settings.api_prefix, tags=["Test"])


# Define root and health check endpoints
@app.get("/", tags=["General"])
async def root():
    """
    Root endpoint providing a welcome message.
    """
    # You could return basic API info from settings here too
    return {
        "message": f"Welcome to the {settings.api.title}",
        "version": settings.api.version,
        "docs": app.docs_url
        }

@app.get("/health", tags=["General"])
async def health_check():
    """
    Simple health check endpoint to confirm the API is running.
    """
    return {"status": "healthy"}

# Note: If you are running this file directly using uvicorn for local testing,
# you might have a section like this at the bottom (DO NOT include this specific
# block if deploying via Render's command `uvicorn src.backend.app.main:app ...`):
#
# if __name__ == "__main__":
#     import uvicorn
#     # Example for local run: uvicorn main:app --reload --port 8000
#     # Render uses its own command, so this block is typically not needed for deployment.
#     uvicorn.run(app, host="0.0.0.0", port=8000)
