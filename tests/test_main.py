import pytest
from unittest.mock import patch, MagicMock, call
from src.main import main # We import the main function itself

# Helper function to make checking print calls easier
def get_all_print_output(mock_print):
    """Converts all calls to the print mock into a single string."""
    return "\n".join([str(call.args[0]) for call in mock_print.call_args_list])

# The string 'src.api.requests.get' is the full path to the 'get' function
# as it's imported *inside* your src/api.py file. This is crucial.

@patch('src.main.get_player_stats')
@patch('src.main.search_for_player')
@patch('src.main.get_league_leaders')
@patch('src.main.get_roster')
@patch('builtins.print')
def test_roster_command_success(mock_print, mock_get_roster, mock_get_leaders, mock_search, mock_get_stats):
    """
    Tests that the 'roster' command calls 'get_roster' with the correct ID
    and prints the result.
    (NOTE: Removed capsys)
    """
    # 1. Arrange:
    # Set up our test command-line arguments
    test_args = ['main.py', 'roster', 'CIN'] 
    
    # Set up our test API data
    fake_roster = {
        "roster": [
            {"person": {"fullName": "Elly De La Cruz"}, "jerseyNumber": "44", "position": {"name": "Shortstop"}}
        ]
    }
    # Tell the mocked get_roster function to return our test data
    mock_get_roster.return_value = fake_roster

    # Use patch('sys.argv', test_args) to simulate the user's command
    with patch('sys.argv', test_args):
        # 2. Act:
        main() # Run the main function

    # 3. Assert:
    # Check that get_roster was called with 113 (the ID for "CIN")
    mock_get_roster.assert_called_once_with(113) 
    
    # We check the 'mock_print' object instead of 'capsys'
    all_output = get_all_print_output(mock_print)
    
    assert "Elly De La Cruz" in all_output
    assert "#44 " in all_output
    assert "(Shortstop)" in all_output

@patch('src.main.get_roster') # We only need to mock the one function we expect to be called
@patch('builtins.print')
def test_roster_command_invalid_team(mock_print, mock_get_roster):
    """
    Tests that the 'roster' command prints an error for an unknown team code.
    (This test was already passing, no changes needed)
    """
    # 1. Arrange:
    test_args = ['main.py', 'roster', 'INVALIDCODE']
    
    # 2. Act:
    with patch('sys.argv', test_args):
        main()
        
    # 3. Assert:
    # Check that the API function was *never* called
    mock_get_roster.assert_not_called()
    
    # Check that our friendly error message was printed
    assert any("Error: Team code 'INVALIDCODE' not found" in str(c) for c in mock_print.call_args_list)

@patch('src.main.get_league_leaders')
@patch('builtins.print')
def test_leaders_command_success(mock_print, mock_get_leaders):
    """
    Tests that the 'leaders' command calls 'get_league_leaders' with the
    correct translated stat category (e.g., "HR" -> "homeRuns").
    (NOTE: Removed capsys)
    """
    # 1. Arrange:
    test_args = ['main.py', 'leaders', 'HR']
    
    # We need to know the current year, which is 2025
    current_year = 2025 
    
    fake_leaders = {
        "leagueLeaders": [
            {"leaders": [
                {"rank": 1, "person": {"fullName": "Test Hitter"}, "team": {"name": "Test Team"}, "value": "99"}
            ]}
        ]
    }
    mock_get_leaders.return_value = fake_leaders
    
    # 2. Act:
    with patch('sys.argv', test_args):
        main()
        
    # 3. Assert:
    # Check that the function was called with the *translated* API term
    mock_get_leaders.assert_called_once_with("homeRuns", current_year, group="hitting")
    
    all_output = get_all_print_output(mock_print)
    assert "Test Hitter" in all_output
    assert "(Test Team) - 99" in all_output

@patch('src.main.search_for_player')
@patch('builtins.print')
def test_stats_command_player_not_found(mock_print, mock_search_player):
    """
    Tests that the 'stats' command prints an error if the player isn't found.
    (This test was already passing, no changes needed)
    """
    # 1. Arrange:
    test_args = ['main.py', 'stats', 'Unknown Player']
    
    # Simulate search_for_player returning None 
    mock_search_player.return_value = None 
    
    # 2. Act:
    with patch('sys.argv', test_args):
        main()
        
    # 3. Assert:
    mock_search_player.assert_called_once_with('Unknown Player')
    assert any("Error: Could not find an active player" in str(c) for c in mock_print.call_args_list)

@patch('src.main.get_player_stats')
@patch('src.main.search_for_player')
@patch('builtins.print')
def test_stats_command_success(mock_print, mock_search_player, mock_get_stats):
    """
    Tests the full 'stats' command flow, from search to printing stats.
    (NOTE: Removed capsys)
    """
    # 1. Arrange:
    test_args = ['main.py', 'stats', 'Test Player', '--season', '2024']
    
    # Simulate search_for_player returning a test ID
    mock_search_player.return_value = 99999
    
    # Simulate get_player_stats returning test stats
    fake_stats = {
        "stats": [
            {
                "group": {"displayName": "hitting"},
                "splits": [
                    {"stat": {"avg": ".300", "homeRuns": 50, "rbi": 120, "gamesPlayed": 162, "hits": 200, "stolenBases": 30}}
                ]
            }
        ]
    }
    mock_get_stats.return_value = fake_stats

    # 2. Act:
    with patch('sys.argv', test_args):
        main()

    # 3. Assert:
    # Check that our functions were called with the correct arguments
    mock_search_player.assert_called_once_with('Test Player')
    mock_get_stats.assert_called_once_with(99999, 2024) # Correct ID and season
    
    # Check that the stats were printed
    all_output = get_all_print_output(mock_print)
    assert "--- Stats for Test Player (2024) ---" in all_output
    assert "AVG: .300 | HR: 50 | RBI: 120" in all_output
    assert "Games: 162 | Hits: 200 | SB: 30" in all_output