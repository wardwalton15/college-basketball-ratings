"""
Rating calculation module for College Basketball Ratings.

Builds a composite team rating from the Four Factors methodology,
then compares against the API's opponent-adjusted efficiency ratings.

Four Factors (Dean Oliver):
  Offense: eFG%, Turnover Rate, ORB%, Free Throw Rate
  Defense: Same factors for opponent (lower eFG%, higher TO forced, etc.)

The API also provides opponent-adjusted efficiency ratings (KenPom-style)
which we store alongside our composite for comparison.
"""

from typing import Dict, List


class RatingCalculator:
    """Calculates team ratings from Four Factors and adjusted efficiency data."""

    # Offensive vs defensive weight in overall composite
    OFF_WEIGHT = 0.52
    DEF_WEIGHT = 0.48

    # Four Factors weights (Dean Oliver's approximate values)
    EFG_WEIGHT = 0.40   # Shooting efficiency
    TO_WEIGHT = 0.25    # Turnover rate
    ORB_WEIGHT = 0.20   # Offensive rebounding
    FTR_WEIGHT = 0.15   # Free throw rate

    # Strength-of-schedule adjustment: blend raw composite with adj_net
    RAW_COMPOSITE_WEIGHT = 0.33
    ADJ_NET_WEIGHT = 0.40
    ADJ_NET_FLOOR = -30.0   # adj_net normalization floor (maps to 0)
    ADJ_NET_CEILING = 35.0  # adj_net normalization ceiling (maps to 100)

    def calculate_offensive_composite(self, team: Dict) -> float | None:
        """
        Score offensive four factors on a 0-100 scale.

        Components (higher is better for offense):
          - eFG%: typically 45-58% -> scale directly
          - TO ratio: typically 0.13-0.25 -> lower is better, invert
          - ORB%: typically 22-38% -> scale directly
          - FTR: typically 20-45% -> scale directly
        """
        efg = team.get('off_efg')
        to_ratio = team.get('off_to_ratio')
        orb = team.get('off_orb')
        ftr = team.get('off_ftr')

        if efg is None:
            return None

        # Normalize each factor to ~0-100 range
        efg_score = _normalize(efg, 42, 60)
        # Lower turnover ratio is better: 0.25 -> bad (0), 0.12 -> good (100)
        to_score = _normalize(0.25 - (to_ratio or 0.19), 0, 0.13)
        orb_score = _normalize(orb or 28, 20, 40)
        ftr_score = _normalize(ftr or 28, 15, 50)

        composite = (
            efg_score * self.EFG_WEIGHT +
            to_score * self.TO_WEIGHT +
            orb_score * self.ORB_WEIGHT +
            ftr_score * self.FTR_WEIGHT
        )
        return round(composite, 1)

    def calculate_defensive_composite(self, team: Dict) -> float | None:
        """
        Score defensive four factors on a 0-100 scale.

        Components (lower opponent values = better defense):
          - Opponent eFG%: lower is better -> invert
          - Opponent TO ratio: higher is better (we force turnovers)
          - Opponent ORB%: lower is better -> invert
          - Opponent FTR: lower is better -> invert
        """
        efg = team.get('def_efg')
        to_ratio = team.get('def_to_ratio')
        orb = team.get('def_orb')
        ftr = team.get('def_ftr')

        if efg is None:
            return None

        # Invert opponent eFG%: 42% allowed -> great (100), 58% allowed -> bad (0)
        efg_score = _normalize(60 - (efg or 50), 0, 18)
        # Higher forced TO ratio is better
        to_score = _normalize(to_ratio or 0.19, 0.12, 0.25)
        # Lower opponent ORB% is better
        orb_score = _normalize(40 - (orb or 30), 0, 20)
        # Lower opponent FTR is better
        ftr_score = _normalize(50 - (ftr or 32), 0, 35)

        composite = (
            efg_score * self.EFG_WEIGHT +
            to_score * self.TO_WEIGHT +
            orb_score * self.ORB_WEIGHT +
            ftr_score * self.FTR_WEIGHT
        )
        return round(composite, 1)

    def calculate_raw_composite(self, off_composite: float, def_composite: float) -> float:
        """Blend offensive and defensive composites (unadjusted for SOS)."""
        return round(
            off_composite * self.OFF_WEIGHT + def_composite * self.DEF_WEIGHT,
            1
        )

    def calculate_adjusted_composite(self, raw_composite: float, adj_net: float) -> float:
        """
        Blend raw four-factors composite with opponent-adjusted net rating.

        This corrects for strength of schedule: teams with strong raw stats
        against weak opponents get pulled toward their adj_net reality.
        """
        normalized_adj_net = _normalize(adj_net, self.ADJ_NET_FLOOR, self.ADJ_NET_CEILING)
        return round(
            self.RAW_COMPOSITE_WEIGHT * raw_composite +
            self.ADJ_NET_WEIGHT * normalized_adj_net,
            1
        )

    def process_teams(self, teams: List[Dict]) -> List[Dict]:
        """
        Calculate all ratings and rankings for every team.

        Adds to each team dict:
          - off_composite, def_composite (four-factors sub-ratings)
          - raw_composite (unadjusted four-factors blend)
          - overall_composite (SOS-adjusted via adj_net blend)
          - Ranks for composites and individual four factors
          - The API's adjusted ratings are kept as-is (adj_off, adj_def, adj_net)
        """
        # Phase 1: Calculate raw four-factors composites
        for team in teams:
            off_comp = self.calculate_offensive_composite(team)
            def_comp = self.calculate_defensive_composite(team)

            team['off_composite'] = off_comp
            team['def_composite'] = def_comp

            if off_comp is not None and def_comp is not None:
                team['raw_composite'] = self.calculate_raw_composite(off_comp, def_comp)
            else:
                team['raw_composite'] = None

        # Phase 2: Apply SOS adjustment by blending with adj_net
        for team in teams:
            raw = team.get('raw_composite')
            adj_net = team.get('adj_net')

            if raw is not None and adj_net is not None:
                team['overall_composite'] = self.calculate_adjusted_composite(raw, adj_net)
            else:
                team['overall_composite'] = raw  # Fallback to raw if adj_net missing

        # Rank by adjusted and raw composites
        _add_rank(teams, 'overall_composite', 'overall_rank', reverse=True)
        _add_rank(teams, 'raw_composite', 'raw_composite_rank', reverse=True)
        _add_rank(teams, 'off_composite', 'off_composite_rank', reverse=True)
        _add_rank(teams, 'def_composite', 'def_composite_rank', reverse=True)

        # Rank individual four factors
        _add_rank(teams, 'off_efg', 'off_efg_rank', reverse=True)
        _add_rank(teams, 'off_to_ratio', 'off_to_rank', reverse=False)    # Lower is better
        _add_rank(teams, 'off_orb', 'off_orb_rank', reverse=True)
        _add_rank(teams, 'off_ftr', 'off_ftr_rank', reverse=True)

        _add_rank(teams, 'def_efg', 'def_efg_rank', reverse=False)       # Lower allowed is better
        _add_rank(teams, 'def_to_ratio', 'def_to_rank', reverse=True)    # Forcing more TOs is better
        _add_rank(teams, 'def_orb', 'def_orb_rank', reverse=False)       # Lower allowed is better
        _add_rank(teams, 'def_ftr', 'def_ftr_rank', reverse=False)       # Lower allowed is better

        _add_rank(teams, 'pace', 'pace_rank', reverse=True)
        _add_rank(teams, 'srs', 'srs_rank', reverse=True)

        # Sort by overall composite descending
        teams.sort(key=lambda t: t.get('overall_composite') or -999, reverse=True)

        return teams


