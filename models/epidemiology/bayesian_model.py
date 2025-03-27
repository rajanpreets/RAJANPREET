import numpy as np
import pandas as pd
import pymc as pm
import arviz as az
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class BayesianEpidemiologicalModel:
    def __init__(self, 
                 prior_params: Dict[str, Any] = None,
                 seasonality: bool = True,
                 trend: bool = True):
        """
        Initialize the Bayesian epidemiological model.
        
        Args:
            prior_params: Dictionary of prior parameters
            seasonality: Whether to include seasonal effects
            trend: Whether to include trend effects
        """
        self.prior_params = prior_params or {
            'alpha': {'mu': 0, 'sigma': 10},
            'beta': {'mu': 0, 'sigma': 10},
            'sigma': {'alpha': 1, 'beta': 1}
        }
        self.seasonality = seasonality
        self.trend = trend
        self.model = None
        self.trace = None

    def build_model(self, data: pd.DataFrame) -> None:
        """
        Build the PyMC model.
        
        Args:
            data: DataFrame with columns ['date', 'cases', 'population']
        """
        with pm.Model() as self.model:
            # Priors
            alpha = pm.Normal('alpha',
                            mu=self.prior_params['alpha']['mu'],
                            sigma=self.prior_params['alpha']['sigma'])
            
            if self.trend:
                beta = pm.Normal('beta',
                               mu=self.prior_params['beta']['mu'],
                               sigma=self.prior_params['beta']['sigma'])
            
            if self.seasonality:
                # Seasonal effect
                seasonal = pm.Normal('seasonal', mu=0, sigma=1)
                seasonal_effect = seasonal * pm.math.sin(2 * np.pi * data.index / 12)
            
            # Likelihood
            if self.trend and self.seasonality:
                mu = alpha + beta * data.index + seasonal_effect
            elif self.trend:
                mu = alpha + beta * data.index
            elif self.seasonality:
                mu = alpha + seasonal_effect
            else:
                mu = alpha
            
            # Observation model
            sigma = pm.HalfNormal('sigma',
                                sigma=self.prior_params['sigma']['alpha'])
            
            cases = pm.Normal('cases',
                            mu=mu,
                            sigma=sigma,
                            observed=data['cases'])

    def fit(self, 
            data: pd.DataFrame,
            draws: int = 2000,
            tune: int = 1000,
            chains: int = 4,
            return_inferencedata: bool = True) -> az.InferenceData:
        """
        Fit the model using MCMC.
        
        Args:
            data: DataFrame with columns ['date', 'cases', 'population']
            draws: Number of posterior draws
            tune: Number of tuning steps
            chains: Number of MCMC chains
            return_inferencedata: Whether to return ArviZ InferenceData
            
        Returns:
            ArviZ InferenceData object
        """
        if self.model is None:
            self.build_model(data)
            
        with self.model:
            self.trace = pm.sample(
                draws=draws,
                tune=tune,
                chains=chains,
                return_inferencedata=return_inferencedata
            )
            
        return self.trace

    def predict(self, 
                future_dates: pd.DatetimeIndex,
                n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate predictions for future dates.
        
        Args:
            future_dates: Future dates to predict for
            n_samples: Number of samples to draw from posterior
            
        Returns:
            Tuple of (mean predictions, lower bound, upper bound)
        """
        if self.trace is None:
            raise ValueError("Model must be fit before making predictions")
            
        with self.model:
            pm.set_data({'cases': np.zeros(len(future_dates))})
            ppc = pm.sample_posterior_predictive(
                self.trace,
                var_names=['cases'],
                samples=n_samples
            )
            
        predictions = ppc.posterior_predictive['cases'].values
        mean_pred = np.mean(predictions, axis=0)
        lower_bound = np.percentile(predictions, 2.5, axis=0)
        upper_bound = np.percentile(predictions, 97.5, axis=0)
        
        return mean_pred, lower_bound, upper_bound

    def get_model_summary(self) -> pd.DataFrame:
        """
        Get summary statistics of the fitted model.
        
        Returns:
            DataFrame with model summary statistics
        """
        if self.trace is None:
            raise ValueError("Model must be fit before getting summary")
            
        return az.summary(self.trace, var_names=['alpha', 'beta', 'sigma']) 