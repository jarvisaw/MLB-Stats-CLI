import argparse
import datetime
from src.api import get_roster, get_league_leaders, search_for_player, get_player_stats

# A complete dictionary mapping all 30 MLB team codes to their API team IDs.
TEAM_MAP = {
    "LAA": 108, # Los Angeles Angels
    "ARI": 109, # Arizona Diamondbacks
    "BAL": 110, # Baltimore Orioles
    "BOS": 111, # Boston Red Sox
    "CHC": 112, # Chicago Cubs
    "CIN": 113, # Cincinnati Reds
    "CLE": 114, # Cleveland Guardians
    "COL": 115, # Colorado Rockies
    "DET": 116, # Detroit Tigers
    "HOU": 117, # Houston Astros
    "KC": 118,  # Kansas City Royals
    "LAD": 119, # Los Angeles Dodgers
    "WSH": 120, # Washington Nationals
    "NYM": 121, # New York Mets
    "OAK": 133, # Oakland Athletics
    "PIT": 134, # Pittsburgh Pirates
    "SD": 135,  # San Diego Padres
    "SEA": 136, # Seattle Mariners
    "SF": 137,  # San Francisco Giants
    "STL": 138, # St. Louis Cardinals
    "TB": 139,  # Tampa Bay Rays
    "TEX": 140, # Texas Rangers
    "TOR": 141, # Toronto Blue Jays
    "MIN": 142, # Minnesota Twins
    "PHI": 143, # Philadelphia Phillies
    "ATL": 144, # Atlanta Braves
    "CWS": 145, # Chicago White Sox
    "MIA": 146, # Miami Marlins
    "NYY": 147, # New York Yankees
    "MIL": 158, # Milwaukee Brewers
}

# Map for user-friendly stat codes to the API's required "leaderCategories"
STAT_MAP = {
    "HR": "homeRuns",
    "AVG": "battingAverage",
    "RBI": "runsBattedIn",
    "H": "hits",
    "SB": "stolenBases",
    "SO": "strikeOuts",      # For pitchers
    "ERA": "earnedRunAverage" # For pitchers
}

