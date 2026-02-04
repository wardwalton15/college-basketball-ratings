"""
Rating calculation module for College Basketball Ratings.

Rating System: Adjusted Efficiency Margin with Consistency Component

Overall Rating = 90% Adjusted Efficiency Margin + 10% Consistency Component

Adjusted Efficiency Margin (adj_net):
  - Points per 100 possessions differential (offense - defense)
  - Opponent-adjusted for strength of schedule

Consistency Component:
  - Rewards lower variance in tempo and offensive efficiency across games
  - Uses Dean Oliver possession formula: 0.96 * [(FGA) + (TO) + 0.44*(FTA) - (ORB)]
  - Lower variance = higher consistency score

The Four Factors composites are still calculated for display/analysis purposes.
"""

from typing import Dict, List


class RatingCalculator:
    """Calculates team ratings from adjusted efficiency and game consistency."""

    # Main rating weights
    ADJ_EFFICIENCY_WEIGHT = 0.90  # Adjusted efficiency margin
    CONSISTENCY_WEIGHT = 0.10     # Consistency component

    # Adjusted efficiency margin normalization
    ADJ_NET_FLOOR = -30.0    # Maps to 0 (worst)
    ADJ_NET_CEILING = 35.0   # Maps to 100 (best)

    # Consistency component normalization (standard deviations)
    # Lower variance = better, so we invert these
    TEMPO_VAR_FLOOR = 0.0      # Perfect consistency (maps to 100)
    TEMPO_VAR_CEILING = 12.0   # High variance (maps to 0)
    OFF_EFF_VAR_FLOOR = 0.0    # Perfect consistency (maps to 100)
    OFF_EFF_VAR_CEILING = 20.0 # High variance (maps to 0)

    # Consistency sub-weights (how to blend tempo vs offensive efficiency variance)
    TEMPO_CONSISTENCY_WEIGHT = 0.40
    OFF_EFF_CONSISTENCY_WEIGHT = 0.60

    # Four Factors weights for composite display (Dean Oliver's values)
    OFF_WEIGHT = 0.52
    DEF_WEIGHT = 0.48
    EFG_WEIGHT = 0.40
    TO_WEIGHT = 0.25
    ORB_WEIGHT = 0.20
    FTR_WEIGHT = 0.15

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
        """Blend offensive and defensive composites (for display purposes)."""
        return round(
            off_composite * self.OFF_WEIGHT + def_composite * self.DEF_WEIGHT,
            1
        )

    def calculate_consistency_score(self, tempo_var: float, off_eff_var: float) -> float:
        """
        Calculate consistency score from game-to-game variance.

        Lower variance = higher score (rewards consistent performance).
        Blends tempo consistency (40%) and offensive efficiency consistency (60%).
        """
        # Invert: lower variance maps to higher score
        tempo_score = _normalize(
            self.TEMPO_VAR_CEILING - tempo_var,
            0,
            self.TEMPO_VAR_CEILING - self.TEMPO_VAR_FLOOR
        )
        off_eff_score = _normalize(
            self.OFF_EFF_VAR_CEILING - off_eff_var,
            0,
            self.OFF_EFF_VAR_CEILING - self.OFF_EFF_VAR_FLOOR
        )

        return round(
            tempo_score * self.TEMPO_CONSISTENCY_WEIGHT +
            off_eff_score * self.OFF_EFF_CONSISTENCY_WEIGHT,
            1
        )

    def calculate_overall_rating(self, adj_net: float, consistency_score: float = None) -> float:
        """
        Calculate overall rating: 90% adjusted efficiency margin + 10% consistency.

        adj_net: Adjusted net rating (points per 100 possessions differential)
        consistency_score: Score from 0-100 based on game-to-game variance
        """
        # Normalize adj_net to 0-100 scale
        adj_net_normalized = _normalize(adj_net, self.ADJ_NET_FLOOR, self.ADJ_NET_CEILING)

        if consistency_score is not None:
            return round(
                adj_net_normalized * self.ADJ_EFFICIENCY_WEIGHT +
                consistency_score * self.CONSISTENCY_WEIGHT,
                1
            )
        else:
            # Fallback to just adj_net if no consistency data
            return round(adj_net_normalized, 1)

    def process_teams(self, teams: List[Dict]) -> List[Dict]:
        """
        Calculate all ratings and rankings for every team.

        Overall Rating = 90% Adjusted Efficiency Margin + 10% Consistency Component

        Adds to each team dict:
          - overall_composite: Main rating (adj efficiency + consistency)
          - consistency_score: Rewards lower variance in tempo and offensive efficiency
          - off_composite, def_composite: Four-factors sub-ratings (for display)
          - raw_composite: Unadjusted four-factors blend (for display)
          - Ranks for all metrics
        """
        # Phase 1: Calculate four-factors composites (for display/analysis)
        for team in teams:
            off_comp = self.calculate_offensive_composite(team)
            def_comp = self.calculate_defensive_composite(team)

            team['off_composite'] = off_comp
            team['def_composite'] = def_comp

            if off_comp is not None and def_comp is not None:
                team['raw_composite'] = self.calculate_raw_composite(off_comp, def_comp)
            else:
                team['raw_composite'] = None

        # Phase 2: Calculate consistency score from game-level variance
        for team in teams:
            tempo_var = team.get('tempo_variance')
            off_eff_var = team.get('off_eff_variance')

            if tempo_var is not None and off_eff_var is not None:
                team['consistency_score'] = self.calculate_consistency_score(tempo_var, off_eff_var)
            else:
                team['consistency_score'] = None

        # Phase 3: Calculate overall rating (90% adj efficiency + 10% consistency)
        for team in teams:
            adj_net = team.get('adj_net')
            consistency = team.get('consistency_score')

            if adj_net is not None:
                team['overall_composite'] = self.calculate_overall_rating(adj_net, consistency)
            else:
                team['overall_composite'] = None

        # Rank by overall and component ratings
        _add_rank(teams, 'overall_composite', 'overall_rank', reverse=True)
        _add_rank(teams, 'consistency_score', 'consistency_rank', reverse=True)
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

        # Rank variance metrics (lower is better for these)
        _add_rank(teams, 'tempo_variance', 'tempo_var_rank', reverse=False)
        _add_rank(teams, 'off_eff_variance', 'off_eff_var_rank', reverse=False)

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
    # Quick test with sample data - includes variance for consistency component
    test_teams = [
        {
            'team': 'Duke', 'conference': 'ACC',
            'adj_off': 130.3, 'adj_def': 90.5, 'adj_net': 39.8,
            'off_efg': 57.9, 'off_to_ratio': 0.14, 'off_orb': 27.9, 'off_ftr': 32.9,
            'def_efg': 44.4, 'def_to_ratio': 0.17, 'def_orb': 33.3, 'def_ftr': 25.0,
            'pace': 65.7, 'srs': 22.2,
            'tempo_variance': 3.5, 'off_eff_variance': 8.2,  # Consistent team
        },
        {
            'team': 'Auburn', 'conference': 'SEC',
            'adj_off': 122.3, 'adj_def': 92.8, 'adj_net': 29.5,
            'off_efg': 53.5, 'off_to_ratio': 0.16, 'off_orb': 33.0, 'off_ftr': 37.0,
            'def_efg': 46.0, 'def_to_ratio': 0.20, 'def_orb': 28.0, 'def_ftr': 30.0,
            'pace': 68.0, 'srs': 18.0,
            'tempo_variance': 5.2, 'off_eff_variance': 12.5,  # More variable
        },
        {
            'team': 'UC San Diego', 'conference': 'Big West',
            'adj_off': 115.1, 'adj_def': 96.3, 'adj_net': 18.8,
            'off_efg': 55.5, 'off_to_ratio': 0.14, 'off_orb': 26.8, 'off_ftr': 32.2,
            'def_efg': 47.0, 'def_to_ratio': 0.25, 'def_orb': 27.6, 'def_ftr': 29.0,
            'pace': 63.1, 'srs': 12.4,
            'tempo_variance': 2.8, 'off_eff_variance': 6.5,  # Very consistent
        },
        {
            'team': 'South Alabama', 'conference': 'Sun Belt',
            'adj_off': 108.0, 'adj_def': 104.4, 'adj_net': 3.6,
            'off_efg': 53.7, 'off_to_ratio': 0.15, 'off_orb': 33.3, 'off_ftr': 39.1,
            'def_efg': 47.3, 'def_to_ratio': 0.22, 'def_orb': 27.2, 'def_ftr': 26.0,
            'pace': 64.5, 'srs': 3.8,
            'tempo_variance': 7.1, 'off_eff_variance': 15.3,  # Inconsistent team
        },
    ]

    calc = RatingCalculator()
    rated = calc.process_teams(test_teams)

    print("=" * 70)
    print("NEW RATING SYSTEM: 90% Adj Efficiency Margin + 10% Consistency")
    print("=" * 70)

    for team in rated:
        print(f"\n{team['team']} ({team['conference']}):")
        print(f"  OVERALL RATING:   {team['overall_composite']} (rank #{team.get('overall_rank')})")
        print(f"  ├─ Adj Net:       {team['adj_net']:+.1f} (90% weight)")
        print(f"  └─ Consistency:   {team['consistency_score']} (10% weight, rank #{team.get('consistency_rank')})")
        print(f"      ├─ Tempo σ:   {team['tempo_variance']} (rank #{team.get('tempo_var_rank')})")
        print(f"      └─ Off Eff σ: {team['off_eff_variance']} (rank #{team.get('off_eff_var_rank')})")
        print(f"  Four Factors:     Off {team['off_composite']} | Def {team['def_composite']} | Raw {team['raw_composite']}")
