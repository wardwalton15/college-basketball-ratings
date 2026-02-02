import React, { useState, useEffect } from 'react';
import TeamTable from './components/TeamTable';
import RefreshButton from './components/RefreshButton';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  // Fetch teams on mount
  useEffect(() => {
    fetchTeams();
  }, []);

  const fetchTeams = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/teams`);
      const data = await response.json();

      if (data.success) {
        setTeams(data.teams);
        if (data.teams.length > 0) {
          setLastUpdated(data.teams[0].last_updated);
        }
      } else {
        setError(data.error || 'Failed to fetch teams');
      }
    } catch (err) {
      setError('Failed to connect to API: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ season: 2026 }),
      });

      const data = await response.json();

      if (data.success) {
        // Fetch updated teams
        await fetchTeams();
        setLastUpdated(data.timestamp);
      } else {
        setError(data.error || 'Failed to refresh data');
      }
    } catch (err) {
      setError('Failed to refresh data: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="container">
          <div className="header-content">
            <div className="header-left">
              <h1>College Basketball Ratings 2025-26</h1>
              {lastUpdated && (
                <p className="last-updated">
                  Last updated: {new Date(lastUpdated).toLocaleString()}
                </p>
              )}
            </div>
            <div className="header-right">
              <RefreshButton onClick={handleRefresh} loading={loading} />
            </div>
          </div>
        </div>
      </header>

      <main className="container">
        {error && (
          <div className="error-banner">
            <strong>Error:</strong> {error}
          </div>
        )}

        {loading && teams.length === 0 ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Loading team data...</p>
          </div>
        ) : (
          <TeamTable teams={teams} />
        )}

        {!loading && teams.length === 0 && !error && (
          <div className="empty-state">
            <p>No team data available. Click "Refresh Data" to load teams.</p>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <div className="container">
          <p>
            Data from{' '}
            <a
              href="https://collegebasketballdata.com"
              target="_blank"
              rel="noopener noreferrer"
            >
              CollegeBasketballData.com
            </a>
          </p>
          <p>Ratings based on Four Factors methodology with opponent adjustments</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
