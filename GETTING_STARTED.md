# Getting Started - Your First 30 Minutes

Follow this step-by-step guide to get the app running from scratch.

## What You'll Need

- [ ] 15-30 minutes of time
- [ ] Internet connection
- [ ] Computer with Python 3.9+ and Node.js 16+
- [ ] Text editor (VS Code recommended)

---

## Step 1: Get Your API Credentials (10 minutes)

### Supabase Setup

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign up with GitHub (easiest)
4. Create new project:
   - Name: `cbb-ratings` (or your choice)
   - Database Password: Generate a strong one
   - Region: Choose closest to you
   - Click "Create new project"
5. Wait 2 minutes for project to provision
6. Go to **Settings** > **API**
7. Copy these two values:
   - `Project URL` (starts with https://)
   - `anon public` key (long string)
8. Keep this tab open, you'll need it again

### CBBD API Key

1. Go to [collegebasketballdata.com](https://collegebasketballdata.com)
2. Create an account
3. Navigate to API section
4. Get your API key (Bearer token)
5. Copy and save it

---

## Step 2: Set Up the Database (5 minutes)

1. In your Supabase project, click **SQL Editor** (left sidebar)
2. Click **New query**
3. Open this project's `database/schema.sql` file
4. Copy the entire contents
5. Paste into Supabase SQL Editor
6. Click **Run** (or press Ctrl+Enter)
7. You should see "Success. No rows returned"
8. Click **Table Editor** (left sidebar)
9. Verify you see a table called `team_ratings`

**You're done with Supabase setup!**

---

## Step 3: Configure the Project (5 minutes)

### Backend Environment

1. Open terminal in project root
2. Copy environment template:
   ```bash
   copy .env.example .env
   # On Mac/Linux: cp .env.example .env
   ```
3. Open `.env` in text editor
4. Fill in your values:
   ```
   CBBD_API_KEY=paste_your_cbbd_key_here
   SUPABASE_URL=paste_your_supabase_url_here
   SUPABASE_ANON_KEY=paste_your_supabase_anon_key_here
   ```
5. Save and close

### Frontend Environment

1. In terminal:
   ```bash
   copy frontend\.env.example frontend\.env
   # On Mac/Linux: cp frontend/.env.example frontend/.env
   ```
2. Open `frontend/.env` in text editor
3. Should already say:
   ```
   REACT_APP_API_URL=http://localhost:5000
   ```
4. This is correct for local development, save and close

**Configuration complete!**

---

## Step 4: Install Dependencies (5 minutes)

### Backend (Python)

```bash
# Navigate to api folder
cd api

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# Install packages (will take 2-3 minutes)
pip install -r requirements.txt

# Go back to root
cd ..
```

### Frontend (Node.js)

```bash
# Navigate to frontend folder
cd frontend

# Install packages (will take 2-3 minutes)
npm install

# Go back to root
cd ..
```

**Dependencies installed!**

---

## Step 5: Start the Application (2 minutes)

### Terminal 1 - Backend

```bash
cd api
venv\Scripts\activate          # Windows (if not already active)
# source venv/bin/activate     # Mac/Linux
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Running on http://localhost:5000
```

**Keep this terminal running!**

### Terminal 2 - Frontend

Open a NEW terminal window:

```bash
cd frontend
npm start
```

After 10-20 seconds, your browser should automatically open to:
```
http://localhost:3000
```

**Keep this terminal running too!**

---

## Step 6: Load Your First Data (3 minutes)

1. In the browser at `http://localhost:3000`
2. You should see the header "College Basketball Ratings 2025-26"
3. Click the **"Refresh Data"** button (white button, top right)
4. Wait 30-60 seconds while it:
   - Fetches data from CBBD API
   - Calculates ratings for all teams
   - Saves to Supabase
5. The table should populate with teams!

**Success! You have data!**

---

## Step 7: Verify Everything Works

### Test Sorting
1. Click the "Rating" column header
2. Click again to reverse sort
3. Try clicking other headers

### Test Team Details
1. Find any team in the table
2. Click the row
3. Details should expand below
4. Click again to collapse

### Find Syracuse (Test Case)
1. Use Ctrl+F (or Cmd+F) to search "Syracuse"
2. Click the Syracuse row
3. Verify:
   - Ratings are displayed
   - Four factors shown
   - Colors are Orange/Blue gradient

**Everything works!**

---

## What You Should See

### Main Page
```
┌────────────────────────────────────────────────────┐
│ 🏀 College Basketball Ratings 2025-26  [Refresh]  │
├────┬──────────┬────────┬─────┬─────┬──────────────┤
│ #  │ Team     │ Rating │ OFF │ DEF │ ...          │
├────┼──────────┼────────┼─────┼─────┼──────────────┤
│ 1  │ Duke     │ 95.2   │ 96  │ 94  │ ...          │
│ 2  │ UConn    │ 94.8   │ 95  │ 95  │ ...          │
│... │ ...      │ ...    │ ... │ ... │ ...          │
└────┴──────────┴────────┴─────┴─────┴──────────────┘
```

### Team Detail (when clicked)
```
┌────────────────────────────────────────────────────┐
│              SYRACUSE                              │
│         (Orange/Blue Gradient Background)          │
├────────────────────────────────────────────────────┤
│ Overall Rating: 87.3 (Rank: #45)                  │
│                                                    │
│ OFFENSE (89.1, Rank: #15)                         │
│ • eFG%: 52.3% (#22)                               │
│ • ORB%: 28.5% (#18)                               │
│ • TOV%: 16.2% (#30)                               │
│ • FTR:  35.1% (#12)                               │
│                                                    │
│ DEFENSE (85.4, Rank: #22)                         │
│ • Opp eFG%: 48.7% (#25)                           │
│ • ... (more stats)                                │
└────────────────────────────────────────────────────┘
```

---

## Common Issues & Fixes

### "Module not found" (Python)
```bash
# Make sure virtual environment is activated
cd api
venv\Scripts\activate
pip install -r requirements.txt
```

### "Command not found: npm"
- Install Node.js from [nodejs.org](https://nodejs.org)
- Download LTS version
- Restart terminal after installation

### "CBBD_API_KEY not found"
- Check `.env` file exists in root directory
- Verify no extra spaces in `.env`
- Make sure virtual environment is activated

### Frontend won't start
```bash
cd frontend
rm -rf node_modules
npm install
npm start
```

### Database errors
- Verify schema was run in Supabase SQL Editor
- Check Supabase credentials in `.env`
- Confirm project is active in Supabase dashboard

### CORS errors in browser
- Ensure backend is running on port 5000
- Check `REACT_APP_API_URL` in `frontend/.env`
- Restart both servers

---

## Next Steps

Now that it's working:

1. **Explore the data**
   - Sort by different columns
   - Click various teams
   - Compare offensive vs defensive ratings

2. **Understand the code**
   - Read [DEVELOPMENT.md](DEVELOPMENT.md) for code overview
   - Check out `api/calculate_ratings.py` for rating formula
   - Look at `frontend/src/components/TeamTable.jsx` for table logic

3. **Customize**
   - Adjust rating weights in `calculate_ratings.py`
   - Modify table columns in `TeamTable.jsx`
   - Change colors in CSS files

4. **Deploy** (when ready)
   - Follow [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
   - Push to GitHub
   - Deploy to Vercel

---

## Helpful Commands

### Stop the servers
- Press `Ctrl+C` in each terminal

### Restart backend
```bash
cd api
venv\Scripts\activate
python app.py
```

### Restart frontend
```bash
cd frontend
npm start
```

### Refresh data manually
- Just click "Refresh Data" in the app
- Or call API directly:
  ```bash
  curl -X POST http://localhost:5000/api/refresh
  ```

---

## You're All Set!

You now have:
- ✅ Backend running (Flask API)
- ✅ Frontend running (React app)
- ✅ Database configured (Supabase)
- ✅ Data loaded (362 teams)
- ✅ Syracuse test case verified

**Time to explore college basketball ratings!**

---

## Getting Help

Stuck? Check these in order:

1. [QUICKSTART.md](QUICKSTART.md) - Quick command reference
2. [SETUP.md](SETUP.md) - Detailed setup with troubleshooting
3. [DEVELOPMENT.md](DEVELOPMENT.md) - Code structure and customization
4. Browser console (F12) - Check for JavaScript errors
5. Terminal output - Check for Python errors

---

**Welcome to College Basketball Ratings!**
