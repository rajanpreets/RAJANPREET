from typing import Generator
from sqlalchemy.orm import Session
from ..database.base import get_db

def get_db_session() -> Generator[Session, None, None]:
    return get_db() 