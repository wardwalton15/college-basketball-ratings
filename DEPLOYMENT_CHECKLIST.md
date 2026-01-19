# Deployment Checklist

Complete this checklist before deploying to production.

## Pre-Deployment

### Database Setup
- [ ] Supabase account created
- [ ] New project created in Supabase
- [ ] Database schema executed (`database/schema.sql`)
- [ ] Tables created successfully (verify in Supabase Table Editor)
- [ ] Indexes created (check schema.sql completion)
- [ ] Supabase URL copied
- [ ] Supabase anon key copied

### API Credentials
- [ ] CBBD account created at collegebasketballdata.com
- [ ] CBBD API key obtained
- [ ] API key tested (run `python api/fetch_data.py`)

### Local Testing
- [ ] Backend runs without errors (`python api/app.py`)
- [ ] Frontend runs without errors (`npm start`)
- [ ] Can fetch data via "Refresh Data" button
- [ ] Teams display in table
- [ ] Sorting works on all columns
- [ ] Team detail view opens on click
- [ ] Syracuse test case verified (correct stats and colors)
- [ ] No console errors in browser (F12)
- [ ] Mobile responsive view tested

### Code Quality
- [ ] No hardcoded credentials in code
- [ ] `.env` files in `.gitignore`
- [ ] All environment variables use `.env` files
- [ ] Error handling implemented
- [ ] Loading states implemented
- [ ] No debug/console.log statements in production code

## GitHub Setup

### Repository
- [ ] GitHub repository created
- [ ] `.gitignore` configured
- [ ] Initial commit created
- [ ] Code pushed to GitHub
- [ ] README.md looks good on GitHub
- [ ] SETUP.md accessible

### Secrets (for GitHub Actions - Phase 2)
- [ ] `CBBD_API_KEY` added to GitHub Secrets
- [ ] `SUPABASE_URL` added to GitHub Secrets
- [ ] `SUPABASE_ANON_KEY` added to GitHub Secrets

## Vercel Deployment

### Initial Setup
- [ ] Vercel account created
- [ ] GitHub repository connected to Vercel
- [ ] Project imported
- [ ] `vercel.json` detected

### Environment Variables
- [ ] `CBBD_API_KEY` set in Vercel
- [ ] `SUPABASE_URL` set in Vercel
- [ ] `SUPABASE_ANON_KEY` set in Vercel
- [ ] `REACT_APP_API_URL` set to production URL
- [ ] All variables marked as Production, Preview, Development as needed

### Build Settings
- [ ] Build command set (auto-detected from package.json)
- [ ] Output directory set (auto-detected as `build`)
- [ ] Node version compatible (16+)
- [ ] Python version compatible (3.9+)

### Domain
- [ ] Custom domain configured (optional)
- [ ] HTTPS enabled
- [ ] DNS records updated (if custom domain)

## Post-Deployment Testing

### Functionality
- [ ] Production site loads
- [ ] "Refresh Data" works
- [ ] Data persists in Supabase
- [ ] Teams display correctly
- [ ] Sorting works
- [ ] Team details work
- [ ] Syracuse test verified in production

### Performance
- [ ] Page load time acceptable (<3s)
- [ ] Table renders smoothly
- [ ] No console errors
- [ ] Mobile performance acceptable
- [ ] API response times acceptable

### Data Validation
- [ ] 300+ teams loaded
- [ ] Ratings calculated correctly
- [ ] Rankings in order
- [ ] No missing data (N/A values)
- [ ] Conference data populated

### Browser Testing
- [ ] Chrome tested
- [ ] Firefox tested
- [ ] Safari tested (if available)
- [ ] Mobile Chrome tested
- [ ] Mobile Safari tested (if available)

## Monitoring

### Initial Monitoring
- [ ] Vercel analytics enabled
- [ ] API response times monitored
- [ ] Error logs checked
- [ ] Database usage checked in Supabase

### Data Freshness
- [ ] Last updated timestamp displays
- [ ] Manual refresh works
- [ ] Data updates in reasonable time (<60s)

## Documentation

- [ ] README.md accurate
- [ ] SETUP.md complete
- [ ] QUICKSTART.md helpful
- [ ] API endpoints documented
- [ ] Environment variables documented
- [ ] Deployment process documented

## Phase 2 Preparation (Future)

- [ ] GitHub Actions workflow file ready
- [ ] Secrets configured for automated updates
- [ ] Cron schedule reviewed
- [ ] Error notification plan

## Security Review

- [ ] No API keys in frontend code
- [ ] Supabase RLS policies reviewed (optional)
- [ ] CORS configured correctly
- [ ] HTTPS enforced
- [ ] Environment variables secured

## Backup Plan

- [ ] Database export taken
- [ ] Environment variables backed up (securely)
- [ ] Rollback plan documented
- [ ] Support contacts available

## Go-Live

- [ ] All above items checked
- [ ] Final test in production
- [ ] Team notified (if applicable)
- [ ] Documentation URL shared
- [ ] First production data refresh completed

## Post-Launch

### Week 1
- [ ] Monitor daily for errors
- [ ] Check data freshness daily
- [ ] Verify Supabase limits not exceeded
- [ ] User feedback collected (if applicable)

### Month 1
- [ ] Performance metrics reviewed
- [ ] Usage patterns analyzed
- [ ] Phase 2 features prioritized
- [ ] Database optimization reviewed

---

## Emergency Contacts

- **Supabase Support:** support@supabase.com
- **Vercel Support:** support@vercel.com
- **CBBD Support:** via collegebasketballdata.com

## Rollback Procedure

If critical issues occur:

1. Revert deployment in Vercel (Deployments > Previous > Promote)
2. Check error logs in Vercel dashboard
3. Fix issues locally
4. Test thoroughly
5. Redeploy

---

**Last Updated:** [Date]
**Deployed By:** [Name]
**Production URL:** [URL]
