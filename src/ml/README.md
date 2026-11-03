# Prediction inputs

Notebook, model, and existing categorical encodings are unchanged.

Fixed station data lives in src/data/train_timetables.json. The runtime reads
this file; it never calls the train-information API. /timetable returns every
station in the training list, without making a network request. /live adds the
live running status from the provider. /predict uses that report_id.

Refresh the file manually from the project root:

    python scripts/scrape_timetables.py

The script scrapes public Confirmtkt HTML and saves schedules, day offsets,
origin distances, adjacent distances/times, and provenance. No new runtime
library is required. All 160 training pairs are included: 139 current and 21
historical. Historical entries use existing CSV records, are labelled clearly,
and are displayed only; mixing them into a current route would corrupt history.
The notebook and datasets are read only by this optional refresh script.

/predict rebuilds delay history on private feature copies, starting with
observed delays and predicting each upcoming current-route station through
the target. Intermediate estimates update all three lags, their average and
previous departure delay. Departure delay is assumed equal to arrival delay.
Stored templates may contain zeros; all five history fields are replaced
before each model call. Forecasts never overwrite live observations.

A refreshed report supplies new actual values. Missing latest observed delay
or unsupported intermediate inputs return HTTP 422. Earlier missing observations
are skipped; absent older startup lags use zero padding, while averages use
available history. Historical stations are excluded. See ../../README.md for
evaluation limits and API details. No retraining or output capping is performed.

Reports expire after 30 minutes and retain the latest 100 in memory. The deployed
service uses one worker. Both /predict parameters are required: station_code and
report_id. The report identifies its train and journey.

Run tests from the project root:

    python -m unittest discover -s tests -v
    node tests/frontend.test.cjs

TestClient requires httpx2 for the installed Starlette version (httpx for older
versions). See docs/training_audit_2026-11-02.md for model limitations.
