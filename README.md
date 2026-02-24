# 🌍 Climate Clock Dashboard

A real-time Python CLI dashboard that fetches and displays live climate data from the [Climate Clock API](https://climateclock.world), including the carbon deadline countdown, renewable energy percentage, conservation metrics, and a live climate news feed.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Why the Original Code Broke](#why-the-original-code-broke)
- [What Was Changed and Fixed](#what-was-changed-and-fixed)
- [Optimizations](#optimizations)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)

---

## Overview

This project was originally built in **2022** as a terminal-based climate data viewer. It pulls live data from the [Climate Clock REST API](https://api.climateclock.world/v1/clock) and displays:

- ⏳ Countdown to irreversible 1.5°C global warming
- ⚡ Real-time percentage of global energy from renewables
- 🌱 Percentage of Earth's land & waters currently protected (30x30 Initiative)
- 🏔️ Land protected by indigenous peoples
- 📰 10 latest positive climate news headlines

---

## Why the Original Code Broke

When the project was first written, it relied on specific module names returned by the Climate Clock API. By 2024–2025, the API had been updated and several of those modules were **renamed, removed, or restructured**, causing the code to crash with a `KeyError`.

### Original modules the code expected:
```
carbon_deadline_1
renewables_1
green_climate_fund_1   ← ❌ No longer exists
indigenous_land_1
newsfeed_1
```

### What the API actually returns now:
```
carbon_deadline_1
renewables_1
regen_agriculture
indigenous_land_1
women_in_parliaments
actnow
end_subsidies
initiative_30x30       ← ✅ Replacement for green_climate_fund_1
loss_damage_g7_debt
loss_damage_g20_debt
ff_divestment_stand_dot_earth
_youth_anxiety
newsfeed_1
```

The `green_climate_fund_1` module was removed entirely from the API. Any attempt to access it by name caused:

```
Error: 'green_climate_fund_1'
```

Additionally, running the script on **Windows** caused a second crash:

```
Error: 'charmap' codec can't encode character '\U0001f30d' in position 2: character maps to <undefined>
```

This happened because Windows defaults to `cp1252` (charmap) encoding for terminal output, which does not support Unicode emoji characters used in the display output.

---

## What Was Changed and Fixed

### 1. Replaced deprecated API module (`climate_clock_info_retrieve.py`)

The call to `green_climate_fund_1` was replaced with `initiative_30x30`, which is the API's current equivalent — a metric tracking the 30x30 initiative to protect 30% of Earth's land and waters by 2030.

```python
# Before (broken)
green_climate_fund_1 = parsed["data"]["modules"]["green_climate_fund_1"]

# After (fixed)
initiative_30x30 = parsed["data"]["modules"]["initiative_30x30"]
```

The return dictionary still uses the key `"green_climate_fund_1"` internally so that `info_format_and_show.py` required minimal changes.

### 2. Rewrote the display formatter (`info_format_and_show.py`)

The original formatter used list index access (e.g., `module[0]`, `module[1]`) to extract fields, which broke because the new API response schema uses named keys instead of positional arrays in some modules. The formatter was rewritten to use **named key access** throughout, making it resilient to future API changes.

```python
# Before (fragile)
label = module[0]
value = module[1]

# After (robust)
label = list_info["renewables_1"]["labels"][0]
value = list_info["renewables_1"]["initial"]
```

### 3. Fixed Windows UTF-8 encoding issue (`run.py`)

Added `sys.stdout.reconfigure(encoding='utf-8')` at the top of `run.py` to force Python to output UTF-8 regardless of the system's default encoding. This resolves the charmap crash on Windows without removing the emoji characters from the display.

```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

---

## Optimizations

### Dynamic metric calculation
The renewable energy percentage is not a static value from the API — it is **calculated in real time** using the API's `rate`, `initial`, and `timestamp` fields:

```python
t = (now - RENEWABLES_1["timestamp"]).total_seconds()
percent = RENEWABLES_1["rate"] * t + RENEWABLES_1["initial"]
```

This means every time you run the tool, you get the most precise current estimate, not a cached number.

### Resilient data parsing
Instead of accessing list indices directly (fragile), all fields are now accessed by name. Labels, units, and values are pulled from their named keys, so if the API adds or reorders fields, the code won't silently produce wrong output or crash with an index error.

### Clean structured output
The terminal display was reformatted to use a consistent, readable layout with clear section dividers, making it easy to scan all 5 metrics and 10 news headlines at a glance.

---

## How to Run

### Prerequisites

- Python 3.8+
- `requests` and `python-dateutil` libraries

### Install dependencies

```bash
pip install requests python-dateutil
```

### Run the dashboard

```bash
cd climate_clock_wttr
python run.py
```

### Output

```
================================================================================
  🌍 CLIMATE CLOCK  |  Tue 24 Feb 2026
================================================================================
  ⏳ Time left to limit global warming to 1.5°C
     3 YRS  148 DAYS  07:22:45
--------------------------------------------------------------------------------
  ⚡ World's energy from renewables: 12.3041%
--------------------------------------------------------------------------------
  🌱 Earth's land & waters protected: 17.6%
--------------------------------------------------------------------------------
  🏔️  Land protected by indigenous people: 43.5 Million sq. km
--------------------------------------------------------------------------------
  📰 Climate News:
     1. Nobel laureate invents machine that harvests water from dry air
     2. Cities across the world are banning fossil fuel adverts
     ...
================================================================================
```

---

## Project Structure

```
climate_clock_wttr/
│
├── run.py                          # Entry point
└── build/
    ├── climate_clock_info_retrieve.py   # API client — fetches and returns data
    └── info_format_and_show.py          # Formatter — calculates and displays output
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `requests` | HTTP calls to the Climate Clock API |
| `python-dateutil` | Precise relativedelta calculations for the countdown timer |
| `json` | Parsing the API's JSON response |
| `datetime` | Timestamp handling and real-time calculations |
| `sys` | UTF-8 stdout reconfiguration for Windows compatibility |

---

## Data Sources

All climate data is sourced from the [Climate Clock API](https://api.climateclock.world/v1/clock), maintained by the [Climate Clock](https://climateclock.world) project. Data is updated daily.
