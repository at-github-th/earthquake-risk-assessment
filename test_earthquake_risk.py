import pytest
from earthquake_risk import fetch_earthquake_data, analyze_by_state

def test_fetch_earthquake_data_returns_list():
    data = fetch_earthquake_data()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "geometry" in data[0]
    assert "properties" in data[0]

def test_analyze_by_state_returns_dataframe():
    data = fetch_earthquake_data()
    df = analyze_by_state(data)
    assert not df.empty
    assert "state" in df.columns
    assert "risk_score" in df.columns
