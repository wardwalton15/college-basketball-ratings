import React from 'react';
import './TeamDetail.css';

function TeamDetail({ team }) {
  const primaryColor = team.primary_color || '#1e3a8a';
  const secondaryColor = team.secondary_color || '#3b82f6';

  return (
    <div
      className="team-detail"
      style={{
        '--team-primary': primaryColor,
        '--team-secondary': secondaryColor,
      }}
    >
      <div className="detail-header">
        <h2>{team.team_name}</h2>
        {team.conference && <span className="detail-conference">{team.conference}</span>}
      </div>

      <div className="detail-content">
        {/* Overall Rating */}
        <div className="rating-section overall-section">
          <h3>Overall Rating</h3>
          <div className="rating-value large">
            {team.overall_rating?.toFixed(1) || 'N/A'}
          </div>
          {team.overall_rank && (
            <div className="rank-badge">Rank: #{team.overall_rank}</div>
          )}
        </div>

        {/* Offensive Rating */}
        <div className="rating-section">
          <h3>Offense</h3>
          <div className="rating-value">
            {team.offensive_rating?.toFixed(1) || 'N/A'}
          </div>
          {team.offensive_rank && (
            <div className="rank-badge">Rank: #{team.offensive_rank}</div>
          )}

          <div className="factors-grid">
            <div className="factor-item">
              <span className="factor-label">eFG%</span>
              <span className="factor-value">
                {team.off_efg?.toFixed(1) || 'N/A'}%
              </span>
              {team.off_efg_rank && (
                <span className="factor-rank">(#{team.off_efg_rank})</span>
              )}
            </div>
            <div className="factor-item">
              <span className="factor-label">ORB%</span>
              <span className="factor-value">
                {team.off_orb?.toFixed(1) || 'N/A'}%
              </span>
              {team.off_orb_rank && (
                <span className="factor-rank">(#{team.off_orb_rank})</span>
              )}
            </div>
            <div className="factor-item">
              <span className="factor-label">TOV%</span>
              <span className="factor-value">
                {team.off_tov?.toFixed(1) || 'N/A'}%
              </span>
              {team.off_tov_rank && (
                <span className="factor-rank">(#{team.off_tov_rank})</span>
              )}
            </div>
            <div className="factor-item">
              <span className="factor-label">FTR</span>
              <span className="factor-value">
                {team.off_ftr?.toFixed(1) || 'N/A'}
              </span>
              {team.off_ftr_rank && (
                <span className="factor-rank">(#{team.off_ftr_rank})</span>
              )}
            </div>
          </div>
        </div>

        {/* Defensive Rating */}
        <div className="rating-section">
          <h3>Defense</h3>
          <div className="rating-value">
            {team.defensive_rating?.toFixed(1) || 'N/A'}
          </div>
          {team.defensive_rank && (
            <div className="rank-badge">Rank: #{team.defensive_rank}</div>
          )}

          <div className="factors-grid">
            <div className="factor-item">
              <span className="factor-label">Opp eFG%</span>
              <span className="factor-value">
                {team.def_efg?.toFixed(1) || 'N/A'}%
              </span>
              {team.def_efg_rank && (
                <span className="factor-rank">(#{team.def_efg_rank})</span>
              )}
            </div>
            <div className="factor-item">
              <span className="factor-label">Opp ORB%</span>
              <span className="factor-value">
                {team.def_orb?.toFixed(1) || 'N/A'}%
              </span>
              {team.def_orb_rank && (
                <span className="factor-rank">(#{team.def_orb_rank})</span>
              )}
            </div>
            <div className="factor-item">
              <span className="factor-label">Forced TOs</span>
              <span className="factor-value">
                {team.def_tov?.toFixed(1) || 'N/A'}%
              </span>
              {team.def_tov_rank && (
                <span className="factor-rank">(#{team.def_tov_rank})</span>
              )}
            </div>
            <div className="factor-item">
              <span className="factor-label">Opp FTR</span>
              <span className="factor-value">
                {team.def_ftr?.toFixed(1) || 'N/A'}
              </span>
              {team.def_ftr_rank && (
                <span className="factor-rank">(#{team.def_ftr_rank})</span>
              )}
            </div>
          </div>
        </div>

        {/* Tempo */}
        <div className="rating-section tempo-section">
          <h3>Tempo</h3>
          <div className="rating-value">
            {team.tempo?.toFixed(1) || 'N/A'}
          </div>
          <div className="tempo-description">possessions/game</div>
          {team.tempo_rank && (
            <div className="rank-badge">Rank: #{team.tempo_rank}</div>
          )}
        </div>
      </div>

      <div className="detail-footer">
        <p className="methodology-note">
          Ratings based on Four Factors with opponent adjustments
        </p>
      </div>
    </div>
  );
}

export default TeamDetail;
