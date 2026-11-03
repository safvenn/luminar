import copy
import unittest
from time import time

from fastapi import HTTPException
from src.depends.db import reports
from src.services.predict_services import predict_services


class RecordingModel:
    feature_names_in_ = ["train_no", "previous_delay", "previous_delay2", "previous_delay3",
                         "previous_departure_delay", "last_three_delay_avg", "station_time_difference"]

    def __init__(self):
        self.inputs = []

    def predict(self, frame):
        self.inputs.append(frame.iloc[0].to_dict())
        return [float(frame.iloc[0]["previous_delay"]) + 2]


class RecursivePredictionTests(unittest.TestCase):
    def setUp(self):
        reports.clear()
        self.rows = []
        for seq, code in enumerate(["TVC", "VAK", "QLN", "KYJ", "HAD", "AMPA", "ALLP"]):
            observed = seq < 3
            self.rows.append({
                "station_code": code, "seq": seq, "train_no": "16346", "current_route": True,
                "live_status": "passed" if observed else "upcoming",
                "live_delay_min": [20, 24, 27][seq] if observed else 999,
                "prediction_available": not observed,
                "model_features": {"train_no": "16346", "station_code": code,
                    "station_time_difference": 0, "scheduled_arrival_iso": "2026-11-03T23:50:00+05:30"},
            })
        reports.append({"report_id": "test", "created_at": time(), "data": self.rows})
        self.model = RecordingModel()

    def predict(self):
        return predict_services("ALLP", self.model, "test")

    def test_four_steps_use_predictions_without_mutating_observations(self):
        before = copy.deepcopy(reports)
        result = self.predict()
        self.assertEqual([s["predicted_delay_arrival_min"] for s in result["prediction_steps"]], [29, 31, 33, 35])
        self.assertEqual(result["predict_time"], "00:25:00")
        fourth = self.model.inputs[-1]
        self.assertEqual([fourth[k] for k in ["previous_delay", "previous_delay2", "previous_delay3"]], [33, 31, 29])
        self.assertEqual(fourth["last_three_delay_avg"], 31)
        self.assertEqual(fourth["previous_departure_delay"], 33)
        self.assertEqual(reports, before)
        self.assertEqual(self.predict()["predicted_delay_arrival_min"], 35)

    def test_new_observation_replaces_previous_prediction(self):
        self.predict()
        self.rows[3].update(live_status="passed", live_delay_min=35, prediction_available=False)
        result = self.predict()
        self.assertEqual(result["predicted_delay_arrival_min"], 41)
        self.assertEqual(len(result["prediction_steps"]), 3)

    def test_observed_zero_is_valid(self):
        for row in self.rows[:3]:
            row["live_delay_min"] = 0
        self.assertEqual(self.predict()["predicted_delay_arrival_min"], 8)

    def test_missing_or_invalid_latest_observation_rejected(self):
        for value in [None, float("nan"), float("inf"), "invalid"]:
            with self.subTest(value=value):
                self.rows[2]["live_delay_min"] = value
                with self.assertRaises(HTTPException) as error:
                    self.predict()
                self.assertEqual(error.exception.status_code, 422)
        self.assertEqual(self.model.inputs, [])

    def test_no_observations_rejected(self):
        for row in self.rows:
            row["live_status"] = "upcoming"
        with self.assertRaises(HTTPException):
            self.predict()

    def test_unsupported_intermediate_station_blocks_target(self):
        self.rows[3]["prediction_available"] = False
        with self.assertRaises(HTTPException) as error:
            self.predict()
        self.assertIn("KYJ", error.exception.detail)
        self.assertEqual(self.model.inputs, [])

    def test_historical_station_is_excluded_and_route_is_sorted(self):
        self.rows.append({"station_code": "OLD", "seq": 3.5, "current_route": False})
        self.rows.reverse()
        self.assertEqual(self.predict()["predicted_delay_arrival_min"], 35)

    def test_nonfinite_model_output_rejected(self):
        self.model.predict = lambda frame: [float("nan")]
        with self.assertRaises(HTTPException) as error:
            self.predict()
        self.assertEqual(error.exception.status_code, 422)

    def test_short_observed_history_uses_training_start_padding(self):
        self.rows[0]["live_delay_min"] = None
        self.rows[1]["live_delay_min"] = None
        self.predict()
        first = self.model.inputs[0]
        self.assertEqual(first["previous_delay"], 27)
        self.assertEqual(first["previous_delay2"], 0)
        self.assertEqual(first["last_three_delay_avg"], 27)