def main():
    """
    Main function to run the MLB Stats CLI application.
    Parses command-line arguments and calls the appropriate functions.
    """
    # Create the main parser
    parser = argparse.ArgumentParser(description="A CLI tool to fetch MLB stats.")
    
    # Create the sub-parser "controller"
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # Create the parser for the "roster" command
    roster_parser = subparsers.add_parser("roster", help="Get a team's 40-man roster.")
    roster_parser.add_argument(
        "team_code", 
        type=str, 
        help="The team's code (e.g., CIN, NYY, LAD)."
    )

    # Create the parser for the "stats" command (placeholder)
    stats_parser = subparsers.add_parser("stats", help="Get a player's season stats (Not implemented yet).")
    stats_parser.add_argument("player_name", type=str, help="The full name of the player.")
    stats_parser.add_argument("--season", type=int, help="The 4-digit season year (e.g., 2024).")

    # Create the parser for the "leaders" command
    leaders_parser = subparsers.add_parser("leaders", help="Get league leaders for a stat.")
    leaders_parser.add_argument("stat_category", type=str, help="The stat to get leaders for (e.g., HR, AVG, SO).")
    # We can add an optional --season flag here later if we want

    # Parse the arguments from the command line
    args = parser.parse_args()

    # Execute the correct code based on the command
    if args.command == "roster":
        # Look up the team ID from our map
        team_id = TEAM_MAP.get(args.team_code.upper())
        
        if not team_id:
            print(f"Error: Team code '{args.team_code}' not found in our map.")
            print(f"Known codes: {list(TEAM_MAP.keys())}")
            return

        # Call our API function from api.py
        print(f"Fetching roster for {args.team_code.upper()} (ID: {team_id})...")
        roster_data = get_roster(team_id)
        
        if roster_data:
            print("--- 40-Man Roster ---")
            for player in roster_data.get("roster", []):
                print(
                    f"  #{player.get('jerseyNumber', 'N/A'):<3} - "
                    f"{player['person'].get('fullName', 'Unknown Player'):<25} "
                    f"({player['position'].get('name', 'Unknown')})"
                )

    elif args.command == "leaders":
        # Get the current year as a default for the season
        # (We use datetime for this)
        current_year = datetime.datetime.now().year
        season = current_year # (We will add a --season flag later)
        
        # Validate the user's stat code using the STAT_MAP
        stat_code = args.stat_category.upper()
        stat_category = STAT_MAP.get(stat_code)
        
        if not stat_category:
            print(f"Error: Unknown stat category '{stat_code}'")
            print(f"Known codes: {list(STAT_MAP.keys())}")
            return
            
        # Determine if it's a hitting or pitching stat
        stat_group = "pitching" if stat_code in ["SO", "ERA"] else "hitting"

        # Call our API function from api.py
        print(f"Fetching {stat_group} leaders for {stat_code} in {season}...")
        leaders_data = get_league_leaders(stat_category, season, group=stat_group)
        
        if leaders_data:
            leaders_list = leaders_data.get("leagueLeaders", [{}])[0].get("leaders", [])
            
            if not leaders_list:
                print(f"No leaders found for {stat_code} in {season}.")
                return

            print(f"--- Top 10 {stat_group} leaders for {stat_code} ({season}) ---")
            for leader in leaders_list:
                print(
                    f"  {leader.get('rank')}. "
                    f"{leader['person'].get('fullName', 'Unknown'):<25} "
                    f"({leader['team'].get('name', 'N/A')}) - "
                    f"{leader.get('value', 'N/A')}"
                )

    elif args.command == "stats":
        # Determine the season. Use the optional --season flag or default to current year
        current_year = datetime.datetime.now().year
        season = args.season if args.season else current_year
        
        print(f"Searching for active player: '{args.player_name}'...")
        
        # Search for the player ID
        player_id = search_for_player(args.player_name)
        
        if not player_id:
            print(f"Error: Could not find an active player named '{args.player_name}'.")
            return
            
        print(f"Found player ID: {player_id}. Fetching stats for {season}...")
        
        # Get the player's stats using their ID
        stats_data = get_player_stats(player_id, season)
        
        if not stats_data or not stats_data.get("stats"):
            print(f"No stats found for {args.player_name} in {season}.")
            return
            
        # Print the stats
        print(f"--- Stats for {args.player_name} ({season}) ---")
        
        stats_found = False
        for stat_group in stats_data.get("stats", []):
            group_name = stat_group.get("group", {}).get("displayName", "Unknown")
            splits = stat_group.get("splits", [])
            
            # Make sure there is actually stat data in the split
            if splits:
                stats_found = True
                print(f"--- {group_name} ---")
                
                # The actual stats are in splits[0]['stat']
                s = splits[0].get("stat", {})
                
                if group_name == "hitting":
                    print(f"  AVG: {s.get('avg', 'N/A')} | HR: {s.get('homeRuns', 'N/A')} | RBI: {s.get('rbi', 'N/A')}")
                    print(f"  Games: {s.get('gamesPlayed', 'N/A')} | Hits: {s.get('hits', 'N/A')} | SB: {s.get('stolenBases', 'N/A')}")
                elif group_name == "pitching":
                    print(f"  W-L: {s.get('wins', 'N/A')}-{s.get('losses', 'N/A')} | ERA: {s.get('era', 'N/A')} | SO: {s.get('strikeOuts', 'N/A')}")
                    print(f"  Games: {s.get('gamesPitched', 'N/A')} | IP: {s.get('inningsPitched', 'N/A')} | WHIP: {s.get('whip', 'N/A')}")

        if not stats_found:
            print(f"No hitting or pitching stats found for {args.player_name} in {season}.")


if __name__ == "__main__":
    main()