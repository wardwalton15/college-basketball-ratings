# College Basketball Ratings - Setup Guide

This guide will walk you through setting up and running the College Basketball Ratings web application.

## Prerequisites

- **Python 3.9+** (for backend API)
- **Node.js 16+** (for frontend)
- **CBBD API Key** from [CollegeBasketballData.com](https://collegebasketballdata.com)
- **Supabase Account** (free tier works fine)

---

## Step 1: Database Setup (Supabase)

1. **Create a Supabase Account**
   - Go to [supabase.com](https://supabase.com)
   - Create a new project

2. **Create the Database Schema**
   - In your Supabase dashboard, go to SQL Editor
   - Copy the contents of `database/schema.sql`
   - Paste and run the SQL script

3. **Get Your Credentials**
   - Go to Project Settings > API
   - Copy the `URL` and `anon/public` key
   - Save these for the environment setup

---

## Step 2: Backend Setup

1. **Navigate to the API folder**
   ```bash
   cd api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv

   # Activate it:
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example file
   cp ../.env.example ../.env

   # Edit .env and add your credentials:
   CBBD_API_KEY=your_api_key_here
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your_anon_key_here
   ```

5. **Test the backend**
   ```bash
   python app.py
   ```

   The API should start on `http://localhost:5000`

6. **Test data fetching (optional)**
   ```bash
   python fetch_data.py
   ```

---

## Step 3: Frontend Setup

1. **Open a new terminal and navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env:
   REACT_APP_API_URL=http://localhost:5000
   ```

4. **Start the development server**
   ```bash
   npm start
   ```

   The app should open at `http://localhost:3000`

---

## Step 4: Load Initial Data

1. **Make sure both backend and frontend are running**
   - Backend: `http://localhost:5000`
   - Frontend: `http://localhost:3000`

2. **Click "Refresh Data" in the web app**
   - This will fetch data from the CBBD API
   - Calculate ratings for all teams
   - Store everything in Supabase

3. **Wait for the data to load**
   - This may take 30-60 seconds for ~362 teams
   - You'll see a loading spinner

4. **Verify the data**
   - Teams should appear in the table
   - Try sorting by different columns
   - Click a team row to see detailed stats

---

---

## Troubleshooting

### Backend Issues

**Error: "CBBD_API_KEY not found"**
- Make sure `.env` file exists in the root directory
- Check that the variable name is exactly `CBBD_API_KEY`
- Verify the API key is valid

**Error: "Database not configured"**
- Check Supabase credentials in `.env`
- Verify the schema was created successfully
- Test connection in Supabase dashboard

**API not starting**
- Make sure virtual environment is activated
- Verify all dependencies installed: `pip list`
- Check for port conflicts on 5000

### Frontend Issues

**Blank page or errors**
- Check browser console for errors (F12)
- Verify backend is running on port 5000
- Check `.env` has correct API URL

**Data not loading**
- Open browser Network tab (F12)
- Check API calls to `/api/teams`
- Verify backend is responding

**Table not sortable**
- Clear browser cache
- Check console for JavaScript errors
- Verify `@tanstack/react-table` is installed

---

## Production Deployment (Vercel)

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your-repo-url
   git push -u origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel will detect the `vercel.json` configuration

3. **Set environment variables in Vercel**
   - Go to Project Settings > Environment Variables
   - Add:
     - `CBBD_API_KEY`
     - `SUPABASE_URL`
     - `SUPABASE_ANON_KEY`
     - `REACT_APP_API_URL` (set to your Vercel domain)

4. **Deploy**
   - Vercel will automatically build and deploy
   - Your app will be live at `your-project.vercel.app`

---

## Usage

### Manual Data Refresh
- Click "Refresh Data" button in the header
- This fetches latest data from CBBD API
- Updates all team ratings
- May take 30-60 seconds

### Sorting Teams
- Click any column header to sort
- Click again to reverse sort order
- Arrow indicators show current sort

### Viewing Team Details
- Click any team row to expand
- Shows full breakdown of ratings
- Displays team colors
- Click again to collapse

### Understanding Ratings

**Overall Rating** = (Offensive × 0.52) + (Defensive × 0.48)

**Offensive Rating** considers:
- eFG% (40%): Shooting efficiency
- ORB% (20%): Offensive rebounding
- TOV% (25%): Turnover rate (lower is better)
- FTR (15%): Free throw rate

**Defensive Rating** considers:
- Opponent eFG% (40%): Defending the shot
- Opponent ORB% (20%): Defensive rebounding
- Forced TOV% (25%): Creating turnovers
- Opponent FTR (15%): Limiting free throws

All stats are **opponent-adjusted** (KenPom-style)

---

## Future Enhancements (Not Currently Implemented)

Phase 2 features planned but not yet built:
- LLM-generated team descriptions
- Automated daily updates via GitHub Actions
- Historical trend charts
- Strength of schedule visualization
- Player-level data integration

---

## Support

For issues or questions:
1. Check this setup guide
2. Review the main specification document
3. Check CBBD API documentation
4. Test individual components (fetch_data.py, calculate_ratings.py)

---

## Project Structure

```
college-basketball-ratings/
├── api/
│   ├── app.py              # Flask API server
│   ├── fetch_data.py       # CBBD API integration
│   ├── calculate_ratings.py # Rating calculations
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── TeamTable.jsx
│   │   │   ├── TeamDetail.jsx
│   │   │   └── RefreshButton.jsx
│   │   ├── App.js
│   │   └── index.js
│   └── package.json        # Node dependencies
├── database/
│   └── schema.sql          # Supabase schema
├── .env.example            # Environment template
└── vercel.json             # Deployment config
```
