# Earthquake Risk Assessment

This is a standalone Python program that assesses earthquake risk across U.S. states using recent USGS data and scores specific insured locations. It was built for Artificial’s Solutions Engineer technical exercise.

---

## How to Run (Standalone CLI)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the main program
```bash
python earthquake_risk.py
```

This will:
- Fetch USGS earthquake data from the last 7 days
- Analyze frequency and magnitude by state (excluding Hawaii)
- Score client-specific addresses using reverse geolocation

### 3. Offline fallback (if no network)
```bash
python earthquake_risk_final.py
```

---

## Key Files

| File | Purpose |
|------|---------|
| `earthquake_risk.py` | Main standalone CLI program |
| `earthquake_risk_final.py` | Offline version with mock data |
| `mock_quakes.json` | Pre-generated mock USGS data |
| `requirements.txt` | Install dependencies |
| `tests/test_basic.py` | Sample placeholder test |

---

## Optional Enhancement (Not Required)

A Streamlit dashboard was included for client-facing clarity.

Run:
```bash
cd dashboard
streamlit run streamlit_app.py
```

Live version (optional demo):  
🔗 https://earthquake-risk-dashboard-8vxjg8tfi7eblwuqkrarzb.streamlit.app

---

## Notes

- This project was built as a CLI-first solution.
- The dashboard is a bonus layer for visibility, not a replacement.

Prepared by: Andrea  
GitHub: `@at-github-th`
