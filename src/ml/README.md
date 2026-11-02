The existing model expects the notebook's encoded inputs.

`preprocessing.json` contains the sorted time-difference categories and the
most common training sequence number for each train/station pair. These were
recovered from the notebook's four training CSVs, after its reported-row filter,
duplicate removal, and journey grouping. Counts match the notebook: 127,610
cleaned rows and 475 time categories. Export these again when retraining.

Live prediction assumptions:
- Match live stops to timetable stations by distance, close proximity, or station name/code aliases.
- Reconcile live delays by using the live API's verified delayMin over raw timetable subtractions when timetables disagree.
- Include observations from both passed stations and the current active station in the delay history.
- Do not artificially forward-fill delays across upcoming stops; maintain true observed previous-station history as seen during training.
- Initial or unobserved history defaults to zero, consistent with training preprocessing.
- Use platform 1 because this API has no platform information.

These estimates depend on timetable accuracy. They do not establish that the
model has been validated on this new API source.
