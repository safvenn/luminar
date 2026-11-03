# Railcast frontend

The browser interface for Railcast's train arrival delay predictor. For full installation, API details, model assumptions, and troubleshooting, see the [project README](../README.md).

## Run

Complete the setup in the project README, then run from the project directory with your Python environment active:

```bash
python -m uvicorn src.main:app --reload --port 8000
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/). FastAPI serves this interface and its assets; no Node.js installation, build step, or separate frontend server is required to use it.

Use Python 3.12 and scikit-learn 1.6.1 for compatibility with the saved model. Live information uses the backend's `api.irctc.dev` integration. Configure `API_KEY` on the server as described in the project README.

## Use

1. Select train `12625`, `16306`, `16325`, or `16346` and a journey date.
2. Click **Find my train**.
3. Select an available upcoming arrival station.
4. Click **Predict arrival** to view the estimated delay and arrival time.
5. Fetch the train again to update live observations; automatic refresh is disabled.

Times use AM/PM and day offsets where applicable. The theme toggle switches between light and dark appearance.

For a later station, the backend predicts each upcoming stop through the target in order. Forecasts remain separate from actual observations. Departure delay is assumed equal to arrival delay, and errors can grow farther ahead. Missing observations or unsupported intermediate inputs produce an explanation instead of a forecast.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | Page structure and forms |
| `styles.css` | Layout and themes |
| `app.js` | Browser interactions and API requests |
| `train-background.svg` | Interface artwork |

## Frontend checks

With Node.js installed, run from the project directory:

```bash
node tests/frontend.test.cjs
```
