# MLB Stats CLI <img src="https://upload.wikimedia.org/wikipedia/commons/a/a6/Major_League_Baseball_logo.svg" alt="MLB Logo" width="100" height="" style="display:inline-block; vertical-align:middle; margin-left:8px;">

![Run Python Tests](https://github.com/jarvisaw/MLB-Stats-CLI/actions/workflows/tests.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A Python-based command-line tool designed to fetch real-time Major League Baseball (MLB) statistics directly from your terminal. Easily look up team rosters, league leaders, and individual player stats.

This project was developed as the midterm requirement for IS4010 at the University of Cincinnati.

---

## Features

* **View Team Rosters:** Get the full 40-man roster for any of the 30 MLB teams.
* **Get League Leaders:** See the top 10 league leaders for major hitting and pitching categories (e.g., `HR`, `AVG`, `RBI`, `SO`, `ERA`).
* **Fetch Player Stats:** Look up the season statistics for any active player, with an option to specify the season year.

---

## Installation ⚙️

To get this project running on your local machine, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/jarvisaw/MLB-Stats-CLI.git
    cd mlb-stats-cli
    ```

2.  **Set Up a Virtual Environment** (Highly Recommended):
    * *On Windows:*
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * *On macOS/Linux:*
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage Examples 🚀

Execute the application from your terminal within the project's root directory using the `python -m src.main` command, followed by the specific command and arguments.

### Command: `roster`

Displays the 40-man roster for a given team code.

**Format:**
```bash
python -m src.main roster [TEAM_CODE]
```

**Example:**
```bash
$ python -m src.main roster CIN

Fetching roster for CIN (ID: 113)...
--- 40-Man Roster ---
  #44  - Elly De La Cruz         (Shortstop)
  #33  - Christian Encarnacion-Strand (First Base)
  #... (and so on)
```

### Command: `leaders`

Shows the top 10 league leaders for a specific statistical category.

**Format:**
```bash
python -m src.main leaders [STAT_CODE]
```

**Example (Home Runs):**
```bash
$ python -m src.main leaders HR

Fetching hitting leaders for HR in 2025...
--- Top 10 hitting leaders for HR (2025) ---
  1. Cal Raleigh         (Seattle Mariners) - 60
  2. Kyle Schwarber      (Philadelphia Phillies) - 56
  #... (and so on)
```

**Example (ERA):**
```bash
$ python -m src.main leaders ERA

Fetching pitching leaders for ERA in 2025...
--- Top 10 pitching leaders for ERA (2025) ---
  1. Paul Skenes         (Pittsburgh Pirates) - 1.97
  #... (and so on)
```

### Command: `stats`

Retrieves the season stats for an individual player. The `--season` flag is optional; if left empty, it defaults to the current year.

**Format:**
```bash
python -m src.main stats "[PLAYER_NAME]" --season [YEAR]
```

**Example:**
```bash
$ python -m src.main stats "Shohei Ohtani" --season 2024

Searching for active player: 'Shohei Ohtani'...
Found player ID: 660271. Fetching stats for 2024...
--- Stats for Shohei Ohtani (2024) ---
--- hitting ---
  AVG: .302 | HR: 44 | RBI: 112
  Games: 154 | Hits: 178 | SB: 41
```

## API Information🔌

This project utilizes the free and public **MLB Data API** hosted at `statsapi.mlb.com`. No authentication keys are required for access.

* **API Documentation Reference:** [Unofficial MLB Data API Docs](https://appac.github.io/mlb-data-api-docs/)

---

## Technologies Used 🛠️

* **Python 3.10+**
* **`argparse`:** For command-line argument parsing.
* **`requests`:** For making HTTP requests to the MLB API.
* **`pytest`:** For running automated tests.
* **`unittest.mock`:** For mocking API calls during testing.
* **GitHub Actions:** For Continuous Integration (CI).

---

## Running Tests ✅

The project includes a comprehensive test suite using `pytest`. All external API calls are mocked using `unittest.mock` to ensure tests are fast, reliable, and can run offline.

To execute the tests locally, navigate to the project root directory and run:

```bash
pytest
```

**Expected Output:**
```bash
$ pytest
================ test session starts ================
platform win32 -- Python 3.10.x, pytest-x.y.z, pluggy-a.b.c
rootdir: /path/to/mlb-stats-cli
collected 11 items

tests/test_api.py ......                      [ 54%]
tests/test_main.py .....                      [100%]

=============== 11 passed in x.yzs ================
```

---