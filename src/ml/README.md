The existing model and notebook are unchanged by the November 2 prediction fix.

preprocessing.json retains the notebook's 475 time categories and train-specific
station sequence values. Train codes: 12625=0, 16306=1, 16325=2, 16346=3;
train types MEX=0, SUF=1. AAM is the dropped station dummy baseline.

Live forecasts require an upcoming arrival with observed delays at the preceding
three supported stops. Missing history stays missing, not zero. Genuine reported
zero delays remain valid. Unknown stations/time categories are unavailable.
Only observed finite API delayMin is used; separate timetable subtraction is not
an acceptable substitute. Platform still defaults to 1. Provider upcoming delays
are displayed as API estimates and are never treated as observations.

/live returns report_id and per-station prediction_available/prediction_reason.
/predict requires station_code and report_id. Reports expire after 30 minutes;
the last 100 are retained in process memory. Use a shared report store before
running multiple workers; an unknown report asks the client to refresh.

Station matching uses unique codes/names and explicit spelling aliases, never
proximity alone. Captured all-train API audit: docs/station_api_audit_2026-11-02.json.
Validation: docs/prediction_fix_validation.json. All 140 timetable rows match;
NDLS/12625 and ERS/16306 remain outside training coverage.

The saved model still has training limitations (see docs/training_audit_2026-11-02.md).
This patch prevents unsupported input forecasts; it does not retrain or establish
accuracy on this provider. No arbitrary output cap is applied.

Run from the project root: .venv312/Scripts/python.exe -m unittest discover -s tests -v
API tests require the TestClient dependency for your Starlette version (httpx2
for the installed version, or httpx on older releases).