def _normalize(value: float, low: float, high: float) -> float:
    """Normalize a value to 0-100 scale given expected range."""
    if high == low:
        return 50.0
    score = (value - low) / (high - low) * 100
    return max(0.0, min(100.0, score))


def _add_rank(teams: List[Dict], field: str, rank_field: str, reverse: bool) -> None:
    """Add ranking for a metric. Teams with None values get no rank."""
    ranked = [t for t in teams if t.get(field) is not None]
    ranked.sort(key=lambda t: t[field], reverse=reverse)
    for i, team in enumerate(ranked):
        team[rank_field] = i + 1


if __name__ == "__main__":
    # Quick test with sample data - includes a mid-major to verify SOS adjustment
    test_teams = [
        {
            'team': 'Duke', 'conference': 'ACC',
            'adj_off': 130.3, 'adj_def': 90.5, 'adj_net': 39.8,
            'off_efg': 57.9, 'off_to_ratio': 0.14, 'off_orb': 27.9, 'off_ftr': 32.9,
            'def_efg': 44.4, 'def_to_ratio': 0.17, 'def_orb': 33.3, 'def_ftr': 25.0,
            'pace': 65.7, 'srs': 22.2,
        },
        {
            'team': 'Auburn', 'conference': 'SEC',
            'adj_off': 122.3, 'adj_def': 92.8, 'adj_net': 29.5,
            'off_efg': 53.5, 'off_to_ratio': 0.16, 'off_orb': 33.0, 'off_ftr': 37.0,
            'def_efg': 46.0, 'def_to_ratio': 0.20, 'def_orb': 28.0, 'def_ftr': 30.0,
            'pace': 68.0, 'srs': 18.0,
        },
        {
            'team': 'UC San Diego', 'conference': 'Big West',
            'adj_off': 115.1, 'adj_def': 96.3, 'adj_net': 18.8,
            'off_efg': 55.5, 'off_to_ratio': 0.14, 'off_orb': 26.8, 'off_ftr': 32.2,
            'def_efg': 47.0, 'def_to_ratio': 0.25, 'def_orb': 27.6, 'def_ftr': 29.0,
            'pace': 63.1, 'srs': 12.4,
        },
        {
            'team': 'South Alabama', 'conference': 'Sun Belt',
            'adj_off': 108.0, 'adj_def': 104.4, 'adj_net': 3.6,
            'off_efg': 53.7, 'off_to_ratio': 0.15, 'off_orb': 33.3, 'off_ftr': 39.1,
            'def_efg': 47.3, 'def_to_ratio': 0.22, 'def_orb': 27.2, 'def_ftr': 26.0,
            'pace': 64.5, 'srs': 3.8,
        },
    ]

    calc = RatingCalculator()
    rated = calc.process_teams(test_teams)

    for team in rated:
        print(f"\n{team['team']} ({team['conference']}):")
        print(f"  Off composite:    {team['off_composite']} (rank {team.get('off_composite_rank')})")
        print(f"  Def composite:    {team['def_composite']} (rank {team.get('def_composite_rank')})")
        print(f"  Raw composite:    {team['raw_composite']} (rank {team.get('raw_composite_rank')}) [unadjusted]")
        print(f"  Overall adjusted: {team['overall_composite']} (rank {team.get('overall_rank')}) [SOS-adjusted]")
        print(f"  Adj Net Rating:   {team['adj_net']} (from API)")
