# Training and preprocessing audit — 2026-11-02

## Scope and reproduction

Read all code cells and stored outputs in `notebooks/Train_Time_Delay_Prediction_(ML_Project)_(1) (3).ipynb`, inspected `src/ml/model.pkl`, and compared `src/ml/preprocessing.json` and `src/services/live_data_services.py` against the local training CSVs. Notebook cell numbers below are zero-based JSON cell indexes. No training or model replacement was performed.

The actual notebook corpus is `notebooks/data/railway_raw_combined.csv`: **173,636 raw rows**, **127,610 rows** after `reported == 1`, nonmissing `delay_arrival_min`, and full-row duplicate removal. The root-level `railway_raw_combined.csv` is a different corpus (269,793 rows; trains 12617, 12625, 16346, 12623, 16649) and must not be substituted silently.

To reproduce the comparisons, load the notebook CSV using pandas, apply the filter and duplicate removal above, parse `date` with `format="mixed"`, sort by `train_no`, `date`, `seq`, and group by `train_no`, `date`, as the notebook does. Compare each train's distinct `station_code` values and per-station modal `seq` with the runtime allowlist and metadata. Recreate `station_time_difference` from scheduled arrival clock minutes minus the previous retained row's scheduled departure clock minutes, adding 1440 for negative differences. Convert finite values to `str(float(value))` and missing values to the literal `"nan"`; sort the unique categories.

## Station and encoding results

| Train | Cleaned rows | Distinct training station codes | Allowlist differences | Metadata station differences |
| --- | ---: | ---: | ---: | ---: |
| 12625 | 55,586 | 56 | 0 | 0 |
| 16306 | 23,992 | 19 | 0 | 0 |
| 16325 | 9,206 | 33 | 0 | 0 |
| 16346 | 38,826 | 52 | 0 | 0 |

All **160 train/station pairs**, all modal sequence values, and all **475 time categories** match the runtime metadata exactly. These are internal training-to-runtime comparisons, not proof that every external API station/name is matched correctly. External timetable/live response matching requires a separate route audit.

## Evidence behind extreme forecasts

The target is arrival delay in **minutes**, without target scaling. Missing lag values are filled with zero in the notebook. The live feature extractor likewise fills unavailable lag values with zero, including histories for distant upcoming stations. Consequently an unknown future history is represented identically to a training row with no previous retained observations.

The training corpus contains these extreme first-retained-report examples:

| Train | Station | Journey date | Target minutes | Previous retained arrival delay |
| --- | --- | --- | ---: | --- |
| 16346 | ERS | 2022-04-20 | 2,890 | Missing, then encoded 0 |
| 16346 | TLY | 2024-07-14 | 1,490 | Missing, then encoded 0 |
| 12625 | TUP | 2022-03-17 | 2,924 | Missing, then encoded 0 |

ERS's scheduled arrival date is 20 April and actual arrival date is 22 April in that historical row. This demonstrates the recorded multi-day target; it does not prove whether the underlying historical observation is erroneous. Genuine long disruptions must not be removed solely because their delays are large.

No cleaned row with target greater than 1,000 minutes had a genuinely observed previous retained arrival delay below 100 minutes. The examples above have missing predecessors rather than observed low delays.

The persisted RandomForestRegressor has 147 features. Its feature importances include `previous_delay` **0.720689**, `last_three_delay_avg` **0.078919**, and `previous_departure_delay` **0.012226**. Invalid or absent history therefore materially affects the estimator. The evidence supports a mechanism for inflated predictions when future unknown histories become zero; it does not establish an exact causal attribution for the user's 304-minute result without that response and feature vector.

All four trains' minimum nonmissing training target is **2 minutes**. There are **zero zero-minute targets** in the cleaned corpus; 35,700 raw targets are missing. Missing targets cannot automatically be interpreted as on-time observations. Maximum targets are 2,924 / 1,501 / 1,481 / 2,890 minutes for trains 12625 / 16306 / 16325 / 16346 respectively.

## Notebook and artifact problems

- Cell 83 currently drops `halts_here`, but the deployed pickle expects that feature. Stored notebook outputs also disagree about its presence. The current notebook source is not a faithful reproducible description of the existing artifact.
- Cell 164 saves `model2`, the RandomForestRegressor, despite subsequent LightGBM development/evaluation using `model`. The reported LightGBM metrics do not describe the deployed RF.
- Cells 127 and 139 use a random row train/test split. Adjacent observations from the same journey can enter both sets. Recorded RF random-split R-squared is approximately **0.8399**, MAE **6.2709 minutes**; recorded five-fold CV R-squared in cell 148 is approximately **0.1515**. These are stored outputs, not newly reproduced validation results; later stored MAE also differs, reinforcing execution-state inconsistency.
- Cell 58 attempts inplace filling on a selected temporary DataFrame and has a stored chained-assignment warning. Cell 59 subsequently fills the main frame, so cell 58 alone is not evidence that NaNs reached the fitted estimator.
- Label encoders are repeatedly refitted in cell 121 rather than exported alongside the model. Runtime metadata was reconstructed separately. It currently matches the local corpus, but future retraining can silently break the contract.
- Historical lag calculation follows the **retained reported rows**, not necessarily every scheduled station. Applying the same shifts over all future timetable stops does not reproduce the training observation process.

## Recommended repair and validation

1. Distinguish observed history from missing history. Do not make distant future predictions using fabricated zero lags. Return an explicit unavailable reason when the model's required observations are absent.
2. Keep station identity checks explicit at the API boundary; do not encode unknown stations as an all-zero known baseline.
3. Rebuild training and inference around one shared feature contract, exporting model, categories, station vocabulary, feature order and provenance together.
4. Evaluate with held-out journeys and chronological splits, comparing against a last-observed-delay baseline. Report error by train, station and forecast horizon.
5. Investigate isolated multi-day historical observations using source provenance before filtering or correcting them. Do not hide the defect by clipping predictions at an arbitrary minute threshold.

This audit does not claim that a five-hour train delay is impossible. It identifies why this model can produce an unsupported large estimate from incomplete live inputs.
