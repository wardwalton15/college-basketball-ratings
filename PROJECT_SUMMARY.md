# Project Summary

## Overview

A complete MVP web application for college basketball team ratings using the Four Factors methodology with opponent-adjusted metrics from CollegeBasketballData.com.

## What's Built

### Backend (Python/Flask)
- **app.py** - Flask API server with 5 REST endpoints
- **fetch_data.py** - CBBD API integration with retry logic
- **calculate_ratings.py** - Four Factors rating algorithm implementation
- **PostgreSQL database** - Supabase for team ratings storage

### Frontend (React)
- **App.js** - Main application with state management
- **TeamTable.jsx** - Sortable table using TanStack Table
- **TeamDetail.jsx** - Expandable team details with dynamic colors
- **RefreshButton.jsx** - Manual data refresh component

### Features

- Display all 360+ Division I teams in sortable table
- 10+ statistical metrics per team
- Opponent-adjusted efficiency ratings
- Click-to-expand team details
- Manual data refresh
- Responsive mobile design
- Real-time loading states and error handling

## Architecture

```
React Frontend → Flask Backend → CBBD API
                      ↓
               Supabase Database
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18.2, TanStack Table 8.11, Axios |
| Backend | Python 3.9+, Flask 3.0, flask-cors |
| Database | Supabase (PostgreSQL) |
| Data Source | CBBD API |
| Deployment | Vercel (configured) |

## Rating Formula

**Overall Composite:**
- Raw Composite (33%): Weighted blend of offensive and defensive factors
- Adjusted Net Rating (67%): Opponent-adjusted efficiency from CBBD API

**Offensive Composite:**
- eFG% (40%) + ORB% (20%) + (100-TOV%) (25%) + FTR (15%)

**Defensive Composite:**
- (100-Opp eFG%) (40%) + (100-Opp ORB%) (20%) + Forced TOV% (25%) + (100-Opp FTR) (15%)

## Project Statistics

- **~2,600 lines of code** (backend + frontend + config)
- **3 Python modules** (app, fetch, calculate)
- **4 React components** (App, TeamTable, TeamDetail, RefreshButton)
- **5 API endpoints** (health, teams, team detail, refresh, stats)
- **Supports 360+ teams** with full statistical breakdowns

## Status

✅ **MVP Complete & Ready for Deployment**

## Getting Started

See [SETUP.md](SETUP.md) for complete installation and setup instructions.

## Documentation

- [README.md](README.md) - Project overview
- [SETUP.md](SETUP.md) - Setup guide
- [QUICKSTART.md](QUICKSTART.md) - Command reference
- [DEVELOPMENT.md](DEVELOPMENT.md) - Developer guide
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Deployment checklist
