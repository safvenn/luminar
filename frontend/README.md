# Railcast frontend

Run FastAPI from the project root:

```powershell
.\.venv312\Scripts\python.exe -m uvicorn src.main:app --reload --port 8000
```

Open http://127.0.0.1:8000/. No separate frontend server is needed.

Use Python 3.12 with scikit-learn 1.6.1 to match the saved model.

Select a supported train (12625, 16306, or 16346), find the train, select a station and predict arrival. Automatic refresh is disabled.

Live data uses RailRadar with API_KEY from src/.env or the server environment.

Times are displayed in 12-hour format with AM/PM and day offsets when applicable.
