## Phase 6 - Deployment (Streamlit UI + FastAPI)

The goal of Phase 6 is to deploy our best-performing price prediction model as a simple demo product that a user can interact with.

Our deployed pipeline is:

Streamlit UI → FastAPI REST API → Trained Random Forest model (trained on price_log) → Price output in USD

#### What is deployed

The deployment package includes:

- Model artifact (model.joblib)

- Feature list (feature_columns.json) to guarantee correct feature order

- Category mappings (mappings.json) so the API encodes dropdown inputs exactly like training

- FastAPI service (api.py) with /health, /codes, /predict

- Streamlit UI (ui.py) for interactive predictions

model.joblib is a large binary file. We exclude it using .gitignore to keep the repository lightweight, avoid pushing very large files, and prevent Git from becoming slow or failing due to file size limits.

#### Why this matters

This phase confirms that our model is not only accurate in notebooks, but also:

- Works end-to-end in a real pipeline (UI → API → model)

- Produces stable predictions with correct input validation

- Can be tested and evaluated like a real service

![UI](<../../Phase 7 Final report/img/ui.png>)


#### How to run the deployment locally

1) Create and activate the environment

Either conda or venv works. Example with conda:

```bash
conda create -n phase6 python=3.10 -y
conda activate phase6
````

Install dependencies:

```bash
pip install fastapi uvicorn joblib numpy pandas pydantic requests streamlit
```

If the model was trained with scikit-learn:

```bash
pip install scikit-learn
```

Note: scikit-learn version should match the version used when saving model.joblib.

2. Check required files exist

These files should be in the same folder where the commands are run:

```text
api.py
ui.py
model.joblib (shared separately, not from Git)
feature_columns.json
mappings.json
ui_defaults.json (optional but recommended)
```

3. Run the FastAPI server

From the project folder:

```bash
uvicorn api:app --reload --port 8000
```

Quick checks:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/codes
http://127.0.0.1:8000/docs
```

4. Run the Streamlit UI

Open a new terminal (same environment) and run:

```bash
streamlit run ui.py
```

Streamlit will show a URL like:

```text
http://localhost:8501
```

## How to test the API quickly (manual)

You can test /predict with a payload like this:

```json
{
  "year": 2015,
  "combined_fuel_economy": 23,
  "mileage": 30895,
  "fuel_type": "Flex Fuel Vehicle",
  "transmission": "M",
  "body_type": "Wagon",
  "engine_type": "I3",
  "wheel_system": "AWD",
  "has_incidents": false,
  "horsepower": 151,
  "torque": 265.21883948671586,
  "legroom": 79.7,
  "maximum_seating": 5,
  "size_of_vehicle": 427.7,
  "major_options_count": 5
}
```

Expected response:

* predicted_price (USD)
* predicted_log_price
* encoded_inputs (encoded numeric values sent to the model)


## Notes about “real-world” inputs

Some features (legroom, size_of_vehicle, torque) are engineered numeric features. In a real product, these would typically be auto-filled from a VIN/trim database. For this demo, the UI keeps them as “advanced inputs” and provides safe defaults.

