import copy
import json
import unittest
from pathlib import Path
from fastapi import HTTPException
from src.services.live_prediction import add_prediction_features
from src.routes.live_data import match_station_stop

ROOT = Path(__file__).resolve().parents[1]
class PredictionSafetyTests(unittest.TestCase):
    def test_ers_missing_history_is_unavailable(self):
        report = json.loads((ROOT / "docs/ers_16346_2026-11-02_before_fix.json").read_text())["report"]
        rows = copy.deepcopy(report["data"])
        live = {"trainNumber": "16346", "updatedAt": "2026-11-02T06:53:15Z", "stops": report["live_stops"]}
        add_prediction_features(rows, live, "MEX")
        ers = next(r for r in rows if r["station_code"] == "ERS")
        self.assertNotIn("model_features", ers)
        self.assertFalse(ers["prediction_available"])

    def test_identity_beats_wrong_distance(self):
        stops = [{"stationName": "Vallattolnagar", "distanceKm": 57}, {"stationName": "Vailapuzha", "distanceKm": None}]
        row = {"station_code": "VPZ", "station_name": "VALLAPUZHA", "distance_km": 57}
        self.assertEqual(match_station_stop(row, stops, set())[0], 1)

    def test_ambiguous_identity_rejected(self):
        row = {"station_code": "ERS", "station_name": "Ernakulam Junction", "distance_km": 200}
        stops = [{"stationName": "Ernakulam Junction", "distanceKm": 200}] * 2
        self.assertIsNone(match_station_stop(row, stops, set())[0])

class JourneyContractTests(unittest.TestCase):
    def setUp(self):
        from src.depends.db import reports
        reports.clear()
        self.reports = reports

    def test_observed_zero_history_remains_valid(self):
        report = json.loads((ROOT / "docs/ers_16346_2026-11-02_before_fix.json").read_text())["report"]
        rows = copy.deepcopy(report["data"])
        index = next(i for i, r in enumerate(rows) if r["station_code"] == "ERS")
        for row in rows[:index]:
            row.update(live_status="passed", live_delay_min=0)
        live = {"trainNumber": "16346", "updatedAt": "2026-11-02T06:53:15Z", "stops": report["live_stops"]}
        add_prediction_features(rows, live, "MEX")
        self.assertTrue(rows[index]["prediction_available"])
        self.assertEqual(rows[index]["model_features"]["previous_delay"], 0)

    def test_missing_api_delay_does_not_use_clock_subtraction(self):
        report = json.loads((ROOT / "docs/ers_16346_2026-11-02_before_fix.json").read_text())["report"]
        rows = copy.deepcopy(report["data"])
        index = next(i for i, r in enumerate(rows) if r["station_code"] == "ERS")
        for row in rows[:index]:
            row.update(live_status="passed", live_delay_min=0)
        rows[index - 1]["live_delay_min"] = None
        rows[index - 1]["live_arrival"] = "23:59"
        live = {"trainNumber": "16346", "updatedAt": "2026-11-02T06:53:15Z", "stops": report["live_stops"]}
        add_prediction_features(rows, live, "MEX")
        self.assertFalse(rows[index]["prediction_available"])

    def test_all_routes_and_report_isolation(self):
        from unittest.mock import patch
        from fastapi.testclient import TestClient
        from src.main import app
        import numpy as np
        class Model:
            feature_names_in_ = np.array(["train_no", "previous_delay", "station_time_difference", "station_code_ERS"])
            def predict(self, frame):
                return [float(frame.iloc[0]["previous_delay"])]
        app.state.model = Model()
        client = TestClient(app)
        fixtures = json.loads((ROOT / "docs/station_api_audit_2026-11-02.json").read_text())["trains"]
        result = {}
        for train, fixture in fixtures.items():
            def fetch(number, endpoint, date=None):
                return copy.deepcopy(fixture["live" if endpoint == "live" else "timetable"])
            with patch("src.routes.live_data.fetch_train_data", side_effect=fetch):
                response = client.get("/live", params={"train_no": train, "date": "2026-11-02"})
            self.assertEqual(response.status_code, 200, response.text)
            result[train] = response.json()
            self.assertTrue(all("live_status" in row for row in result[train]["data"]))
            for row in result[train]["data"]:
                self.assertNotIn("model_features", row)
                self.assertIn("prediction_available", row)
                if not row["prediction_available"]:
                    response = client.post("/predict", params={"station_code": row["station_code"], "report_id": result[train]["report_id"]})
                    self.assertEqual(response.status_code, 422)
        original = self.reports[0]
        station = next(row for row in original["data"] if row["station_code"] == "NZM")
        station.update(prediction_available=True, model_features={"train_no": "12625", "station_code": "NZM", "previous_delay": 17, "station_time_difference": 0})
        station["station_code"] = "NZM"
        response = client.post("/predict", params={"station_code": "NZM", "report_id": original["report_id"]})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["train_no"], "12625")
        self.assertEqual(response.json()["predicted_delay_arrival_min"], 17)
        self.assertEqual(client.post("/predict", params={"station_code": "NZM"}).status_code, 422)
        self.assertEqual(client.post("/predict", params={"station_code": "NZM", "report_id": "missing"}).status_code, 409)
        original["created_at"] = 0
        self.assertEqual(client.post("/predict", params={"station_code": "NZM", "report_id": original["report_id"]}).status_code, 409)

if __name__ == "__main__":
    unittest.main()
