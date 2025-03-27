from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.connection import get_db
from ..core.config import settings

router = APIRouter()

@router.get("/database")
async def test_database(db: Session = Depends(get_db)):
    """Test database connection."""
    try:
        # Try to execute a simple query
        db.execute("SELECT 1")
        return {"status": "success", "message": "Database connection successful"}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}

@router.get("/config")
async def test_config():
    """Test configuration loading."""
    config_status = {
        "database_url": "configured" if settings.database_url else "missing",
        "grok_api_key": "configured" if settings.grok_api_key else "missing",
        "serper_api_key": "configured" if settings.serper_api_key else "missing"
    }
    return config_status 