# Code Review Report — Student Placement Prediction (FastAPI + ML)

**Reviewed:** 2026-10-03  
**Project:** Student Placement Prediction System  
**Stack:** Python · FastAPI · scikit-learn · joblib · Pydantic v2

---

## Overall Rating: 6 / 10

You've built a working, layered FastAPI ML server with a clear separation of concerns — routers, services, schemas, dependencies, and a repository layer. That structure is good for a learning project. However, there are several real bugs and patterns that would break in production or make the project harder to maintain. This report covers all of them with concrete fixes.

---

## Architecture Map

```
main.py  ──lifespan──▶  loads models into app.state
    │
    └── predict_router.py  (POST /predict)
            │
            ├── Depends(get_ml_components)   →  ml_components.py  reads app.state
            ├── Security(verify_auth)         →  auth.py
            └── predict_services()            →  model_loader.py
                        │
                        ├── _encode()         →  predict_repository.py  (label encoders)
                        └── model_predict()   →  model_selector.py  (scaler + model)
```

The layering intention is correct. The issues are in the details.

---

## Bugs (will break at runtime or silently produce wrong results)

### BUG-1 — Hardcoded absolute paths in `main.py`

```python
# app/main.py  line 14-16
knn_model = joblib.load(r'C:\Desktop\luminar\FastApi-ml\Student Palcemnt\models\knn_model.pkt')
```

**Problem:** This path only works on your machine. Anyone else (or a CI/CD environment, or Docker) gets a `FileNotFoundError` at startup.

**Fix:** Use `__file__` to build a relative path, the same way you already do for `FRONTEND_DIR`:

```python
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.knn_model = joblib.load(MODELS_DIR / "knn_model.pkt")
    app.state.nb_model  = joblib.load(MODELS_DIR / "nb_model.pkt")
    app.state.scaler    = joblib.load(MODELS_DIR / "scaler.pkt")
    yield
```

---

### BUG-2 — `verify_auth` returns `None` on success; status code is wrong

```python
# app/dependencies/auth.py
def verify_auth(API=Depends(Api_header)):
    if API != API_KEY:
        raise HTTPException(status_code=404, detail="Not authenticated")
    return API  # ← only reached if auth passes
```

Two problems:

1. `404 Not Found` is the wrong status for authentication failure. The correct code is `401 Unauthorized` (or `403 Forbidden` if you want to hide whether the endpoint exists).
2. If `API_KEY` is `None` (missing `.env` file), then any request with `X-API-Key: None` string will pass. Add a startup guard.

**Fix:**

```python
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY environment variable is not set")

def verify_auth(api_key: str = Depends(Api_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key
```

---

### BUG-3 — `model_loader.py` imports `_encode` but never uses it externally; `predict_services` has silent misalignment risk

```python
# app/services/model_loader.py
def _encode(encoder: Any, value: Any) -> int:
    return int(encoder.transform([value])[0])
```

The `_encode` function is defined here but the router imports it:

```python
# app/routers/predict_router.py
from app.services.model_loader import _encode, predict_services
```

`_encode` is imported into the router but **never called there**. This is dead import — either a leftover or a mistake. Remove it from the router import.

Also, `predict_services` constructs a raw Python list then calls `model_predict(features, scaler, model)` — but `model_selector.model_predict` signature is `(features, scaler, model)` which matches. This is fine, but using `numpy.array` explicitly is safer:

```python
import numpy as np
features = np.array([[...]], dtype=float)
```

---

### BUG-4 — `ml` dependency is subscripted with `model` (an Enum), not a string key

```python
# app/routers/predict_router.py
return predict_services(data, ml[model], ml['scaler'])
```

`ml` is a plain dict. `model` is a `Model_input` enum. Dict keys are strings, so `ml[model]` will raise a `KeyError` because `Model_input.knn_model != 'knn_model'` — you need `ml[model.value]`:

```python
return predict_services(data, ml[model.value], ml["scaler"])
```

---

### BUG-5 — The test is broken and tests nothing useful

```python
# tests/test_predict_route.py
result = predict(Prediction_input(**payload))
```

`predict` is the FastAPI route function. It requires injected dependencies (`ml`, `auth`). Calling it directly skips all of that and will raise a `TypeError`. The test would fail immediately if run with pytest.

