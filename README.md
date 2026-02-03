# College Basketball Ratings

A web application that displays college basketball team ratings using the Four Factors methodology with opponent adjustments.

![Project Status](https://img.shields.io/badge/status-MVP-green)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![React](https://img.shields.io/badge/react-18.2-blue)

## Overview

This application provides team ratings for all Division I college basketball teams using advanced analytics:

- **Overall Team Ratings** - Composite score combining offensive and defensive performance
- **Four Factors Analysis** - eFG%, Rebounding, Turnovers, and Free Throw Rate
- **Opponent Adjustments** - Strength-of-schedule corrections from CBBD API
- **Interactive Table** - Sort by any metric, click to expand team details
- **Responsive Design** - Works on mobile and desktop

## Features

- Sortable table with all 360+ D-I teams
- 10+ statistical metrics per team
- Click-to-expand team details with dynamic color schemes
- Manual data refresh from CollegeBasketballData.com API
- Real-time loading states and error handling

## Quick Start

### Prerequisites

- Python 3.9+ and Node.js 16+
- [CBBD API key](https://collegebasketballdata.com)
- [Supabase account](https://supabase.com) (free tier works)

### Installation

1. **Set up environment variables**
   ```bash
   cp .env.example .env
   cp frontend/.env.example frontend/.env
   # Edit both files with your credentials
   ```

2. **Set up the database**
   - Create a Supabase project
   - Run `database/schema.sql` in the SQL Editor

3. **Start the backend**
   ```bash
   cd api
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

4. **Start the frontend** (in a new terminal)
   ```bash
   cd frontend
   npm install
   npm start
   ```

5. **Load data**
   - Open `http://localhost:3000`
   - Click "Refresh Data" to fetch team data

See [SETUP.md](SETUP.md) for detailed instructions and troubleshooting.

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 with TanStack Table |
| Backend | Python Flask |
| Database | Supabase (PostgreSQL) |
| Data Source | CBBD API (collegebasketballdata.com) |
| Hosting | Vercel (planned) |

## Rating Methodology

**Overall Rating:** Blends raw composite (33%) with opponent-adjusted net rating (67%)

**Offensive Composite:** eFG% (40%) + ORB% (20%) + (100-TOV%) (25%) + FTR (15%)

**Defensive Composite:** (100-Opp eFG%) (40%) + (100-Opp ORB%) (20%) + Forced TOV% (25%) + (100-Opp FTR) (15%)

All metrics use opponent adjustments from the CBBD API for strength-of-schedule corrections.

## Project Structure

```
college-basketball-ratings/
├── api/                    # Python Flask backend
│   ├── app.py             # API routes
│   ├── fetch_data.py      # CBBD API integration
│   └── calculate_ratings.py # Rating calculations
├── frontend/              # React frontend
│   └── src/
│       ├── components/    # React components
│       ├── App.js        # Main application
│       └── index.js      # Entry point
├── database/             # Database schema
│   └── schema.sql       # Supabase table definitions
└── vercel.json          # Deployment configuration
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/teams` | GET | Get all team ratings |
| `/api/teams/:name` | GET | Get specific team |
| `/api/refresh` | POST | Refresh data from CBBD |
| `/api/stats` | GET | Database statistics |

## Usage

- **Sort:** Click column headers to sort teams
- **View Details:** Click any team row to expand full breakdown
- **Refresh Data:** Click "Refresh Data" button to fetch latest stats (takes ~30-60 seconds)

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for customization and extending features.

## Deployment

Configured for Vercel deployment. See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for the complete deployment guide.

## Documentation

- **[SETUP.md](SETUP.md)** - Complete setup guide with troubleshooting
- **[QUICKSTART.md](QUICKSTART.md)** - Quick command reference
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Guide for customization and adding features
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Pre-deployment verification

## Data Source

Data from [CollegeBasketballData.com](https://collegebasketballdata.com) via the `cbbd` Python package.

## License

This project is for educational and personal use.

---

**Built for college basketball analytics enthusiasts**
