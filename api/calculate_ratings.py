"""
Rating calculation module for College Basketball Ratings
Implements the Four Factors methodology with opponent adjustments
"""

from typing import Dict, List, Tuple


class RatingCalculator:
    """Calculates team ratings based on Four Factors"""

    # Component weights
    OFFENSIVE_WEIGHT = 0.52
    DEFENSIVE_WEIGHT = 0.48

    # Four Factors weights
    EFG_WEIGHT = 0.40
    ORB_WEIGHT = 0.20
    TOV_WEIGHT = 0.25
    FTR_WEIGHT = 0.15

    # Scaling factor to get ratings in 0-100 range
    # This may need adjustment based on actual data distribution
    SCALING_FACTOR = 1.0

    def __init__(self, scaling_factor: float = None):
        """
        Initialize the rating calculator

        Args:
            scaling_factor: Optional custom scaling factor
        """
        if scaling_factor is not None:
            self.SCALING_FACTOR = scaling_factor

    def calculate_offensive_rating(self, team: Dict) -> float:
        """
        Calculate offensive rating from Four Factors or adjusted efficiency

        If Four Factors are available, uses:
        Offensive Rating = (
            adj_off_efg_pct × 0.40 +
            adj_off_orb_pct × 0.20 +
            (100 - adj_off_tov_pct) × 0.25 +
            adj_off_ftr × 0.15
        ) × scaling_factor

        If only efficiency data is available, uses adjusted offensive efficiency directly

        Args:
            team: Team data dictionary with adjusted stats

        Returns:
            Offensive rating (float)
        """
        off_efg = team.get('off_efg_pct') or 0
        off_orb = team.get('off_orb_pct') or 0
        off_tov = team.get('off_tov_pct') or 0
        off_ftr = team.get('off_ftr') or 0

        # Check if we have Four Factors data
        has_four_factors = off_efg > 0 or off_orb > 0

        if has_four_factors:
            # Use Four Factors formula
            rating = (
                off_efg * self.EFG_WEIGHT +
                off_orb * self.ORB_WEIGHT +
                (100 - off_tov) * self.TOV_WEIGHT +  # Lower TO% is better
                off_ftr * self.FTR_WEIGHT
            ) * self.SCALING_FACTOR
        else:
            # Fall back to adjusted efficiency
            # Typical adjusted offensive efficiency is around 100-120 points per 100 possessions
            # Scale to roughly 0-100 range
            adj_off = team.get('adj_offensive_efficiency') or 0
            rating = (adj_off - 85) * 2  # Scale 85-135 range to 0-100

        return round(max(0, min(100, rating)), 2)

    def calculate_defensive_rating(self, team: Dict) -> float:
        """
        Calculate defensive rating from Four Factors or adjusted efficiency

        If Four Factors are available, uses:
        Defensive Rating = (
            (100 - adj_def_efg_pct) × 0.40 +
            (100 - adj_def_orb_pct) × 0.20 +
            adj_def_tov_pct × 0.25 +
            (100 - adj_def_ftr) × 0.15
        ) × scaling_factor

        If only efficiency data is available, uses adjusted defensive efficiency directly

        Args:
            team: Team data dictionary with adjusted stats

        Returns:
            Defensive rating (float)
        """
        def_efg = team.get('def_efg_pct') or 0
        def_orb = team.get('def_orb_pct') or 0
        def_tov = team.get('def_tov_pct') or 0
        def_ftr = team.get('def_ftr') or 0

        # Check if we have Four Factors data
        has_four_factors = def_efg > 0 or def_orb > 0

        if has_four_factors:
            # Use Four Factors formula
            rating = (
                (100 - def_efg) * self.EFG_WEIGHT +      # Lower allowed eFG% is better
                (100 - def_orb) * self.ORB_WEIGHT +      # Limiting opponent ORB is better
                def_tov * self.TOV_WEIGHT +              # Forcing TOs is better
                (100 - def_ftr) * self.FTR_WEIGHT        # Limiting FTs is better
            ) * self.SCALING_FACTOR
        else:
            # Fall back to adjusted efficiency
            # Typical adjusted defensive efficiency is around 85-110 points per 100 possessions
            # Lower is better, so we invert the scale
            adj_def = team.get('adj_defensive_efficiency') or 100
            rating = (130 - adj_def) * 2  # Scale so 85 -> 90, 110 -> 40

        return round(max(0, min(100, rating)), 2)

    def calculate_overall_rating(self, offensive_rating: float, defensive_rating: float) -> float:
        """
        Calculate overall rating from offensive and defensive ratings

        Formula:
        Overall Rating = (Offensive Rating × 0.52) + (Defensive Rating × 0.48)

        Args:
            offensive_rating: Team's offensive rating
            defensive_rating: Team's defensive rating

        Returns:
            Overall rating (float)
        """
        overall = (
            offensive_rating * self.OFFENSIVE_WEIGHT +
            defensive_rating * self.DEFENSIVE_WEIGHT
        )
        return round(overall, 2)

    def calculate_all_ratings(self, team: Dict) -> Dict:
        """
        Calculate all ratings for a team

        Args:
            team: Team data dictionary

        Returns:
            Dictionary with offensive_rating, defensive_rating, and overall_rating
        """
        off_rating = self.calculate_offensive_rating(team)
        def_rating = self.calculate_defensive_rating(team)
        overall = self.calculate_overall_rating(off_rating, def_rating)

        return {
            'offensive_rating': off_rating,
            'defensive_rating': def_rating,
            'overall_rating': overall
        }

    def process_teams(self, teams: List[Dict]) -> List[Dict]:
        """
        Calculate ratings for all teams and add rankings

        Args:
            teams: List of team data dictionaries

        Returns:
            List of teams with ratings and ranks added
        """
        # Calculate ratings for all teams
        for team in teams:
            ratings = self.calculate_all_ratings(team)
            team.update(ratings)

        # Sort by overall rating for ranking
        teams_sorted = sorted(teams, key=lambda x: x['overall_rating'], reverse=True)

        # Add overall rank
        for i, team in enumerate(teams_sorted):
            team['overall_rank'] = i + 1

        # Calculate and add component ranks
        self._add_component_ranks(teams_sorted)

        return teams_sorted

    def _add_component_ranks(self, teams: List[Dict]) -> None:
        """
        Add ranking for each component (offensive, defensive, individual factors)

        Args:
            teams: List of team dictionaries (modified in place)
        """
        # Offensive rating rank
        teams_by_off = sorted(teams, key=lambda x: x['offensive_rating'], reverse=True)
        for i, team in enumerate(teams_by_off):
            team['offensive_rank'] = i + 1

        # Defensive rating rank
        teams_by_def = sorted(teams, key=lambda x: x['defensive_rating'], reverse=True)
        for i, team in enumerate(teams_by_def):
            team['defensive_rank'] = i + 1

        # Individual factor ranks
        self._rank_by_metric(teams, 'off_efg_pct', 'off_efg_rank', reverse=True)
        self._rank_by_metric(teams, 'off_orb_pct', 'off_orb_rank', reverse=True)
        self._rank_by_metric(teams, 'off_tov_pct', 'off_tov_rank', reverse=False)  # Lower is better
        self._rank_by_metric(teams, 'off_ftr', 'off_ftr_rank', reverse=True)

        self._rank_by_metric(teams, 'def_efg_pct', 'def_efg_rank', reverse=False)  # Lower is better
        self._rank_by_metric(teams, 'def_orb_pct', 'def_orb_rank', reverse=False)  # Lower is better
        self._rank_by_metric(teams, 'def_tov_pct', 'def_tov_rank', reverse=True)
        self._rank_by_metric(teams, 'def_ftr', 'def_ftr_rank', reverse=False)  # Lower is better

        self._rank_by_metric(teams, 'tempo', 'tempo_rank', reverse=True)

    def _rank_by_metric(self, teams: List[Dict], metric: str, rank_field: str, reverse: bool) -> None:
        """
        Rank teams by a specific metric

        Args:
            teams: List of teams
            metric: Metric field name
            rank_field: Field name for rank
            reverse: True if higher is better, False if lower is better
        """
        teams_sorted = sorted(teams, key=lambda x: x.get(metric, 0), reverse=reverse)
        for i, team in enumerate(teams_sorted):
            # Find the team in original list and update rank
            for orig_team in teams:
                if orig_team['team'] == team['team']:
                    orig_team[rank_field] = i + 1
                    break

    def determine_scaling_factor(self, teams: List[Dict]) -> float:
        """
        Determine optimal scaling factor to get ratings in 0-100 range

        Args:
            teams: List of team data dictionaries

        Returns:
            Recommended scaling factor
        """
        # Calculate unscaled ratings
        temp_calculator = RatingCalculator(scaling_factor=1.0)
        unscaled_ratings = [temp_calculator.calculate_all_ratings(t)['overall_rating'] for t in teams]

        # Find max unscaled rating
        max_rating = max(unscaled_ratings)

        # Calculate scaling factor to map max to ~95-100 range
        target_max = 97.5
        scaling_factor = target_max / max_rating

        return round(scaling_factor, 3)


if __name__ == "__main__":
    # Test with sample Syracuse data
    test_team = {
        'team': 'Syracuse',
        'season': 2026,
        'conference': 'ACC',
        'off_efg_pct': 52.3,
        'off_orb_pct': 28.5,
        'off_tov_pct': 16.2,
        'off_ftr': 35.1,
        'def_efg_pct': 48.7,
        'def_orb_pct': 25.3,
        'def_tov_pct': 18.9,
        'def_ftr': 31.2,
        'tempo': 68.5
    }

    calculator = RatingCalculator()
    ratings = calculator.calculate_all_ratings(test_team)

    print("Syracuse Ratings:")
    print(f"  Offensive: {ratings['offensive_rating']}")
    print(f"  Defensive: {ratings['defensive_rating']}")
    print(f"  Overall: {ratings['overall_rating']}")
