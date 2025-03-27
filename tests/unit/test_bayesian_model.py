import pytest
import numpy as np
from models.epidemiology.bayesian_model import BayesianEpidemiologicalModel

@pytest.fixture
def bayesian_model():
    return BayesianEpidemiologicalModel()

@pytest.fixture
def sample_market_data():
    return {
        "market_trend": 0.05,
        "market_share": 0.2,
        "growth_rate": 0.1
    }

@pytest.fixture
def sample_epi_data():
    return {
        "prevalence": 0.01,
        "incidence": 0.001,
        "risk_factors": ["age", "gender"]
    }

@pytest.fixture
def sample_fda_data():
    return {
        "approval_status": "approved",
        "price_per_patient": 1000,
        "reimbursement_rate": 0.8
    }

@pytest.fixture
def sample_ai_analysis():
    return {
        "competitor_analysis": {
            "new_entrants": 2,
            "market_exits": 1
        },
        "treatment_preference": 0.7
    }

def test_forecast_market_size(bayesian_model, sample_market_data, sample_epi_data, sample_fda_data):
    forecast = bayesian_model.forecast_market_size(
        market_data=sample_market_data,
        epi_data=sample_epi_data,
        fda_data=sample_fda_data,
        forecast_horizon=5
    )
    
    assert "market_size" in forecast
    assert "confidence_interval" in forecast
    assert len(forecast["confidence_interval"]) == 2
    assert forecast["confidence_interval"][0] <= forecast["confidence_interval"][1]

def test_forecast_patient_share(bayesian_model, sample_market_data, sample_ai_analysis):
    forecast = bayesian_model.forecast_patient_share(
        market_data=sample_market_data,
        ai_analysis=sample_ai_analysis,
        forecast_horizon=5
    )
    
    assert "patient_share" in forecast
    assert "confidence_interval" in forecast
    assert len(forecast["confidence_interval"]) == 2
    assert forecast["confidence_interval"][0] <= forecast["confidence_interval"][1]

def test_forecast_revenue(bayesian_model, sample_fda_data):
    forecast = bayesian_model.forecast_revenue(
        market_size=1000000,
        patient_share=0.2,
        pricing_data=sample_fda_data,
        forecast_horizon=5
    )
    
    assert "revenue" in forecast
    assert "confidence_interval" in forecast
    assert len(forecast["confidence_interval"]) == 2
    assert forecast["confidence_interval"][0] <= forecast["confidence_interval"][1]

def test_calculate_posterior_mean(bayesian_model):
    posterior_mean = bayesian_model._calculate_posterior_mean(
        prior_mean=1000000,
        prior_std=500000,
        likelihood_mean=1200000,
        likelihood_std=300000
    )
    
    assert isinstance(posterior_mean, float)
    assert posterior_mean > 0

def test_calculate_confidence_intervals(bayesian_model):
    forecast = [100, 110, 120, 130, 140]
    ci_lower, ci_upper = bayesian_model._calculate_confidence_intervals(forecast)
    
    assert ci_lower <= ci_upper
    assert ci_lower <= np.mean(forecast)
    assert ci_upper >= np.mean(forecast)

def test_calculate_competitor_factor(bayesian_model):
    competitor_analysis = {
        "new_entrants": 2,
        "market_exits": 1
    }
    
    factor = bayesian_model._calculate_competitor_factor(competitor_analysis, year=1)
    assert isinstance(factor, float)
    assert factor > 0

def test_calculate_price_factor(bayesian_model):
    pricing_data = {
        "price_inflation": 0.05
    }
    
    factor = bayesian_model._calculate_price_factor(pricing_data, year=1)
    assert isinstance(factor, float)
    assert factor > 1  # Should be greater than 1 due to inflation 