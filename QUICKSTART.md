# Quick Start Reference

Fast reference for common tasks and commands.

## First Time Setup

```bash
# 1. Install backend dependencies
cd api
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt

# 2. Install frontend dependencies
cd ../frontend
npm install

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials

cp frontend/.env.example frontend/.env
# Edit with API URL
```

## Daily Development

### Start Backend (Terminal 1)
```bash
cd api
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
python app.py
```
Server runs at: `http://localhost:5000`

### Start Frontend (Terminal 2)
```bash
cd frontend
npm start
```
App opens at: `http://localhost:3000`

## Common Tasks

### Test Data Fetching
```bash
cd api
python fetch_data.py
```

### Test Rating Calculation
```bash
cd api
python calculate_ratings.py
```

### Build for Production
```bash
cd frontend
npm run build
```

### Clear Cache
```bash
# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install

# Backend
cd api
rm -rf venv
python -m venv venv
pip install -r requirements.txt
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Check API status |
| `/api/teams` | GET | Get all teams |
| `/api/teams/<name>` | GET | Get one team |
| `/api/refresh` | POST | Update data |
| `/api/stats` | GET | Get DB stats |

## Environment Variables

### Backend (.env in root)
```
CBBD_API_KEY=your_key
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=your_key
```

### Frontend (frontend/.env)
```
REACT_APP_API_URL=http://localhost:5000
```

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Check virtual env is activated
which python      # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend errors
```bash
# Clear and reinstall
rm -rf node_modules
npm install

# Check Node version
node --version    # Should be 16+
```

### Database issues
1. Check Supabase credentials in .env
2. Verify schema was created in Supabase SQL Editor
3. Test connection in Supabase dashboard

### CORS errors
- Make sure backend is running on port 5000
- Check REACT_APP_API_URL in frontend/.env
- Verify Flask-CORS is installed

## Git Commands

```bash
# Initial setup
git init
git add .
git commit -m "Initial commit"

# Create .gitignore entries
# Already done in .gitignore file

# Push to GitHub
git remote add origin <your-repo-url>
git push -u origin main
```

## File Locations

| What | Where |
|------|-------|
| API code | `api/` |
| React components | `frontend/src/components/` |
| Database schema | `database/schema.sql` |
| Environment config | `.env` and `frontend/.env` |
| Deployment config | `vercel.json` |

## Test URLs

After starting both servers:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000
- **Health Check:** http://localhost:5000/api/health
- **Teams List:** http://localhost:5000/api/teams

## Data Flow

1. Click "Refresh Data" button
2. Frontend calls `/api/refresh` (POST)
3. Backend calls CBBD API
4. Backend calculates ratings
5. Backend saves to Supabase
6. Frontend fetches updated data
7. Table displays teams

## Next Steps After Setup

1. Create Supabase account and project
2. Run `database/schema.sql` in Supabase SQL Editor
3. Get CBBD API key
4. Configure environment variables in `.env` files
5. Start backend and frontend servers
6. Click "Refresh Data" to load team data
7. Explore team ratings and details

## Support Files

- Project overview: [README.md](README.md)
- Full setup guide: [SETUP.md](SETUP.md)
- Developer guide: [DEVELOPMENT.md](DEVELOPMENT.md)
- Deployment: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
