# Railcast — Train Arrival Prediction

Railcast combines live Indian railway running information with a trained machine-learning model to estimate arrival delays. Its responsive HTML, CSS, and JavaScript frontend is served by a FastAPI backend.

**Live application:** https://railcast-api.onrender.com/

This branch (`codex/railcast-deploy`) contains the deployment package, training notebooks, and datasets. Its project files are at the repository root.

## Features

- Live train route, station times, location, and delay information.
- Journey date selection for trains 12625, 16306, 16325, and 16346.
- Arrival predictions for eligible halting stations with scheduled arrivals that have not already been passed.
- Mobile layouts, light/dark themes, and 12-hour time displays.
- Manual refresh of live train information.

Predictions require observed stop data. When no completed stops with observed arrivals are available, the app can show live status without enabling predictions. Estimates depend on the upstream data and model assumptions; they are not guaranteed arrival times.

## Requirements

- Python 3.12 (Render uses 3.12.8).
- An API key for the live railway provider at `api.irctc.dev`.
- scikit-learn 1.6.1, matching the saved model.

## Run locally

Clone this deployment branch:

```sh
git clone --branch codex/railcast-deploy --single-branch https://github.com/safvenn/luminar.git
cd luminar
python -m venv .venv
```

Activate the virtual environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```sh
# macOS / Linux
source .venv/bin/activate
```

Install dependencies and unpack the model:

```sh
python -m pip install -r requirements.txt
python prepare_model.py
```

Create a `.env` file in the project root with your own key:

```dotenv
API_KEY=your_live_railway_api_key
```

Alternatively, set `API_KEY` in the server environment. Never commit real credentials. All `.env*` files are ignored.

Start the application:

```sh
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/. The frontend is served by FastAPI; no Node.js build is required. API documentation is at `/docs` and the health endpoint is `/health`.

## Project structure

```text
frontend/                  HTML, CSS, JavaScript, and Vercel routing
src/main.py                FastAPI application and model startup
src/routes/                Live railway API routes
src/services/              Feature preparation and prediction logic
src/ml/preprocessing.json  Model preprocessing metadata
notebooks/                 Training notebook and training datasets
model.pkl.gz               Compressed production model
prepare_model.py           Extracts the production model to src/ml/model.pkl
model.pkl                  Separate model artifact from the original project
app.py                     Original standalone Streamlit experiment
requirements.txt           Backend deployment dependencies
requirements-notebooks.txt Full development and notebook dependencies
```

The production API loads `src/ml/model.pkl`, extracted from `model.pkl.gz`. The root-level `model.pkl` is a separate artifact, not the production API model. The extracted production model is ignored by Git to avoid duplicating the large file.

## Notebooks and experiments

```sh
python -m pip install -r requirements-notebooks.txt
```

Open the notebook in `notebooks/` with a Jupyter-compatible editor and select the virtual environment's Python kernel. The raw training CSVs are under `notebooks/data/raw/`. Review notebook file paths before running on another machine.

`app.py` is a separate Streamlit experiment with a machine-specific model path; update that path before using it. It is not the Render entry point. Use the requirements files above for installation; the original `pyproject.toml` is retained as project metadata.

## Deployment

### Render

The live service deploys from `codex/railcast-deploy` using:

- Runtime: Python 3.12.8
- Build: `pip install -r requirements.txt && python prepare_model.py`
- Start: `uvicorn src.main:app --host 0.0.0.0 --port $PORT --workers 1`
- Environment variable: `API_KEY`

Keep a single worker: live report state is currently stored in process memory. The latest report is shared within that process, so concurrent users are not isolated. Restarts clear this state.

### Vercel frontend

`frontend/vercel.json` maps `/assets/*` to the static files and proxies `/live`, `/predict`, and `/health` to the Render backend. Use `frontend` as the Vercel project root with no framework or build command. Update the proxy destinations if the backend URL changes. A completed Vercel deployment has not yet been verified; the live URL above is hosted on Render.

## Troubleshooting

- **Model file missing:** run `python prepare_model.py` before starting the API.
- **Live API authentication error:** check the configured `API_KEY` and provider access.
- **Predictions unavailable:** fetch live data first and select an eligible arrival station. A journey may not yet have the observations needed for prediction.
- **Model compatibility errors:** use Python 3.12 and scikit-learn 1.6.1.

Additional preprocessing assumptions are documented in `src/ml/README.md`.
