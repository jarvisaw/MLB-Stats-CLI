import requests
from requests.exceptions import RequestException

def get_roster(team_id):
    """
    Fetches the 40-man roster for a specific team ID from the MLB API.

    Args:
        team_id (str or int): The unique ID for the MLB team (e.g., 113 for Reds).

    Returns:
        dict: A dictionary containing the roster data if the API call is successful.
        None: If a network error or HTTP error occurs.
    """
    # Specific API endpoint for a team's roster
    url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster"
    
    try:
        # Make the API call
        response = requests.get(url)
        
        # This checks for bad responses (like 404, 500)
        response.raise_for_status() 
        
        # Parse the JSON response and return it
        return response.json()

    except RequestException as e:
        # This block catches any network-related/HTTP errors (e.g., no internet)
        print(f"Error fetching roster from API: {e}")
        return None
    
def get_league_leaders(stat_category, season, group="hitting", limit=10):
    """
    Fetches the league leaders for a specific stat category and season.

    Args:
        stat_category (str): The API-ready stat category (e.g., "homeRuns").
        season (int or str): The 4-digit season year.
        group (str, optional): "hitting" or "pitching". Defaults to "hitting".
        limit (int, optional): The number of players to return. Defaults to 10.

    Returns:
        dict: A dictionary containing the leaders data if the API call is successful.
        None: If an error occurs.
    """
    # Define the base URL and the query parameters
    url = "https://statsapi.mlb.com/api/v1/stats/leaders"
    
    params = {
        "leaderCategories": stat_category,
        "season": season,
        "statGroup": group,
        "limit": limit,
        "sportId": 1  # MLB sport ID
    }

    # Make the API call
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()

    except RequestException as e:
        print(f"Error fetching leaders from API: {e}")
        return None
    
def search_for_player(full_name):
    """
    Searches for an active MLB player by their full name.

    Args:
        full_name (str): The full name of the player to search for (e.g., "Shohei Ohtani").

    Returns:
        str: The player's unique ID if found.
        None: If an error occurs or no active player is found.
    """
    url = "https://statsapi.mlb.com/api/v1/people/search"
    
    params = {
        "names": full_name.lower(), # The API is case-insensitive, but this is good practice
        "active": "true",
        "sportId": 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # 'people' is a list. We check if it's not empty.
        if data.get("people"):
            # Return the ID of the first player found
            return data["people"][0]["id"]
        else:
            # No active player found with that name
            return None

    except RequestException as e:
        print(f"Error searching for player: {e}")
        return None

def get_player_stats(player_id, season):
    """
    Fetches a player's season stats for both hitting and pitching.

    Args:
        player_id (str or int): The player's unique ID.
        season (int or str): The 4-digit season year.

    Returns:
        dict: A dictionary containing the player's stat data.
        None: If an error occurs.
    """
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats"
    
    params = {
        "stats": "season",
        "group": "hitting,pitching", # Request both stat groups
        "season": season,
        "sportId": 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except RequestException as e:
        print(f"Error fetching player stats: {e}")
        return None