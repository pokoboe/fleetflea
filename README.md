# README.md

# 🌿 GreenFleet

**A MyGeotab Add-In that turns idle waste and EV readiness into actionable decisions.**

Built for the Geotab Vibe Coding Contest 2026 by FleetFlea.

---

## What It Does

GreenFleet surfaces two insights that are technically available in MyGeotab but
require significant manual work to extract:

| Question | What GreenFleet IQ shows |
|---|---|
| Which vehicles waste the most fuel idling? | Top 10 ranked by idle %, with litres and CO₂ per vehicle |
| Which vehicles are ready to go electric? | EV Score 0–100 based on actual trip patterns |
| Where would they charge? | Map of real stop locations + nearby EV chargers |

---

## Features

### 📊 Tab 1 — Idle & EV Analysis

**3 KPI Cards**
- 🌍 **CO₂ Emitted** — fleet total for the selected period, with passenger-car equivalent
- ⏱️ **Idle Fuel Wasted** — litres burned engine-on / vehicle stationary
- ⚡ **EV-Ready Vehicles** — count scoring ≥ 72/100

**Top 10 Idle Offenders**
- Sorted by idle % of engine-on time (not raw hours)
- Progress bar per vehicle, color-coded: green / orange / red
- Per-vehicle idle fuel (L) and CO₂ (kg)
- Click 📊 → modal chart: 3 metrics on one timeline with dual Y-axis

**Top EV Transition Candidates**
- EV Score algorithm: range fit (42 pts) + idle behavior (30 pts) + trip frequency (22 pts) + base (10 pts)
- Verdicts: Strong EV fit / Good candidate / Possible / Low priority
- Adjustable date range: Last day / Last 5 days / Last 30 days

### ⚡ Tab 2 — EV Charging Readiness Map

- 🟡 **Charging stops** — locations where a vehicle stopped 30–90 min
- 🟣 **Night stops** — vehicles parked evening → morning (overnight charging opportunity)
- 🟢 **EV Chargers** — real stations from OpenChargeMap within 50 miles of fleet territory
- Toggle each layer independently
- Click any marker for vehicle name, stop duration, and timestamp

---

## Data Sources

| Data | Source | Method |
|---|---|---|
| Trip distances, durations | MyGeotab `Trip` API | Direct |
| Stop coordinates | MyGeotab `LogRecord` API | Last GPS point before trip end |
| Vehicle fuel type | `Device.engineType` | Diesel vs gasoline CO₂ factor |
| EV charger locations | OpenChargeMap API | JSONP (no API key required) |

**Fuel estimates:** Uses `trip.fuelUsed` when available (engine data); falls back to
10 L/100 km for gasoline / adjusted for diesel.

---

## Installation

### 1. Add to MyGeotab

Administration → System Settings → Add-Ins → Add → paste:

```json
{
  "name": "GreenFleet",
  "supportEmail": "https://github.com/pokoboe/fleetflea",
  "version": "2.0.26",
  "items": [{
    "url": "https://pokoboe.github.io/fleetflea/greenfleet.html",
    "path": "ActivityLink",
    "menuName": { "en": "GreenFleet" }
  }]
}
```

Enable **"Allow unverified Add-Ins"** if prompted.

### 2. Repository structure

```
fleetflea/
├── greenfleet.html     ← Add-In (single file, no build step)
├── greenfleet.css      ← Zenith-compatible styles
└── lib/
    ├── chart.umd.min.js   ← Chart.js 4.4.1 (bundled, no CDN)
    ├── leaflet.js         ← Leaflet 1.9 (bundled, no CDN)
    └── leaflet.css
```

Libraries are bundled locally to avoid corporate CSP and tracking-prevention blocks.

---

## Technical Notes

**Distance units:** The MyGeotab JS API returns `trip.distance` in **kilometers**
(not meters as stated in the Python SDK docs). Auto-detected at runtime by checking
if max raw value > 5000.

**Duration format:** `idlingDuration` / `drivingDuration` can arrive as
`{ totalSeconds }`, `{ ticks }`, or `"HH:MM:SS"` string depending on API version.
All three formats are handled by `parseDur()`.

**Stop coordinates:** Trip API does not include stop/start GPS coordinates.
GreenFleet IQ queries `LogRecord` for the last GPS point within 4 minutes before
each trip end — this gives the actual stop location.

**EV Charger API:** Uses JSONP (dynamic `<script>` injection) instead of `fetch()`
to bypass Content Security Policy restrictions inside the MyGeotab iframe.

---

## License

MIT — free to use, fork, and build upon.

Built with ❤️ and Claude by FleetFlea · February 2026