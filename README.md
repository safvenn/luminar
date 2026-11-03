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

## Predicting several stops ahead

If the train is at A and you select E, the server predicts B, then C, then D, then E.

1. Start with actual delays from passed/current stations.
2. Predict the next station using its station and timetable inputs.
3. Add that prediction to a temporary history.
4. Update the previous three delays, their average and previous departure delay before predicting the following station.
5. Return the target station's estimated delay and arrival time.

For example, observations of 20, 24 and 27 minutes might give 29 minutes at B. C then uses 24, 27 and 29. Future unknown delays are no longer passed to the model as zeros.

Predictions never overwrite live observations or stored report features. Each request computes a new chain. Refresh the train to obtain new observations; automatic refresh is disabled.

## Assumptions and limitations

- Departure delay is assumed equal to arrival delay. The provider supplies one observed delay, and the model predicts arrival delay only.
- At least one observed delay is required, including a valid delay at the latest passed/current station. Otherwise the API returns HTTP 422. Actual zero-minute observations remain valid.
- Earlier missing observations are skipped, following the notebook's retained-report approach. With fewer than three observations, absent older lag slots use training's zero padding; the average uses available history. Future stops use predictions, not zero padding.
- Every intermediate current-route station needs supported schedule/model inputs. Unsupported intermediate stations return HTTP 422. Historical stations are excluded.
- The current timetable is traversed in sequence order. Historical training used retained reports that may skip stations; that remaining difference requires validation.
- Errors can accumulate farther ahead. The existing model is unchanged and predictions are not capped. This implementation does not establish forecasting accuracy.
- The separate manual Streamlit form in app.py is not the live-route prediction flow.

## API

Fetch /live for a report_id, then POST /predict with station_code and report_id as query parameters. Existing response fields remain. Additional fields are prediction_method (recursive) and prediction_steps (ordered station codes and estimated arrival delays through the target). prediction_note explains the assumptions.

Reports expire after 30 minutes. Refresh after expiry or when new observations are needed.

## Validation

```powershell
.\.venv312\Scripts\python.exe -m unittest discover -s tests -v
node tests/frontend.test.cjs
```

Regression tests cover propagation, updated delay features, fresh observations, unchanged reports, valid zeros, invalid inputs and unsupported intermediate stations.

For accuracy evaluation, replay held-out historical journeys with future observations hidden. Compare errors at 1, 2, 4 and 8 stops against carrying forward the latest delay. Keep entire later journeys outside training.