A proper unit test mocks dependencies, or uses `TestClient`:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_returns_binary_label():
    response = client.post(
        "/predict?model=knn_model",
        json={...},
        headers={"X-API-Key": "test-key"},
    )
    assert response.status_code == 200
    assert response.json()["result"] in {0, 1}
```

---

### BUG-6 — Label encoder classes in `predict_repository.py` are duplicated from `datas/student_placement_prediction.py`

The training notebook does `lab.fit_transform(df[col])` which encodes by the actual sorted unique values in the dataset. The repository file does `LabelEncoder().fit(["Female", "Male", "Other"])` — a manually written list. If the dataset had a different sort order or extra values, the numeric encoding would be **silently wrong** (e.g., `Male → 1` in training but `Male → 2` in production).

**Fix:** Save and load the fitted encoders from disk, exactly like the scaler:

```python
# In training script:
import joblib
joblib.dump(gender_encoder, "models/Gender.pkt")
# ... for each encoder

# In app/services/model_loader.py or lifespan:
app.state.gender_encoder = joblib.load(MODELS_DIR / "Gender.pkt")
```

The `.pkt` encoder files already exist in `models/` — they just aren't being loaded or used.

---

## Design & Architecture Issues

### ARCH-1 — `predict_repository.py` is misnamed

In conventional architecture, a *repository* talks to a data store (database, file, cache). Your file contains label encoder instances — it's not a repository, it's a static configuration module. A better name: `app/encoders.py` or `app/ml/encoders.py`.

---

### ARCH-2 — Model loading has no error handling

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.knn_model = joblib.load(...)
```

If a model file is missing or corrupt, the app crashes at startup with an unhelpful traceback. Wrap with a clear error:

```python
try:
    app.state.knn_model = joblib.load(MODELS_DIR / "knn_model.pkt")
except FileNotFoundError as e:
    raise RuntimeError(f"Model artifact missing: {e}") from e
```

---

### ARCH-3 — No input validation constraints on numeric fields

```python
class Prediction_input(BaseModel):
    Age: int
    CGPA: float
    Attendance_Percentage: int
    Programming_Skill: int
```

Nothing stops a caller from sending `Age: -5`, `CGPA: 999.9`, or `Programming_Skill: 10000`. Pydantic supports field constraints directly:

```python
from pydantic import BaseModel, Field

class Prediction_input(BaseModel):
    Age: int = Field(ge=15, le=60)
    CGPA: float = Field(ge=0.0, le=4.0)
    Attendance_Percentage: int = Field(ge=0, le=100)
    Programming_Skill: int = Field(ge=1, le=10)
    Resume_Score: int = Field(ge=0, le=100)
    Interview_Score: int = Field(ge=0, le=100)
```

---

### ARCH-4 — `model` is a query parameter disguised as a function argument

```python
@router.post("/predict", response_model=Predict_response)
def predict(data: Prediction_input, model: Model_input, ml=Depends(...), auth=Security(...)):
```

FastAPI infers `model: Model_input` as a **query parameter** because it's a simple type that isn't a `Body`. This works, but it's unusual to select a model via a query string for a POST endpoint. A more explicit design uses a wrapper body:

```python
class PredictRequest(BaseModel):
    model: Model_input
    input: Prediction_input

@router.post("/predict")
def predict(request: PredictRequest, ...):
```

Or keep the query param but document it explicitly with `Query(...)`.

---

### ARCH-5 — `Predict_response` only returns a binary integer with no context

```python
class Predict_response(BaseModel):
    result: int
```

The response gives the caller a `0` or `1` with no explanation. A more useful response:

```python
class Predict_response(BaseModel):
    result: int                        # 0 or 1
    placement_label: str               # "Placed" or "Not Placed"
    model_used: str                    # which model produced this
```

This makes the API self-documenting and the frontend easier to build.

---

### ARCH-6 — Static files mount order vs. the `/` route

```python
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")
```

The mount serves everything in `frontend/` under `/assets/`. But your `index.html` likely references `app.js` and `styles.css` without a path prefix, or with `./` — depending on your HTML, those requests may 404. The mount should probably be `/static` or the HTML `<script src>` and `<link href>` must match the mount point. Verify this in the browser console.

---

### ARCH-7 — `python-dotenv` is used but not in `requirements.txt`

