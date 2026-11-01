import pandas as pd

train_stations = {
    "12625": [
        "AGC", "AWY", "BAB", "BHA", "BINA", "BPL", "BPQ", "BVH",
        "BZA", "CBE", "CD", "CGY", "CHJ", "CNGR", "CTO", "ED",
        "ERN", "ET", "FDB", "FDN", "GDR", "GWL", "JHS", "JTJ",
        "KPD", "KSWR", "KTYM", "KYJ", "MJRI", "MTJ", "MVLK",
        "NGP", "NLR", "NUB", "NZM", "OKAC", "OTP", "PGT", "PWL",
        "QLN", "RDM", "RU", "SA", "SEGM", "SKZR", "SMTL", "TCR",
        "TPTY", "TRVL", "TUP", "TVC", "VAK", "VARD", "VGLB",
        "VGLJ", "WL"
    ],
    "16306": [
        "AFK", "AWY", "BDJ", "CAN", "CKI", "CLT", "ERN", "IJK",
        "KTU", "MAHE", "MGK", "PGI", "PTB", "SRR", "TA", "TCR",
        "TIR", "TLY", "WKI"
    ],
    "16325": [
        "AAM", "AFK", "AWY", "CKI", "CWR", "ERN", "ERSD", "ETM",
        "IJK", "IPL", "KDTY", "KFE", "KRPP", "KTYM", "KUC",
        "KZC", "MGK", "MLTR", "MNTT", "NIL", "PKQ", "PNQ",
        "PUK", "PVRD", "SRR", "TCR", "TRTR", "TUV", "VARD",
        "VNB", "VPZ", "VTK", "WKI"
    ],
    "16346": [
        "ALLP", "AMPA", "AWY", "BDJ", "BTJL", "BYNR", "CAN",
        "CHI", "CHV", "CLT", "CNO", "DINR", "ERS", "HAD",
        "KAWR", "KGQ", "KHED", "KPQ", "KPY", "KRMI", "KT",
        "KTU", "KUDA", "KUDL", "KYJ", "KZE", "LTT", "MAJN",
        "MAO", "MRDW", "NLE", "PAY", "PGI", "PNVL", "QLN",
        "RAJP", "RN", "ROHA", "SGR", "SL", "SRR", "SRTL",
        "TCR", "THVM", "TIR", "TLY", "TNA", "TVC", "UD",
        "VAK", "VVH", "XX-TNAB"
    ]
}

# Get station codes using a train number
# train_no = "16306"
# station_codes = train_stations.get(str(train_no), [])
# print(station_codes)







