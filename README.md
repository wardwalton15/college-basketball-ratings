# College Basketball Ratings

A web application that displays college basketball team ratings based on the Four Factors methodology with opponent adjustments.

![Project Status](https://img.shields.io/badge/status-MVP-green)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![React](https://img.shields.io/badge/react-18.2-blue)

## Overview

This application provides comprehensive team ratings for Division I college basketball teams using advanced analytics:

- **Overall Team Ratings** - Composite score from offensive and defensive performance
- **Four Factors Analysis** - Breakdown by eFG%, Rebounding, Turnovers, and Free Throws
- **Opponent Adjustments** - KenPom-style adjustments for strength of schedule
- **Interactive Sorting** - Sort teams by any metric
- **Detailed Team Views** - Click any team to see full statistical breakdown

## Features

### Current (MVP - Phase 1)

- Main table with all 362 D-I teams
- Sortable columns for all metrics
- Click-to-expand team details with color schemes
- Manual data refresh from CBBD API
- Responsive design for mobile and desktop

### Coming Soon (Phase 2)

- LLM-generated team descriptions
- Automated daily updates
- Historical trend charts
- Strength of schedule visualization
- Player-level data integration

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- CBBD API key ([get one here](https://collegebasketballdata.com))
- Supabase account (free tier)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd college-basketball-ratings
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Set up the database**
   - Create a Supabase project
   - Run the SQL in `database/schema.sql`

4. **Start the backend**
   ```bash
   cd api
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   python app.py
   ```

5. **Start the frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

6. **Open the app**
   - Navigate to `http://localhost:3000`
   - Click "Refresh Data" to load teams

For detailed setup instructions, see [SETUP.md](SETUP.md).

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 with TanStack Table |
| Backend | Python Flask |
| Database | Supabase (PostgreSQL) |
| Data Source | CBBD API (collegebasketballdata.com) |
| Hosting | Vercel (planned) |

## Rating Methodology

### Overall Rating
```
Overall = (Offensive × 0.52) + (Defensive × 0.48)
```

### Offensive Rating
Combines four factors with weightings:
- **eFG%** (40%): Effective Field Goal Percentage
- **ORB%** (20%): Offensive Rebound Percentage
- **TOV%** (25%): Turnover Percentage (lower is better)
- **FTR** (15%): Free Throw Rate

### Defensive Rating
Evaluates opponent-adjusted defensive performance:
- **Opp eFG%** (40%): Opponent shooting efficiency
- **Opp ORB%** (20%): Defensive rebounding
- **Forced TOV%** (25%): Creating turnovers
- **Opp FTR** (15%): Limiting free throws

All metrics use **opponent adjustments** from the CBBD API's adjusted efficiency endpoint, providing KenPom-style strength of schedule corrections.

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

### Viewing Teams
- Teams are displayed in a sortable table
- Click any column header to sort
- Default sort: Overall Rating (highest first)

### Team Details
- Click any team row to expand
- Shows overall, offensive, and defensive ratings
- Displays all four factors with individual ranks
- Team colors applied to detail view

### Refreshing Data
- Click "Refresh Data" in the header
- Fetches latest data from CBBD API
- Recalculates all ratings
- Updates database

## Development

### Running Tests
```bash
# Test data fetching
cd api
python fetch_data.py

# Test rating calculations
python calculate_ratings.py
```

### Environment Variables

**Backend (.env)**
```
CBBD_API_KEY=your_key_here
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=your_key_here
```

**Frontend (.env)**
```
REACT_APP_API_URL=http://localhost:5000
```

## Deployment

The application is configured for deployment on Vercel:

1. Connect GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main

See [SETUP.md](SETUP.md) for detailed deployment instructions.

## Data Source

This application uses data from [CollegeBasketballData.com](https://collegebasketballdata.com) via the `cbbd` Python package.

- Team season statistics (box scores)
- Adjusted efficiency ratings (opponent-adjusted)
- Team metadata (colors, logos)

## Contributing

This is currently an MVP. Future enhancements are planned for Phase 2.

## License

This project is for educational and personal use.

## Acknowledgments

- Data provided by [CollegeBasketballData.com](https://collegebasketballdata.com)
- Rating methodology inspired by Dean Oliver's Four Factors
- Opponent adjustments based on KenPom methodology

---

**Built for college basketball analytics enthusiasts**