```python
# app/dependencies/auth.py
from dotenv import load_dotenv
```

`python-dotenv` is not listed in `requirements.txt`. A fresh install will fail with `ModuleNotFoundError`.

**Fix:** Add it:

```
python-dotenv>=1.0
```

---

### ARCH-8 — Training notebook uses a single shared `LabelEncoder` instance

```python
# datas/student_placement_prediction.py
lab = LabelEncoder()
for i in obj:
    df[i] = lab.fit_transform(df[i])   # ← overwrites lab on every iteration
```

After this loop, `lab` holds only the last column's fit. Then you do:

```python
Gender = lab.fit(df['Gender'])         # re-fit after encoding is done — too late
```

These `fit` calls after `fit_transform` re-fit the encoder on already-encoded integer columns, making the saved encoders useless. This is likely why the app uses hardcoded `LabelEncoder().fit(["Female", ...])` as a workaround. The correct approach is one encoder per column:

```python
encoders = {}
for col in categorical_cols:
    enc = LabelEncoder()
    df[col] = enc.fit_transform(df[col])
    encoders[col] = enc
    joblib.dump(enc, f"models/{col}.pkt")
```

---

## Code Style & Conventions

| Item | Issue | Convention |
|---|---|---|
| Class names | `Prediction_input`, `Model_input`, `Predict_response` | PEP 8: use `PredictionInput`, `ModelInput`, `PredictResponse` |
| Field names in schema | `Age`, `Gender`, `CGPA` (PascalCase) | Pydantic fields should be `snake_case`: `age`, `cgpa` |
| Folder name | `Student Palcemnt` (typo + space) | Use `student_placement` or `student-placement` |
| `requirements.txt` | No pinned versions for most packages | Pin all versions: `fastapi==0.115.0`, `uvicorn==0.30.0` |
| Debug prints | `print("Model loaded - main.py:22")` with line number | Use Python `logging` module instead |
| Unused import | `_encode` imported in router but not used | Remove it |

---

## Security Notes

- The `.env` file containing `API_KEY` should be listed in `.gitignore`. Confirm it is before pushing to GitHub.
- `API_KEY` comparison should use `secrets.compare_digest` to prevent timing attacks:
  ```python
  import secrets
  if not secrets.compare_digest(api_key, API_KEY):
      raise HTTPException(status_code=401, ...)
  ```
- There is no rate limiting. A real deployment should add it (e.g., `slowapi`).

---

## What You Did Well

- **Lifespan pattern** — loading models once at startup with `@asynccontextmanager` is the correct FastAPI pattern. Good choice.
- **`app.state` for model storage** — sharing loaded models via `app.state` and injecting via `Depends` is idiomatic FastAPI.
- **Layered structure** — separating routers, services, schemas, dependencies, and ML logic shows good architectural instinct.
- **Pydantic `Literal` for enums** — using `Literal["Male", "Female", "Other"]` for constrained string fields gives you free validation and OpenAPI docs.
- **API key auth** — adding auth at all to an ML endpoint is the right move, even if the implementation needs polishing.
- **`response_model`** — declaring `response_model=Predict_response` on the route is correct and produces clean OpenAPI output.

---

## Priority Fix List

| Priority | Issue | File |
|---|---|---|
| 🔴 Critical | Hardcoded absolute paths | `main.py` |
| 🔴 Critical | `ml[model]` KeyError (Enum vs string) | `predict_router.py` |
| 🔴 Critical | `python-dotenv` missing from requirements | `requirements.txt` |
| 🟠 High | Wrong HTTP status on auth failure (404 → 401) | `auth.py` |
| 🟠 High | `API_KEY=None` bypass risk | `auth.py` |
| 🟠 High | Test calls route function directly — broken | `test_predict_route.py` |
| 🟠 High | Encoder mismatch (hardcoded vs trained) | `predict_repository.py` |
| 🟡 Medium | No numeric field validation constraints | `prediction_input.py` |
| 🟡 Medium | No model load error handling | `main.py` |
| 🟡 Medium | Training notebook encoder bug | `student_placement_prediction.py` |
| ⚪ Low | Naming conventions (PEP 8) | everywhere |
| ⚪ Low | `print` → `logging` | `main.py` |
| ⚪ Low | Dead import (`_encode` in router) | `predict_router.py` |
