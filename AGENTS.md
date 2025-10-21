# Project Name: MLB Stats CLI

## Overview

This project is a Python-based command-line interface (CLI) application for my IS4010 midterm. The tool allows users to quickly fetch and display real-time baseball statistics from the MLB. It interacts with a public, no-auth API and is built with `argparse` for commands, `requests` for API calls, and `pytest` for testing.

## API Integration

-   **API:** MLB Data API
-   **Documentation:** `https://appac.github.io/mlb-data-api-docs/`
-   **Authentication:** None required.
-   **Data Format:** JSON

## CLI Commands (3)

The application will support three main commands:

1.  **`stats`**
    -   **Usage:** `python -m src.main stats "[player_name]" --season [YYYY]`
    -   **Purpose:** Searches for a specific player and displays their key hitting or pitching stats for a given season. The `--season` argument is optional and defaults to the current year.
    -   **API Endpoint(s):** Will likely involve searching for a player ID (`/player_search`) and then fetching stats with that ID (`/stats`).

2.  **`roster`**
    -   **Usage:** `python -m src.main roster [team_code]`
    -   **Purpose:** Fetches and displays the current 40-man roster for a specific team (e.g., `CIN`, `NYY`, `LAD`). Output should include jersey number, full name, and position.
    -   **API Endpoint(s):** `/roster/{team_id}`

3.  **`leaders`**
    -   **Usage:** `python -m src.main leaders [stat_category]`
    -   **Purpose:** Fetches and displays the top 10 league leaders for a specific statistical category (e.g., `HR`, `AVG`, `RBI`, `SO`).
    -   **API Endpoint(s):** `/stats/leaders`

## Technical Stack

-   **Language:** Python 3.10+
-   **CLI Parsing:** `argparse` library
-   **API Requests:** `requests` library
-   **Testing:** `pytest` and `unittest.mock`

## Code Organization

The project follows the structure specified in the midterm rubric:

-   `src/main.py`: Main entry point. Handles all `argparse` setup and CLI logic.
-   `src/api.py`: Contains all functions that interact with the MLB API. These functions will handle making `requests.get()` calls, parsing JSON, and returning data.
-   `src/models.py`: (Optional) May be used for data classes if the API responses are complex.
-   `tests/test_main.py`: `pytest` tests for the `argparse` CLI commands.
-   `tests/test_api.py`: `pytest` tests for the API functions, using `@patch` to mock all external `requests` calls.

## Development Standards

-   All code will follow **PEP 8** style guidelines.
-   All functions and classes will have clear **docstrings**.
-   API calls in `src/api.py` will include **error handling** (e.g., `try...except` blocks) for network errors or bad responses (e.g., 404).
-   All tests must **mock API calls** using `unittest.mock`. No real network requests will be made during testing.
-   The final CI/CD pipeline in GitHub Actions must pass.