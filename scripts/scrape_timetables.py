"""Refresh fixed timetables from public HTML; never calls a timetable API.

Run from any directory: python scripts/scrape_timetables.py
Historical-only stations are explicitly labelled and kept off the current route.
"""
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.services.live_data_services import train_stations


class ScheduleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.cells = None
        self.text = None
        self.code = None

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.cells, self.code = [], None
        elif tag == 'td' and self.cells is not None:
            self.text = []
        elif tag == 'a' and self.cells is not None:
            href = dict(attrs).get('href', '')
            match = re.fullmatch(r'/station/([A-Z0-9-]+)', href)
            if match:
                self.code = match.group(1)

    def handle_data(self, data):
        if self.text is not None:
            self.text.append(data)

    def handle_endtag(self, tag):
        if tag == 'td' and self.text is not None:
            self.cells.append(' '.join(''.join(self.text).split()))
            self.text = None
        elif tag == 'tr' and self.cells is not None:
            if self.code and len(self.cells) == 8:
                self.rows.append((self.code, self.cells))
            self.cells = None


def clock(value):
    value = str(value).strip()
    return value + ':00' if re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', value) else None


def minute(value, day):
    if value is None or day is None:
        return None
    hour, minutes = map(int, value.split(':')[:2])
    return day * 1440 + hour * 60 + minutes


def adjacent(row, previous):
    row['previous_station_code'] = previous['code'] if previous else None
    row['distance_from_previous_km'] = (round(row['distance_km'] - previous['distance_km'], 3)
                                         if previous else 0.0)
    arrival = minute(row['arrival'], row['arrival_day_offset'])
    departure = minute(previous['departure'], previous['departure_day_offset']) if previous else None
    row['minutes_from_previous_station'] = arrival - departure if arrival is not None and departure is not None else None


def scrape(train):
    url = f'https://www.confirmtkt.com/train-schedule/{train}'
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    parser = ScheduleParser()
    parser.feed(response.text)
    result = []
    for code, cells in parser.rows:
        arrival, departure = clock(cells[2]), clock(cells[3])
        day = int(cells[7]) - 1
        # The HTML Day column is the arrival day; a midnight halt can depart next day.
        departure_day = day + int(bool(arrival and departure and departure < arrival))
        row = dict(code=code, name=cells[1].rsplit(' - ', 1)[0], seq=int(cells[0]),
                   arrival=arrival, departure=departure, arrival_day_offset=day if arrival else None,
                   departure_day_offset=departure_day if departure else None,
                   distance_km=float(cells[5].replace('km', '').strip()), available=True,
                   current_route=True, training_station=code in train_stations[train],
                   schedule_source='public_html', source=url, unavailable_reason=None)
        if result and (row['seq'] <= result[-1]['seq'] or row['distance_km'] < result[-1]['distance_km']):
            raise ValueError(f'{train}: invalid timetable order')
        adjacent(row, result[-1] if result else None)
        result.append(row)
    if len(result) < 10 or len({r['code'] for r in result}) != len(result):
        raise ValueError(f'{train}: incomplete or duplicate HTML timetable')
    return url, result


def historical_rows(train, missing):
    path = ROOT / 'notebooks' / 'data' / 'raw' / f'{train}.csv'
    if not path.exists():
        return []
    frame = pd.read_csv(path, low_memory=False)
    frame['station_code'] = frame['station_code'].astype(str).str.strip().str.upper()
    frame['_arrival'] = pd.to_datetime(frame['sch_arrival_date'] + ' ' + frame['sch_arrival'], errors='coerce', format='%d %b %Y %H:%M')
    frame['_departure'] = pd.to_datetime(frame['sch_departure_date'] + ' ' + frame['sch_departure'], errors='coerce', format='%d %b %Y %H:%M')
    frame['_journey'] = pd.to_datetime(frame['date'], errors='coerce')
    frame = frame.dropna(subset=['distance_km', 'seq', '_arrival', '_departure', '_journey'])
    frame = frame.sort_values(['_journey', 'seq'], kind='stable')
    result = []
    for code in missing:
        candidates = frame[frame.station_code == code]
        if candidates.empty:
            continue
        record = candidates.iloc[-1]
        def convert(r):
            return dict(code=r.station_code, arrival=r['_arrival'].strftime('%H:%M:%S'),
                        departure=r['_departure'].strftime('%H:%M:%S'),
                        arrival_day_offset=int((r['_arrival'].normalize()-r['_journey']).days),
                        departure_day_offset=int((r['_departure'].normalize()-r['_journey']).days),
                        distance_km=float(r.distance_km))
        row = convert(record)
        previous = frame[(frame['_journey'] == record['_journey']) & (frame.seq < record.seq)]
        adjacent(row, convert(previous.iloc[-1]) if not previous.empty else None)
        row.update(name=code, seq=float(record.seq), available=True, current_route=False,
                   training_station=True, schedule_source='training_history',
                   source=path.relative_to(ROOT).as_posix(), historical_journey_date=str(record['date']),
                   unavailable_reason='Not present in the scraped current timetable; historical schedule only.')
        result.append(row)
    return result


def main():
    metadata = json.loads((ROOT / 'src' / 'ml' / 'preprocessing.json').read_text(encoding='utf-8'))
    output = dict(schema_version=1, scraped_at=datetime.now(timezone.utc).isoformat(),
                  source_type='public_html_with_explicit_training_history', trains={})
    for train, codes in train_stations.items():
        url, rows = scrape(train)
        current_codes = {r['code'] for r in rows}
        rows.extend(historical_rows(train, sorted(set(codes)-current_codes)))
        available_codes = {r['code'] for r in rows}
        for code in sorted(set(codes)-available_codes):
            rows.append(dict(code=code, name=code, seq=None, arrival=None, departure=None,
                             arrival_day_offset=None, departure_day_offset=None, distance_km=None,
                             previous_station_code=None, distance_from_previous_km=None,
                             minutes_from_previous_station=None, available=False, current_route=False,
                             training_station=True, schedule_source='unavailable', source=url,
                             unavailable_reason='Absent from current timetable and no complete historical schedule.'))
        for row in rows:
            row['training_seq'] = metadata['station_sequences'][train].get(row['code'])
        output['trains'][train] = dict(source_url=url, train_name={'12625':'Kerala Express','16306':'Kannur Ernakulam Express','16325':'Nilambur Road Kottayam Express','16346':'Netravati Express'}[train], stations=rows)
        print(f'{train}: {len(current_codes)} current, {sum(r["schedule_source"] == "training_history" for r in rows)} historical, {sum(not r["available"] for r in rows)} unavailable')
    destination = ROOT / 'src' / 'data' / 'train_timetables.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(output, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    temporary.replace(destination)


if __name__ == '__main__':
    main()
