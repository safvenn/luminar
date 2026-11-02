const $ = (id) => document.getElementById(id);
function applyTheme(dark) {
  document.documentElement.dataset.theme = dark ? 'dark' : 'light';
  $('theme-toggle').setAttribute('aria-pressed', String(dark));
  $('theme-toggle').setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
  $('theme-toggle').title = dark ? 'Switch to light mode' : 'Switch to dark mode';
  document.querySelector('meta[name="theme-color"]').content = dark ? '#101827' : '#f8f9fc';
}
applyTheme(document.documentElement.dataset.theme === 'dark');
$('theme-toggle').addEventListener('click', () => {
  const dark = document.documentElement.dataset.theme !== 'dark';
  applyTheme(dark);
  try { localStorage.setItem('railcast-theme', dark ? 'dark' : 'light'); } catch {}
});
let report = null;
let busy = false;

// Initialize journey date with today's date in local time
try {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  if ($('journey-date') && !$('journey-date').value) {
    $('journey-date').value = `${year}-${month}-${day}`;
  }
} catch {}

function centerCurrentStation() {
  const route = $('route-stations');
  const current = route.querySelector('.current-station');
  if (!current) return;
  const offset = current.getBoundingClientRect().left - route.getBoundingClientRect().left;
  route.scrollTo({ left: route.scrollLeft + offset - route.clientWidth / 2 + current.clientWidth / 2,
    behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
}
function currentStationIndex(data) {
  const observed = data.data.findIndex(station => station.live_status === 'current');
  if (observed >= 0) return observed;
  const location = data.current_location;
  if (!location) return -1;
  const code = String(typeof location === 'string' ? location : location.stationCode || '').trim().toUpperCase();
  const exact = data.data.findIndex(station => String(station.station_code).trim().toUpperCase() === code);
  if (exact >= 0) return exact;
  // A non-halting current station may be absent from this halt-only route.
  if (typeof location.sequence !== 'number') {
    // Show the last known stop when the live location is between listed stops.
    return data.data.reduce((last, station, index) => station.live_status === 'passed' ? index : last, -1);
  }
  let latest = -1;
  data.data.forEach((station, index) => {
    if (typeof station.seq === 'number' && station.seq <= location.sequence &&
        (latest < 0 || station.seq > data.data[latest].seq)) latest = index;
  });
  return latest;
}
function message(text, error = false) { $('form-message').textContent = text; $('form-message').classList.toggle('error', error); }
function canPredict() { return Boolean(report && report.prediction_available !== false && canSelectStation($('station').value)); }
function setBusy(value) { busy = value; $('find-button').disabled = value; $('train-number').disabled = value; $('journey-date').disabled = value; $('station').disabled = value || !report || report.prediction_available === false || !report.data.some(station => canSelectStation(station.station_code)); $('predict-button').disabled = value || !canPredict(); }
async function request(path, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 60000);
  try {
    const response = await fetch(path, { ...options, signal: controller.signal });
    const data = await response.json().catch(() => null);
    if (!response.ok) throw new Error(typeof data?.detail === 'string' ? data.detail : 'The railway service is unavailable. Please try again.');
    if (!data) throw new Error('The server returned an unreadable response. Please try again.');
    return data;
  } catch (error) {
    if (error.name === 'AbortError') throw new Error('This request took too long. Please try again.');
    if (error instanceof TypeError) throw new Error('Unable to connect. Make sure the train API is running.');
    throw error;
  } finally { clearTimeout(timeout); }
}
function resetResult() { $('empty-result').hidden = false; $('prediction-result').hidden = true; $('result-badge').textContent = report?.prediction_available === false ? 'LIVE STATUS ONLY' : report && !report.data.some(station => canSelectStation(station.station_code)) ? 'NO UPCOMING ARRIVALS' : report ? 'READY TO PREDICT' : 'AWAITING JOURNEY'; $('result-caption').textContent = 'Powered by your train delay prediction model'; }
function estimatedArrival(scheduledArrival, delay, predictedTime) {
  const parseTime = (value) => {
    const match = /^(\d{1,2}):(\d{2})(?::(\d{2}))?$/.exec(String(value ?? '').trim());
    if (!match) return null;
    const [, hours, minutes, seconds = '0'] = match;
    if (+hours > 23 || +minutes > 59 || +seconds > 59) return null;
    return +hours * 3600 + +minutes * 60 + +seconds;
  };
  const scheduledSeconds = parseTime(scheduledArrival);
  const arrivalSeconds = scheduledSeconds === null ? parseTime(predictedTime) : scheduledSeconds + delay * 60;
  if (arrivalSeconds === null || !Number.isFinite(arrivalSeconds)) return 'Unavailable';
  const secondsInDay = ((arrivalSeconds % 86400) + 86400) % 86400;
  const hours = Math.floor(secondsInDay / 3600);
  const period = hours >= 12 ? 'PM' : 'AM';
  const minutes = String(Math.floor(secondsInDay % 3600 / 60)).padStart(2, '0');
  return `${hours % 12 || 12}:${minutes} ${period}`;
}
function isHaltingStation(station) { return station?.halts_here === true || station?.halts_here === 1; }
function hasPassed(station) {
  if (!report) return false;
  const lastPassed = report.data.reduce((last, stop, index) => stop.live_status === 'passed' ? index : last, -1);
  return report.data.indexOf(station) <= lastPassed;
}
function canSelectStation(code) { return Boolean(report?.data.some(station => String(station.station_code) === code && isHaltingStation(station) && station.prediction_available === true && station.scheduled_arrival && !hasPassed(station))); }
function selectStation(code) { if (busy || report?.prediction_available === false) return; if (!canSelectStation(code)) code = ''; $('station').value = code; $('predict-button').disabled = !canPredict(); resetResult(); document.querySelectorAll('.station-stop').forEach(button => button.classList.toggle('selected', button.dataset.code === code)); }
$('station').addEventListener('change', () => selectStation($('station').value));
function resetJourney() {
  report = null;
  resetResult();
  $('route-panel').hidden = true;
  $('station').replaceChildren(new Option('Find a train to see its stations', ''));
  $('find-button').textContent = 'Find my train →';
  setBusy(false);
  message('Find your selected train to load its latest status.');
}
$('train-number').addEventListener('change', resetJourney);
$('journey-date').addEventListener('change', resetJourney);
$('train-form').addEventListener('submit', async (event) => {
  event.preventDefault(); if (busy) return;
  const number = $('train-number').value.trim(); if (!/^\d{5}$/.test(number)) return;
  const date = $('journey-date')?.value?.trim() || '';
  await loadTrain(number, date);
});
async function loadTrain(number, date = '') {
  if (busy) return;
  report = null; resetResult(); $('route-panel').hidden = true; $('station').replaceChildren(new Option('Loading stations…', ''));
  $('find-button').textContent = 'Finding your train…'; message('Fetching the latest running information…');
  setBusy(true);
  $('route-refresh-status').textContent = 'Updating live train location…';
  try {
    const query = `/live?train_no=${encodeURIComponent(number)}${date ? `&date=${encodeURIComponent(date)}` : ''}`;
    const data = await request(query);
    if (!Array.isArray(data.data) || !data.data.length) throw new Error('No stops were found for this train. Select another train.');
    const haltingStops = data.data.filter(isHaltingStation);
    if (!haltingStops.length) throw new Error('No halting stations were found for this train. Select another train.');
    report = { ...data, data: haltingStops }; $('station').replaceChildren(new Option('Select your arrival station', ''));
    $('route-stations').replaceChildren();
    const currentIndex = currentStationIndex(report);
    const currentLabel = report.data[currentIndex]?.live_status === 'current' ? 'Current station' : 'Last reported stop';
    for (const [index, station] of report.data.entries()) {
      const isCurrentStation = index === currentIndex;
      const code = String(station.station_code);
      const scheduledTime = station.scheduled_arrival
        ? estimatedArrival(station.scheduled_arrival, 0, null, station.arrival_day_offset)
        : `Departs ${estimatedArrival(station.scheduled_departure, 0, null, station.departure_day_offset)}`;
      const option = new Option(`${code} · ${scheduledTime}${hasPassed(station) ? ' · Passed' : isCurrentStation ? ` · ${currentLabel}` : ''}`, code);
      option.disabled = !canSelectStation(code);
      $('station').add(option);
      const button = document.createElement('button'); button.type = 'button'; button.className = 'station-stop'; button.dataset.code = code;
      button.disabled = !canSelectStation(code) || report.prediction_available === false;
      button.setAttribute('aria-label', `${code}, ${scheduledTime}${station.live_status === 'passed' ? ', already passed' : ''}`);
      button.classList.toggle('travelled', index < currentIndex);
      const name = document.createElement('strong'); name.textContent = code;
      const time = document.createElement('span'); time.textContent = scheduledTime;
      const distance = document.createElement('span'); distance.textContent = `${station.distance_km ?? '—'} km`;
      button.append(name, time, distance);
      if (!station.prediction_available && station.prediction_reason) {
        button.title = station.prediction_reason;
        const reason = document.createElement('span');
        reason.textContent = station.prediction_reason;
        button.append(reason);
      }
      if (station.live_date) {
        const dateSpan = document.createElement('span');
        dateSpan.className = 'station-date';
        dateSpan.textContent = `📅 ${station.live_date}`;
        button.append(dateSpan);
      }
      if (typeof station.live_delay_min === 'number') {
        const live = document.createElement('span');
        live.textContent = `${station.live_status === 'upcoming' ? 'API estimate' : 'Reported'}: ${station.live_delay_min === 0 ? 'on time' : `${Math.abs(station.live_delay_min)} min ${station.live_delay_min < 0 ? 'early' : 'late'}`}`;
        button.append(live);
      }
      if (isCurrentStation) {
        button.classList.add('current-station');
        const marker = document.createElement('span');
        marker.className = 'terminal-train';
        marker.setAttribute('aria-hidden', 'true');
        const icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
        use.setAttribute('href', '#train-icon');
        icon.append(use);
        marker.append(icon);
        button.append(marker);
        const label = document.createElement('span');
        label.className = 'terminal-label';
        label.textContent = currentLabel;
        button.append(label);
      }
      button.addEventListener('click', () => { selectStation(code); $('station').focus(); }); $('route-stations').append(button);
    }
    const dateTitle = report.journey_date ? ` · ${report.journey_date}` : '';
    $('route-title').textContent = `${report.train_name || 'Train'} · ${report.train_no || number}${dateTitle}`;
    $('route-count').textContent = `${report.data.length} STOPS`; $('route-panel').hidden = false;
    $('station').value = '';
    resetResult();
    const location = typeof report.current_location === 'string' ? report.current_location : report.current_location?.name || report.current_location?.stationCode;
    const delay = report.current_delay;
    const delayText = typeof delay === 'number' ? delay === 0 ? 'On time' : `${Math.abs(delay)} min ${delay < 0 ? 'early' : 'late'}` : 'Delay unavailable';
    const datePrefix = report.journey_date ? `Journey date: ${report.journey_date} · ` : '';
    $('route-refresh-status').textContent = `${datePrefix}${location ? `Last reported location: ${location}` : 'Location unavailable'} · ${delayText}${report.last_updated ? ` · Source updated ${report.last_updated.replace(/,+$/, '')} IST` : ''} · Refresh train for the latest status. Days are counted from departure.`;
    requestAnimationFrame(centerCurrentStation);
    $('route-panel').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'start' });
    message(report.prediction_available === false ? report.prediction_message || 'Live status is available, but prediction is not ready yet.' : report.data.some(station => canSelectStation(station.station_code)) ? 'Train found. Choose an upcoming arrival station below.' : 'There are no upcoming arrivals on this journey. Refresh for a new run or choose another train.');
  } catch (error) {
    report = null;
    $('station').replaceChildren(new Option('Find a train to see its stations', '')); message(error.message, true);
  }
  finally { setBusy(false); $('find-button').textContent = report ? 'Refresh train ↻' : 'Find my train →'; }
}
$('prediction-form').addEventListener('submit', async (event) => {
  event.preventDefault(); if (busy || !report) return;
  if (report.prediction_available === false) { message(report.prediction_message || 'Prediction is unavailable.', true); return; }
  if (!canSelectStation($('station').value)) { selectStation(''); message('Choose a station where this train halts.', true); return; }
  const station = $('station').value; setBusy(true); resetResult(); $('predict-button').textContent = 'Calculating arrival…'; message('Your arrival outlook is on its way…');
  try {
    const data = await request(`/predict?station_code=${encodeURIComponent(station)}&report_id=${encodeURIComponent(report.report_id)}`, { method: 'POST' });
    const delay = data.predicted_delay_arrival_min;
    if (typeof delay !== 'number' || !Number.isFinite(delay)) throw new Error('The model returned an invalid prediction. Please try again.');
    if (data.report_id !== report.report_id || String(data.train_no) !== String(report.train_no) || String(data.station_code).toUpperCase() !== station.toUpperCase()) throw new Error('The active train data changed. Find your train again before predicting.');
    $('result-train').textContent = `${report.train_name || 'Train'} · ${data.train_no}`; $('result-station').textContent = `Arriving at ${data.station_code}`;
    const selectedStop = report.data.find(stop => String(stop.station_code).trim().toUpperCase() === station.trim().toUpperCase());
    $('delay-value').textContent = `${Math.abs(delay).toFixed(1)} min`;
    $('arrival-value').textContent = estimatedArrival(selectedStop?.scheduled_arrival, delay, data.predict_time, selectedStop?.arrival_day_offset);
    $('arrival-value').classList.toggle('unavailable', $('arrival-value').textContent === 'Unavailable');
    $('result-badge').textContent = delay > 0 ? 'ESTIMATED DELAY' : delay < 0 ? 'EXPECTED EARLY' : 'EXPECTED ON TIME';
    $('empty-result').hidden = true; $('prediction-result').hidden = false;
    $('result-caption').textContent = `Prediction updated at ${new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true })}`;
    message(data.prediction_note
      ? data.prediction_note
      : 'Your prediction is ready. Travel times are estimates, so allow a little flexibility.');
  } catch (error) { message(error.message, true); }
  finally { setBusy(false); $('predict-button').textContent = 'Predict arrival →'; }
});
