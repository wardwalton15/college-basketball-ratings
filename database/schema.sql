-- College Basketball Ratings Database Schema
-- To be executed in Supabase SQL Editor

CREATE TABLE IF NOT EXISTS team_ratings (
    id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    season INT NOT NULL,
    conference VARCHAR(50),

    -- Overall and component ratings
    overall_rating DECIMAL(5,2),
    offensive_rating DECIMAL(5,2),
    defensive_rating DECIMAL(5,2),

    -- Offensive Four Factors (opponent-adjusted)
    off_efg DECIMAL(5,2),
    off_orb DECIMAL(5,2),
    off_tov DECIMAL(5,2),
    off_ftr DECIMAL(5,2),

    -- Defensive Four Factors (opponent-adjusted)
    def_efg DECIMAL(5,2),
    def_orb DECIMAL(5,2),
    def_tov DECIMAL(5,2),
    def_ftr DECIMAL(5,2),

    -- Tempo
    tempo DECIMAL(5,2),

    -- Team branding
    primary_color VARCHAR(7),
    secondary_color VARCHAR(7),
    logo_url TEXT,

    -- Metadata
    last_updated TIMESTAMP DEFAULT NOW(),

    -- Ensure one record per team per season
    UNIQUE(team_name, season)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_overall_rating ON team_ratings(overall_rating DESC);
CREATE INDEX IF NOT EXISTS idx_team_season ON team_ratings(team_name, season);
CREATE INDEX IF NOT EXISTS idx_season ON team_ratings(season);
CREATE INDEX IF NOT EXISTS idx_conference ON team_ratings(conference);

-- Enable Row Level Security (optional for Supabase)
-- ALTER TABLE team_ratings ENABLE ROW LEVEL SECURITY;

-- Create policy to allow public read access
-- CREATE POLICY "Allow public read access" ON team_ratings
--     FOR SELECT USING (true);