def extract_features(data: dict) -> pd.DataFrame:
    # Model features plus the arrival timestamp used for display.
    feature_cols = [
        'train_no', 'train_type', 'seq', 'station_code', 'halts_here',
        'platform', 'distance_km', 'previous_delay', 'previous_departure_delay',
        'previous_delay2', 'previous_delay3', 'previous_distance_diff',
        'last_three_delay_avg',
        'station_time_difference', 'is_weekend', 'month',
        'sch_arrival_hour', 'scheduled_arrival_iso'
    ]

    if not isinstance(data, dict):
        raise ValueError('Live railway data must be a dictionary')

    train_number = data.get('trainNumber')
    if train_number is None:
        raise ValueError('trainNumber missing from live API response')
    train_no = str(int(train_number))  # Training notebook treated this as text.

    train_info = data.get('train') or {}
    if not isinstance(train_info, dict):
        train_info = {}
    raw_type = str(train_info.get('type') or 'MEX').strip()
    type_upper = raw_type.upper()
    if type_upper == 'SUF' or 'SUPERFAST' in type_upper or 'SUPER FAST' in type_upper:
        train_type = 1
    elif type_upper == 'MEX' or 'EXPRESS' in type_upper or 'MAIL' in type_upper:
        train_type = 0
    else:
        raise ValueError(f'Unknown train type: {raw_type}')

    records = []
    for st in data.get('route') or []:
        if not isinstance(st, dict):
            continue
        station_code = str(st.get('stationCode') or '').strip().upper()
        stations = train_stations.get(str(train_no), [])
        if station_code not in stations:
            continue

        sch_arr = st.get('scheduledArrival') or st.get('scheduledDeparture')
        sch_dep = st.get('scheduledDeparture') or st.get('scheduledArrival')
        halt = st.get('haltsHere', st.get('halts_here', 1))
        if isinstance(halt, str):
            halt = 0 if halt.strip().lower() in ('false', 'no', '0') else 1

        records.append({
            'train_no': train_no,
            'train_type': train_type,
            'seq': st.get('sequence'),
            'station_code': station_code,
            'halts_here': halt,
            'delay_arrival_min': st.get('delayArrival'),
            'delay_departure_min': st.get('delayDeparture'),
            'platform': st.get('platform'),
            'distance_km': st.get('distance'),
            'sch_arrival_iso': sch_arr,
            'scheduled_arrival_iso': st.get('scheduledArrival'),
            'sch_departure_iso': sch_dep
        })

    df = pd.DataFrame(records)
    if df.empty:
        return pd.DataFrame(columns=feature_cols)

    # Fix API route ordering before shift()/rolling().
    df['seq'] = pd.to_numeric(df['seq'], errors='coerce')
    df = df.dropna(subset=['seq']).sort_values('seq', kind='stable').reset_index(drop=True)
    if df.empty:
        return pd.DataFrame(columns=feature_cols)

    # Clean numeric fields using the same categories as training.
    platform = df['platform'].astype('string').str.strip().str.upper()
    platform = platform.str.translate(str.maketrans('०१२३४५६७८९', '0123456789'))
    platform = platform.str.replace(r'^(\d+)\.0$', r'\1', regex=True)
    platform = platform.replace({'1A': '1', '3A': '3'})
    df['platform'] = pd.to_numeric(platform, errors='coerce').fillna(1).astype(float)

    df['halts_here'] = pd.to_numeric(df['halts_here'], errors='coerce').fillna(1).astype(float)
    df['distance_km'] = pd.to_numeric(df['distance_km'], errors='coerce')
    if df['distance_km'].isna().any():
        raise ValueError('distance missing in live route; cannot compute previous_distance_diff')
    df['delay_arrival_min'] = pd.to_numeric(df['delay_arrival_min'], errors='coerce')
    df['delay_departure_min'] = pd.to_numeric(df['delay_departure_min'], errors='coerce')

    # Same lag feature names and directions as training.
    df['previous_delay'] = df['delay_arrival_min'].shift(1)
    df['previous_departure_delay'] = df['delay_departure_min'].shift(1)
    df['previous_delay2'] = df['delay_arrival_min'].shift(2)
    df['previous_delay3'] = df['delay_arrival_min'].shift(3)
    df['previous_distance_diff'] = df['distance_km'].diff()
    df['last_three_delay_avg'] = (
        df['delay_arrival_min'].shift(1).rolling(3, min_periods=1).mean()
    )

    # Interpret naive ISO timestamps as India-local, and convert offset-aware
    # timestamps to India time. The notebook used local arrival date/hour.
    def as_ist(value):
        if value is None or pd.isna(value):
            return pd.NaT
        try:
            timestamp = pd.Timestamp(value)
            if pd.isna(timestamp):
                return pd.NaT
            return (timestamp.tz_localize('Asia/Kolkata')
                    if timestamp.tzinfo is None
                    else timestamp.tz_convert('Asia/Kolkata'))
        except (TypeError, ValueError):
            return pd.NaT

    arrivals = pd.to_datetime(df['sch_arrival_iso'].map(as_ist), errors='coerce')
    departures = pd.to_datetime(df['sch_departure_iso'].map(as_ist), errors='coerce')

    if arrivals.isna().any() or departures.isna().any():
        raise ValueError('Scheduled times must include valid dates and times')

    # The training notebook used HH:MM, not full timestamps, for this feature.
    df['scheduled_arrival'] = arrivals.dt.strftime('%H:%M')
    df['previous_sch_departure_date'] = departures.dt.strftime('%H:%M').shift(1)
    arrival_minutes = arrivals.dt.hour * 60 + arrivals.dt.minute
    previous_departure_minutes = departures.dt.hour.shift(1) * 60 + departures.dt.minute.shift(1)
    difference = arrival_minutes - previous_departure_minutes
    df['station_time_difference'] = difference.where(difference >= 0, difference + 1440)
    # Match the notebook's text categories, including its missing-value label.
    df['station_time_difference'] = df['station_time_difference'].map(
        lambda value: 'nan' if pd.isna(value) else str(float(value))
    )

    df['weekend'] = arrivals.dt.day_name().str[:3]
    df['is_weekend'] = df['weekend'].isin(['Sat', 'Sun']).astype(int)
    df['month'] = arrivals.dt.month
    df['sch_arrival_hour'] = arrivals.dt.hour
    

    for column in df.columns:
        if column == 'scheduled_arrival_iso':
            continue
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].fillna(0)
        else:
            df[column] = df[column].fillna('0')

    return df[feature_cols]
