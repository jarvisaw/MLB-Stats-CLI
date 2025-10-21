import pytest
import requests
from unittest.mock import patch, MagicMock
from src.api import get_roster, get_league_leaders, search_for_player, get_player_stats

# The string 'src.api.requests.get' is the full path to the 'get' function in the 'requests' module
@patch('src.api.requests.get')
def test_get_roster_success(mock_get):
    """
    Tests that get_roster returns correct data on a successful API call.
    """
    # Arrange: Set up our test data and mock response
    fake_json = {
        "roster": [
            {"person": {"fullName": "Test Player 1"}, "jerseyNumber": "10", "position": {"name": "Shortstop"}}
        ]
    }
    
    mock_response = MagicMock()
    mock_response.json.return_value = fake_json
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response # Make requests.get() return our test response
    
    # Call the function we are testing
    team_id = 113
    result = get_roster(team_id)
    
    # Check that the function behaved as expected
    expected_url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster"
    mock_get.assert_called_once_with(expected_url) # Was it called with the right URL?
    assert result == fake_json # Did it return the test data?

@patch('src.api.requests.get')
def test_get_roster_failure(mock_get):
    """
    Tests that get_roster returns None when the API call fails.
    """
    # Configure the mock to simulate an HTTP error
    mock_response = MagicMock()
    # Tell the mock to raise an error when .raise_for_status() is called
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("404 Error")
    mock_get.return_value = mock_response
    
    result = get_roster(113)
    
    assert result is None # The function should catch the error and return None

@patch('src.api.requests.get')
def test_get_league_leaders_success(mock_get):
    """
    Tests that get_league_leaders returns correct data on a successful call.
    """
    fake_json = {
        "leagueLeaders": [
            {"leaders": [{"rank": 1, "person": {"fullName": "Test Leader"}}]}
        ]
    }
    mock_response = MagicMock()
    mock_response.json.return_value = fake_json
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    stat_category = "homeRuns"
    season = 2024
    
    result = get_league_leaders(stat_category, season)
    
    expected_url = "https://statsapi.mlb.com/api/v1/stats/leaders"
    expected_params = {
        "leaderCategories": stat_category,
        "season": season,
        "statGroup": "hitting",
        "limit": 10,
        "sportId": 1
    }
    mock_get.assert_called_once_with(expected_url, params=expected_params)
    assert result == fake_json

@patch('src.api.requests.get')
def test_search_for_player_success(mock_get):
    """
    Tests that search_for_player returns the player ID when a player is found.
    """
    fake_json = {"people": [{"id": 12345, "fullName": "Test Player"}]}
    mock_response = MagicMock()
    mock_response.json.return_value = fake_json
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = search_for_player("Test Player")
    
    assert result == 12345 # Should return the ID

@patch('src.api.requests.get')
def test_search_for_player_not_found(mock_get):
    """
    Tests that search_for_player returns None when no player is found.
    """
    fake_json = {"people": []} # API returns an empty list
    mock_response = MagicMock()
    mock_response.json.return_value = fake_json
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    result = search_for_player("Unknown Player")
    
    assert result is None # Should return None

@patch('src.api.requests.get')
def test_get_player_stats_success(mock_get):
    """
    Tests that get_player_stats returns data on a successful call.
    """
    fake_json = {
        "stats": [
            {"group": "hitting", "splits": [{"stat": {"homeRuns": 50}}]}
        ]
    }
    mock_response = MagicMock()
    mock_response.json.return_value = fake_json
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    player_id = 12345
    season = 2024
    
    result = get_player_stats(player_id, season)
    
    expected_url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats"
    expected_params = {
        "stats": "season",
        "group": "hitting,pitching",
        "season": season,
        "sportId": 1
    }
    mock_get.assert_called_once_with(expected_url, params=expected_params)
    assert result == fake_json