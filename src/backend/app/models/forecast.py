from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..database.base import Base

class ForecastRun(Base):
    __tablename__ = "forecast_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    drug_id = Column(String, nullable=False)
    forecast_type = Column(String, nullable=False)  # market_size, patient_share, revenue
    status = Column(String, nullable=False)  # pending, running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    parameters = Column(JSON, nullable=False)
    results = Column(JSON)
    error_message = Column(String)

    # Relationships
    market_size_results = relationship("MarketSizeResult", back_populates="forecast_run")
    patient_share_results = relationship("PatientShareResult", back_populates="forecast_run")
    revenue_results = relationship("RevenueResult", back_populates="forecast_run")

class MarketSizeResult(Base):
    __tablename__ = "market_size_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    forecast_run_id = Column(String, ForeignKey("forecast_runs.id"))
    date = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)
    lower_bound = Column(Float)
    upper_bound = Column(Float)
    confidence_interval = Column(Float)

    # Relationship
    forecast_run = relationship("ForecastRun", back_populates="market_size_results")

class PatientShareResult(Base):
    __tablename__ = "patient_share_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    forecast_run_id = Column(String, ForeignKey("forecast_runs.id"))
    date = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)
    lower_bound = Column(Float)
    upper_bound = Column(Float)
    confidence_interval = Column(Float)

    # Relationship
    forecast_run = relationship("ForecastRun", back_populates="patient_share_results")

class RevenueResult(Base):
    __tablename__ = "revenue_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    forecast_run_id = Column(String, ForeignKey("forecast_runs.id"))
    date = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)
    lower_bound = Column(Float)
    upper_bound = Column(Float)
    confidence_interval = Column(Float)

    # Relationship
    forecast_run = relationship("ForecastRun", back_populates="revenue_results") 