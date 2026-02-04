-- College Basketball Ratings Database Schema
-- To be executed in Supabase SQL Editor

-- Drop existing table if schema has changed
DROP TABLE IF EXISTS team_ratings;

CREATE TABLE team_ratings (
    id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    season INT NOT NULL,
    conference VARCHAR(50),

    -- Record
    wins INT,
    losses INT,
    games INT,

    -- Main rating: 90% Adj Efficiency Margin + 10% Consistency
    overall_composite DECIMAL(5,2),
    overall_rank INT,

    -- Consistency component (rewards lower game-to-game variance)
    consistency_score DECIMAL(5,2),
    consistency_rank INT,
    tempo_variance DECIMAL(5,2),      -- Std dev of possessions per game
    tempo_var_rank INT,
    off_eff_variance DECIMAL(5,2),    -- Std dev of offensive efficiency
    off_eff_var_rank INT,

    -- Four factors composites (for display/analysis)
    raw_composite DECIMAL(5,2),
    raw_composite_rank INT,
    off_composite DECIMAL(5,2),
    off_composite_rank INT,
    def_composite DECIMAL(5,2),
    def_composite_rank INT,

    -- API adjusted efficiency (KenPom-style, pts per 100 possessions)
    adj_off DECIMAL(6,2),
    adj_def DECIMAL(6,2),
    adj_net DECIMAL(6,2),

    -- API rankings
    rank_off INT,   -- API adj offensive rank
    rank_def INT,   -- API adj defensive rank
    rank_net INT,   -- API adj net rank

    -- Offensive four factors (raw season stats)
    off_efg DECIMAL(5,2),         -- Effective FG%
    off_efg_rank INT,
    off_to_ratio DECIMAL(5,3),    -- Turnover ratio
    off_to_rank INT,
    off_orb DECIMAL(5,2),         -- Offensive rebound %
    off_orb_rank INT,
    off_ftr DECIMAL(5,2),         -- Free throw rate
    off_ftr_rank INT,

    -- Defensive four factors (opponent stats)
    def_efg DECIMAL(5,2),
    def_efg_rank INT,
    def_to_ratio DECIMAL(5,3),
    def_to_rank INT,
    def_orb DECIMAL(5,2),
    def_orb_rank INT,
    def_ftr DECIMAL(5,2),
    def_ftr_rank INT,

    -- Other metrics
    pace DECIMAL(5,2),
    pace_rank INT,
    srs DECIMAL(6,2),
    srs_rank INT,

    -- Branding
    primary_color VARCHAR(10),
    secondary_color VARCHAR(10),
    logo_url TEXT,
    abbreviation VARCHAR(10),

    -- Metadata
    last_updated TIMESTAMP DEFAULT NOW(),

    UNIQUE(team_name, season)
);

-- Indexes for sorting and filtering
CREATE INDEX idx_overall_composite ON team_ratings(overall_composite DESC);
CREATE INDEX idx_consistency_score ON team_ratings(consistency_score DESC);
CREATE INDEX idx_raw_composite ON team_ratings(raw_composite DESC);
CREATE INDEX idx_adj_net ON team_ratings(adj_net DESC);
CREATE INDEX idx_team_season ON team_ratings(team_name, season);
CREATE INDEX idx_season ON team_ratings(season);
CREATE INDEX idx_conference ON team_ratings(conference);

-- Comment explaining the rating system
COMMENT ON TABLE team_ratings IS 'Team ratings: Overall = 90% Adjusted Efficiency Margin + 10% Consistency Component';
COMMENT ON COLUMN team_ratings.overall_composite IS 'Main rating: 90% normalized adj_net + 10% consistency_score';
COMMENT ON COLUMN team_ratings.consistency_score IS 'Rewards lower variance in tempo and offensive efficiency across games';
COMMENT ON COLUMN team_ratings.tempo_variance IS 'Std deviation of possessions per game (lower = more consistent)';
COMMENT ON COLUMN team_ratings.off_eff_variance IS 'Std deviation of offensive efficiency per game (lower = more consistent)';
