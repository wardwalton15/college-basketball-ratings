"""
Data fetching module for College Basketball Ratings
Fetches data from CollegeBasketballData.com API using direct HTTP requests
"""

import os
import time
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

# API Base URL
CBBD_API_BASE = "https://api.collegebasketballdata.com"


class CBBDataFetcher:
    """Handles fetching data from CBBD API"""

    def __init__(self, api_key: str = None):
        """
        Initialize the data fetcher

        Args:
            api_key: CBBD API key (Bearer token)
        """
        self.api_key = api_key or os.getenv('CBBD_API_KEY')
        if not self.api_key:
            raise ValueError("CBBD_API_KEY not found in environment variables")

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_request(self, endpoint: str, params: dict = None, retries: int = 3) -> Optional[List[Dict]]:
        """
        Make an API request with retry logic

        Args:
            endpoint: API endpoint path
            params: Query parameters
            retries: Number of retry attempts

        Returns:
            JSON response as list of dictionaries
        """
        url = f"{CBBD_API_BASE}{endpoint}"

        for attempt in range(retries):
            try:
                response = self.session.get(url, params=params, timeout=60)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.JSONDecodeError as e:
                print(f"Attempt {attempt + 1}/{retries} failed: {e}")
                print(f"Response status: {response.status_code}")
                print(f"Response content (first 500 chars): {response.text[:500]}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1}/{retries} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise

    def fetch_adjusted_efficiency(self, season: int = 2025) -> List[Dict]:
        """
        Fetch opponent-adjusted efficiency ratings (KenPom-style)
        This is the primary data source for our ratings

        Args:
            season: Season year (e.g., 2025)

        Returns:
            List of adjusted efficiency dictionaries
        """
        print(f"Fetching adjusted efficiency ratings for {season}...")

        try:
            response = self._make_request(
                '/ratings/efficiency',
                params={'season': season}
            )
            print(f"Fetched {len(response) if response else 0} efficiency ratings")
            return response or []
        except Exception as e:
            print(f"Error fetching adjusted efficiency: {e}")
            raise

    def fetch_team_info(self, season: int = 2025) -> List[Dict]:
        """
        Fetch team information including colors and logos

        Args:
            season: Season year

        Returns:
            List of team info dictionaries
        """
        print(f"Fetching team info...")

        try:
            response = self._make_request('/teams')
            print(f"Fetched {len(response) if response else 0} teams info")
            return response or []
        except Exception as e:
            print(f"Error fetching team info: {e}")
            return []

    def fetch_four_factors(self, season: int = 2025) -> List[Dict]:
        """
        Fetch four factors stats directly if available

        Args:
            season: Season year

        Returns:
            List of four factors dictionaries
        """
        print(f"Fetching four factors for {season}...")

        try:
            response = self._make_request(
                '/stats/fourfactors',
                params={'season': season}
            )
            print(f"Fetched {len(response) if response else 0} four factors records")
            return response or []
        except Exception as e:
            print(f"Note: Four factors endpoint not available, using efficiency data")
            return []

    def fetch_all_data(self, season: int = 2025) -> Dict[str, List[Dict]]:
        """
        Fetch all required data for the application

        Args:
            season: Season year

        Returns:
            Dictionary with efficiency, team_info, and four_factors keys
        """
        print(f"\n{'='*50}")
        print(f"Fetching all data for {season} season...")
        print(f"{'='*50}\n")

        efficiency = self.fetch_adjusted_efficiency(season)
        team_info = self.fetch_team_info(season)
        four_factors = self.fetch_four_factors(season)

        return {
            'efficiency': efficiency,
            'team_info': team_info,
            'four_factors': four_factors
        }

    def process_team_data(self, data: Dict[str, List[Dict]], season: int = 2025) -> List[Dict]:
        """
        Process and combine all fetched data into unified team records

        Args:
            data: Dictionary containing efficiency, team_info, four_factors
            season: Season year

        Returns:
            List of processed team dictionaries ready for rating calculation
        """
        efficiency_data = data.get('efficiency', [])
        team_info_data = data.get('team_info', [])
        four_factors_data = data.get('four_factors', [])

        # Create lookup dictionaries
        team_info_map = {}
        for team in team_info_data:
            team_name = team.get('team') or team.get('school')
            if team_name:
                team_info_map[team_name] = team

        four_factors_map = {}
        for ff in four_factors_data:
            team_name = ff.get('team')
            if team_name:
                four_factors_map[team_name] = ff

        processed_teams = []

        for eff in efficiency_data:
            team_name = eff.get('team')
            if not team_name:
                continue

            # Get team info for colors/logo
            info = team_info_map.get(team_name, {})

            # Get four factors if available
            ff = four_factors_map.get(team_name, {})

            # Build unified team record
            # The efficiency endpoint provides adjusted offensive/defensive efficiency
            # We'll use these directly or derive four factors from them
            team_record = {
                'team': team_name,
                'season': season,
                'conference': eff.get('conference'),

                # Adjusted efficiency data
                'adj_offensive_efficiency': eff.get('offense') or eff.get('adjOffense') or eff.get('adjustedOffense'),
                'adj_defensive_efficiency': eff.get('defense') or eff.get('adjDefense') or eff.get('adjustedDefense'),
                'tempo': eff.get('tempo') or eff.get('adjustedTempo'),

                # Four factors - try from four_factors endpoint first, then efficiency
                'off_efg_pct': ff.get('offEfgPct') or ff.get('off_efg_pct') or eff.get('offEfgPct') or eff.get('offensiveEfgPct'),
                'off_orb_pct': ff.get('offOrbPct') or ff.get('off_orb_pct') or eff.get('offOrbPct') or eff.get('offensiveOrbPct'),
                'off_tov_pct': ff.get('offTovPct') or ff.get('off_tov_pct') or eff.get('offTovPct') or eff.get('offensiveTovPct'),
                'off_ftr': ff.get('offFtr') or ff.get('off_ftr') or eff.get('offFtr') or eff.get('offensiveFtr'),

                'def_efg_pct': ff.get('defEfgPct') or ff.get('def_efg_pct') or eff.get('defEfgPct') or eff.get('defensiveEfgPct'),
                'def_orb_pct': ff.get('defOrbPct') or ff.get('def_orb_pct') or eff.get('defOrbPct') or eff.get('defensiveOrbPct'),
                'def_tov_pct': ff.get('defTovPct') or ff.get('def_tov_pct') or eff.get('defTovPct') or eff.get('defensiveTovPct'),
                'def_ftr': ff.get('defFtr') or ff.get('def_ftr') or eff.get('defFtr') or eff.get('defensiveFtr'),

                # Team branding
                'color': info.get('color') or info.get('primaryColor'),
                'alt_color': info.get('altColor') or info.get('secondaryColor') or info.get('alt_color'),
                'logo': info.get('logo') or info.get('logos', [None])[0] if isinstance(info.get('logos'), list) else info.get('logo'),
            }

            processed_teams.append(team_record)

        print(f"\nProcessed {len(processed_teams)} teams")
        return processed_teams


def validate_team_data(team: Dict) -> bool:
    """
    Validate team data for completeness and correctness

    Args:
        team: Team data dictionary

    Returns:
        True if valid, False otherwise
    """
    # At minimum, we need team name and some efficiency data
    if not team.get('team'):
        return False

    # Check if we have at least offensive and defensive efficiency
    has_efficiency = (
        team.get('adj_offensive_efficiency') is not None or
        team.get('off_efg_pct') is not None
    )

    return has_efficiency


if __name__ == "__main__":
    # Test the fetcher
    print("Testing CBBD API Data Fetcher...")
    print("-" * 50)

    try:
        fetcher = CBBDataFetcher()

        # Fetch all data for current season
        # Note: Use 2025 for 2024-25 season, or check what's available
        data = fetcher.fetch_all_data(2025)

        # Process the data
        teams = fetcher.process_team_data(data, 2025)

        if teams:
            print(f"\n{'='*50}")
            print(f"Successfully processed {len(teams)} teams")
            print(f"{'='*50}")

            # Show sample team data
            sample = teams[0]
            print(f"\nSample team data ({sample['team']}):")
            for key, value in sample.items():
                print(f"  {key}: {value}")

            # Find Syracuse specifically
            syracuse = next((t for t in teams if 'Syracuse' in t.get('team', '')), None)
            if syracuse:
                print(f"\n{'='*50}")
                print("Syracuse Data:")
                print(f"{'='*50}")
                for key, value in syracuse.items():
                    print(f"  {key}: {value}")
            else:
                print("\nSyracuse not found in data")

            # Count valid teams
            valid_count = sum(1 for t in teams if validate_team_data(t))
            print(f"\nValid teams: {valid_count}/{len(teams)}")

        else:
            print("No teams data received")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
