# Pharma Forecasting API

A powerful API for pharmaceutical demand forecasting, built with FastAPI and deployed on Render.

## Features

- Demand forecasting for pharmaceutical products
- Confidence interval calculations
- RESTful API endpoints
- Easy integration with existing systems

## Tech Stack

- Python 3.8+
- FastAPI
- Pandas
- NumPy
- Prophet (for advanced forecasting)
- Scikit-learn

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd pharma-forecasting
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the API server:
```bash
uvicorn src.main:app --reload
```

2. Access the API documentation at `http://localhost:8000/docs`

## API Endpoints

### POST /forecast

Generate forecasts for pharmaceutical products.

Request body:
```json
{
    "product_id": "string",
    "historical_data": [
        {
            "date": "2023-01-01",
            "value": 100
        }
    ],
    "forecast_periods": 12
}
```

Response:
```json
{
    "product_id": "string",
    "forecast": [
        {
            "date": "2024-01-01",
            "value": 105.5
        }
    ],
    "confidence_intervals": [
        {
            "date": "2024-01-01",
            "lower_bound": 94.95,
            "upper_bound": 116.05
        }
    ]
}
```

## Deployment

This project is configured for deployment on Render. The `render.yaml` file contains the necessary configuration.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
