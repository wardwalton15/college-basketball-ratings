"""
Data fetching module for College Basketball Ratings
Fetches data from CollegeBasketballData.com API (api.collegebasketballdata.com)
"""

import os
import time
import statistics
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

CBBD_API_BASE = "https://api.collegebasketballdata.com"


class CBBDataFetcher:
    """Handles fetching data from CBBD API"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('CBBD_API_KEY')
        if not self.api_key:
            raise ValueError("CBBD_API_KEY not found in environment variables")

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        })

    def _make_request(self, endpoint: str, params: dict = None, retries: int = 3) -> Optional[list | dict]:
        """Make an API request with retry logic and exponential backoff."""
        url = f"{CBBD_API_BASE}{endpoint}"

        for attempt in range(retries):
            try:
                response = self.session.get(url, params=params, timeout=60)
                response.raise_for_status()

                # The API serves Swagger UI HTML for invalid endpoints
                content_type = response.headers.get('content-type', '')
                if 'text/html' in content_type:
                    raise ValueError(f"Endpoint {endpoint} returned HTML (likely invalid endpoint)")

                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"  Attempt {attempt + 1}/{retries} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise

    def fetch_adjusted_ratings(self, season: int = 2026) -> List[Dict]:
        """
        Fetch opponent-adjusted efficiency ratings for all D-I teams.

        Endpoint: /ratings/adjusted
        Returns ~364 D-I teams with:
          - offensiveRating, defensiveRating, netRating
          - rankings.offense, rankings.defense, rankings.net
        """
        print(f"Fetching adjusted ratings for {season}...")
        data = self._make_request('/ratings/adjusted', params={'season': season})
        print(f"  Got {len(data)} teams")
        return data or []

    def fetch_team_stats(self, season: int = 2026) -> List[Dict]:
        """
        Fetch team season stats including four factors.

        Endpoint: /stats/team/season
        Returns ~700 teams (includes non-D-I) with:
          - teamStats.fourFactors (eFG%, TO ratio, ORB%, FTR)
          - opponentStats.fourFactors (same for opponents)
          - pace, wins, losses, full box score aggregates
        """
        print(f"Fetching team season stats for {season}...")
        data = self._make_request('/stats/team/season', params={'season': season})
        print(f"  Got {len(data)} team stat records")
        return data or []

    def fetch_srs_ratings(self, season: int = 2026) -> List[Dict]:
        """
        Fetch Simple Rating System (SRS) ratings.

        Endpoint: /ratings/srs
        Returns ~364 D-I teams with a single SRS rating value.
        """
        print(f"Fetching SRS ratings for {season}...")
        data = self._make_request('/ratings/srs', params={'season': season})
        print(f"  Got {len(data)} SRS ratings")
        return data or []

    def fetch_team_info(self) -> List[Dict]:
        """
        Fetch team branding info (colors, venues, etc).

        Endpoint: /teams
        Returns all teams with:
          - school, mascot, abbreviation, primaryColor, secondaryColor
          - currentVenue, currentCity, currentState, conference
        """
        print("Fetching team info...")
        data = self._make_request('/teams')
        print(f"  Got {len(data)} teams")
        return data or []

    def fetch_game_stats(self, season: int = 2026, team: str = None) -> List[Dict]:
        """
        Fetch game-by-game stats for teams.

        Endpoint: /games/teams
        Returns individual game records with:
          - pace, teamStats.possessions, teamStats.rating (offensive efficiency)
          - Full box score stats for possession calculation
        """
        params = {'season': season}
        if team:
            params['team'] = team
        data = self._make_request('/games/teams', params=params, retries=3)
        return data or []

    def fetch_all_game_stats(self, season: int = 2026, teams: List[str] = None) -> Dict[str, List[Dict]]:
        """
        Fetch game-by-game stats for all teams.

        Returns a dict mapping team name -> list of game records.
        """
        print(f"Fetching game-by-game stats for {season}...")
        all_games = self.fetch_game_stats(season)
        print(f"  Got {len(all_games)} game records total")

        # Group by team
        games_by_team = {}
        for game in all_games:
            team_name = game.get('team')
            if team_name:
                if team_name not in games_by_team:
                    games_by_team[team_name] = []
                games_by_team[team_name].append(game)

        print(f"  Grouped into {len(games_by_team)} teams")
        return games_by_team

    def fetch_all(self, season: int = 2026) -> Dict[str, List[Dict]]:
        """Fetch all data sources needed for team ratings."""
        print(f"\n{'='*50}")
        print(f"Fetching all data for {season} season")
        print(f"{'='*50}\n")

        return {
            'adjusted': self.fetch_adjusted_ratings(season),
            'team_stats': self.fetch_team_stats(season),
            'srs': self.fetch_srs_ratings(season),
            'team_info': self.fetch_team_info(),
            'game_stats': self.fetch_all_game_stats(season),
        }

    def build_team_records(self, data: Dict[str, List[Dict]], season: int = 2026) -> List[Dict]:
        """
        Merge all data sources into unified team records.

        Uses adjusted ratings as the canonical list of D-I teams (~364),
        then joins team stats, SRS, branding info, and game-level variance by team name.
        """
        adjusted = data.get('adjusted', [])
        team_stats = data.get('team_stats', [])
        srs = data.get('srs', [])
        team_info = data.get('team_info', [])
        game_stats = data.get('game_stats', {})  # Dict[team_name, List[game]]

        # Build lookup maps
        stats_map = {t['team']: t for t in team_stats if t.get('team')}
        srs_map = {t['team']: t for t in srs if t.get('team')}
        # team_info uses 'school' not 'team'
        info_map = {t['school']: t for t in team_info if t.get('school')}

        teams = []
        for adj in adjusted:
            name = adj.get('team')
            if not name:
                continue

            stats = stats_map.get(name, {})
            srs_data = srs_map.get(name, {})
            info = info_map.get(name, {})

            off_ff = (stats.get('teamStats') or {}).get('fourFactors') or {}
            def_ff = (stats.get('opponentStats') or {}).get('fourFactors') or {}

            # Calculate game-level variance for consistency component
            team_games = game_stats.get(name, [])
            tempo_variance, off_eff_variance = self._calculate_game_variance(team_games)

            teams.append({
                'team': name,
                'season': season,
                'conference': adj.get('conference'),

                # Adjusted efficiency (points per 100 possessions)
                'adj_off': adj.get('offensiveRating'),
                'adj_def': adj.get('defensiveRating'),
                'adj_net': adj.get('netRating'),

                # API-provided rankings
                'rank_off': (adj.get('rankings') or {}).get('offense'),
                'rank_def': (adj.get('rankings') or {}).get('defense'),
                'rank_net': (adj.get('rankings') or {}).get('net'),

                # Record
                'wins': stats.get('wins'),
                'losses': stats.get('losses'),
                'games': stats.get('games'),

                # Pace
                'pace': stats.get('pace'),

                # Offensive four factors
                'off_efg': off_ff.get('effectiveFieldGoalPct'),
                'off_to_ratio': off_ff.get('turnoverRatio'),
                'off_orb': off_ff.get('offensiveReboundPct'),
                'off_ftr': off_ff.get('freeThrowRate'),

                # Defensive four factors (opponent stats)
                'def_efg': def_ff.get('effectiveFieldGoalPct'),
                'def_to_ratio': def_ff.get('turnoverRatio'),
                'def_orb': def_ff.get('offensiveReboundPct'),
                'def_ftr': def_ff.get('freeThrowRate'),

                # SRS
                'srs': srs_data.get('rating'),

                # Game-level variance (for consistency component)
                'tempo_variance': tempo_variance,
                'off_eff_variance': off_eff_variance,

                # Branding
                'primary_color': info.get('primaryColor'),
                'secondary_color': info.get('secondaryColor'),
                'logo': info.get('logo'),
                'abbreviation': info.get('abbreviation'),
            })

        print(f"\nBuilt {len(teams)} team records")

        # Report teams missing stats
        missing_stats = [t['team'] for t in teams if t['off_efg'] is None]
        if missing_stats:
            print(f"  {len(missing_stats)} teams missing four factors data")

        # Report teams with variance data
        with_variance = sum(1 for t in teams if t['tempo_variance'] is not None)
        print(f"  {with_variance} teams with game-level variance data")

        return teams

    def _calculate_game_variance(self, games: List[Dict]) -> tuple:
        """
        Calculate variance in tempo and offensive efficiency across games.

        Uses Dean Oliver's possession formula:
        Possessions = 0.96 * [(FGA) + (TO) + 0.44*(FTA) - (ORB)]

        Returns (tempo_variance, off_eff_variance) or (None, None) if insufficient data.
        """
        if len(games) < 3:  # Need at least 3 games for meaningful variance
            return None, None

        tempos = []
        off_effs = []

        for game in games:
            team_stats = game.get('teamStats') or {}

            # Get box score components for possession calculation
            fg_attempted = (team_stats.get('fieldGoals') or {}).get('attempted')
            turnovers = (team_stats.get('turnovers') or {}).get('total', 0)
            ft_attempted = (team_stats.get('freeThrows') or {}).get('attempted')
            off_rebounds = (team_stats.get('rebounds') or {}).get('offensive')
            points = (team_stats.get('points') or {}).get('total')
            game_minutes = game.get('gameMinutes', 40)

            # Skip games with missing data
            if any(v is None for v in [fg_attempted, ft_attempted, off_rebounds, points]):
                continue

            # Dean Oliver possession formula
            possessions = 0.96 * (fg_attempted + turnovers + 0.44 * ft_attempted - off_rebounds)

            if possessions > 0:
                # Tempo: possessions per 40 minutes
                tempo = possessions * (40 / game_minutes) if game_minutes > 0 else possessions
                tempos.append(tempo)

                # Offensive efficiency: points per 100 possessions
                off_eff = (points / possessions) * 100
                off_effs.append(off_eff)

        # Need at least 3 valid games
        if len(tempos) < 3:
            return None, None

        try:
            tempo_var = statistics.stdev(tempos)
            off_eff_var = statistics.stdev(off_effs)
            return round(tempo_var, 2), round(off_eff_var, 2)
        except statistics.StatisticsError:
            return None, None


if __name__ == "__main__":
    print("Testing CBBD API Data Fetcher")
    print("-" * 50)

    fetcher = CBBDataFetcher()
    data = fetcher.fetch_all(2026)
    teams = fetcher.build_team_records(data, 2026)

    if not teams:
        print("ERROR: No team data received")
        exit(1)

    # Show a sample
    sample = next((t for t in teams if t['team'] == 'Duke'), teams[0])
    print(f"\nSample: {sample['team']}")
    for key, value in sample.items():
        print(f"  {key}: {value}")

    # Summary
    with_stats = sum(1 for t in teams if t['off_efg'] is not None)
    print(f"\nTotal teams: {len(teams)}")
    print(f"With four factors: {with_stats}")
    print(f"With SRS: {sum(1 for t in teams if t['srs'] is not None)}")
