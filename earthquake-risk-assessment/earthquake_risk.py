import requests
import pandas as pd
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from collections import defaultdict

# Exclude Hawaii and territories
EXCLUDED_STATES = {'HI'}

# Geocoder
geolocator = Nominatim(user_agent="risk_assessor")

# Fetch USGS earthquake data for the past 7 days
def fetch_earthquake_data():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d"),
        "endtime": datetime.utcnow().strftime("%Y-%m-%d"),
        "minlatitude": 24.396308,
        "maxlatitude": 49.384358,
        "minlongitude": -125.0,
        "maxlongitude": -66.93457,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["features"]

# Resolve coordinates to a US state
def get_state_from_coords(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True, timeout=10)
        address = location.raw.get("address", {})
        state = address.get("state")
        return state
    except:
        return None

# Aggregate earthquakes by state
def analyze_by_state(quakes):
    state_data = defaultdict(list)
    for quake in quakes:
        coords = quake["geometry"]["coordinates"]
        lon, lat = coords[0], coords[1]
        mag = quake["properties"]["mag"] or 0
        state = get_state_from_coords(lat, lon)
        if state and state not in EXCLUDED_STATES:
            state_data[state].append(mag)

    analysis = []
    for state, mags in state_data.items():
        count = len(mags)
        avg_mag = sum(mags) / count if count else 0
        risk = count * avg_mag  # simple weighted risk
        analysis.append({"state": state, "count": count, "avg_mag": avg_mag, "risk_score": risk})

    return pd.DataFrame(analysis).sort_values("risk_score", ascending=False)

# Analyze specific addresses
def analyze_client_locations(locations, state_df):
    results = []
    for loc in locations:
        location = geolocator.geocode(loc["address"])
        state = get_state_from_coords(location.latitude, location.longitude) if location else "Unknown"
        row = state_df[state_df['state'] == state]
        risk = row["risk_score"].values[0] if not row.empty else "Unknown"
        results.append({**loc, "state": state, "risk_score": risk})
    return pd.DataFrame(results)

if __name__ == "__main__":
    print("Fetching earthquake data...")
    quakes = fetch_earthquake_data()
    print("Analyzing state-level risk...")
    state_df = analyze_by_state(quakes)
    print(state_df)

    print("Analyzing client locations...")
    client_locs = [
        {"name": "West Anchorage High School", "address": "1700 Hillcrest Dr, Anchorage, AK 99517"},
        {"name": "City Hall", "address": "1 Dr Carlton B Goodlett Pl, San Francisco, CA 94102"},
        {"name": "Los Angeles Memorial Coliseum", "address": "3911 S Figueroa St, Los Angeles, CA 90037"},
        {"name": "Harrah's Reno (Former)", "address": "219 N Center St, Reno, NV 89501"},
        {"name": "Benson Polytechnic High School", "address": "546 NE 12th Ave, Portland, OR 97232"},
        {"name": "Salt Lake Temple", "address": "50 N Temple, Salt Lake City, UT 84150"},
        {"name": "Challis High School", "address": "1 Schoolhouse Rd, Challis, ID 83226"},
    ]

    results_df = analyze_client_locations(client_locs, state_df)
    print(results_df)
