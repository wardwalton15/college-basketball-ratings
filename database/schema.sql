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

    -- Our composite ratings (from four factors)
    overall_composite DECIMAL(5,2),
    raw_composite DECIMAL(5,2),
    off_composite DECIMAL(5,2),
    def_composite DECIMAL(5,2),

    -- API adjusted efficiency (KenPom-style, pts per 100 possessions)
    adj_off DECIMAL(6,2),
    adj_def DECIMAL(6,2),
    adj_net DECIMAL(6,2),

    -- Rankings
    overall_rank INT,
    raw_composite_rank INT,
    off_composite_rank INT,
    def_composite_rank INT,
    rank_off INT,   -- API adj offensive rank
    rank_def INT,   -- API adj defensive rank
    rank_net INT,   -- API adj net rank

    -- Offensive four factors (raw season stats)
    off_efg DECIMAL(5,2),         -- Effective FG%
    off_to_ratio DECIMAL(5,3),    -- Turnover ratio
    off_orb DECIMAL(5,2),         -- Offensive rebound %
    off_ftr DECIMAL(5,2),         -- Free throw rate

    -- Defensive four factors (opponent stats)
    def_efg DECIMAL(5,2),
    def_to_ratio DECIMAL(5,3),
    def_orb DECIMAL(5,2),
    def_ftr DECIMAL(5,2),

    -- Other metrics
    pace DECIMAL(5,2),
    srs DECIMAL(6,2),

    -- Branding
    primary_color VARCHAR(10),
    secondary_color VARCHAR(10),
    logo_url TEXT,
    abbreviation VARCHAR(10),

    -- Metadata
    last_updated TIMESTAMP DEFAULT NOW(),

    UNIQUE(team_name, season)
);

-- Indexes
CREATE INDEX idx_overall_composite ON team_ratings(overall_composite DESC);
CREATE INDEX idx_raw_composite ON team_ratings(raw_composite DESC);
CREATE INDEX idx_adj_net ON team_ratings(adj_net DESC);
CREATE INDEX idx_team_season ON team_ratings(team_name, season);
CREATE INDEX idx_season ON team_ratings(season);
CREATE INDEX idx_conference ON team_ratings(conference);
