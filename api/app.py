"""
Flask API for College Basketball Ratings
Provides endpoints for fetching and refreshing team ratings
"""

import os
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client

from fetch_data import CBBDataFetcher
from calculate_ratings import RatingCalculator

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("WARNING: Supabase credentials not found. Database operations will fail.")
    supabase: Client = None
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/teams', methods=['GET'])
def get_teams():
    """Get all team ratings from database."""
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500

    season = request.args.get('season', 2026, type=int)
    sort_by = request.args.get('sort_by', 'overall_composite')
    order = request.args.get('order', 'desc')

    try:
        query = supabase.table('team_ratings').select('*').eq('season', season)
        query = query.order(sort_by, desc=(order.lower() != 'asc'))
        response = query.execute()

        return jsonify({
            'success': True,
            'count': len(response.data),
            'teams': response.data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/teams/<team_name>', methods=['GET'])
def get_team(team_name):
    """Get a specific team's data."""
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500

    season = request.args.get('season', 2026, type=int)

    try:
        response = supabase.table('team_ratings') \
            .select('*') \
            .eq('team_name', team_name) \
            .eq('season', season) \
            .execute()

        if not response.data:
            return jsonify({'success': False, 'error': 'Team not found'}), 404

        return jsonify({'success': True, 'team': response.data[0]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """Fetch fresh data from CBBD API, calculate ratings, and store in database."""
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500

    try:
        data = request.get_json() or {}
        season = data.get('season', 2026)

        print(f"Starting data refresh for season {season}...")

        # 1. Fetch from API
        fetcher = CBBDataFetcher()
        raw_data = fetcher.fetch_all(season)
        teams = fetcher.build_team_records(raw_data, season)

        if not teams:
            return jsonify({'success': False, 'error': 'No team data received'}), 500

        # 2. Calculate ratings
        calculator = RatingCalculator()
        rated_teams = calculator.process_teams(teams)

        # 3. Prepare database records
        db_records = []
        for team in rated_teams:
            db_records.append({
                'team_name': team['team'],
                'season': season,
                'conference': team.get('conference'),
                'wins': team.get('wins'),
                'losses': team.get('losses'),
                'games': team.get('games'),
                'overall_composite': team.get('overall_composite'),
                'raw_composite': team.get('raw_composite'),
                'off_composite': team.get('off_composite'),
                'def_composite': team.get('def_composite'),
                'adj_off': team.get('adj_off'),
                'adj_def': team.get('adj_def'),
                'adj_net': team.get('adj_net'),
                'overall_rank': team.get('overall_rank'),
                'raw_composite_rank': team.get('raw_composite_rank'),
                'off_composite_rank': team.get('off_composite_rank'),
                'def_composite_rank': team.get('def_composite_rank'),
                'rank_off': team.get('rank_off'),
                'rank_def': team.get('rank_def'),
                'rank_net': team.get('rank_net'),
                'off_efg': team.get('off_efg'),
                'off_to_ratio': team.get('off_to_ratio'),
                'off_orb': team.get('off_orb'),
                'off_ftr': team.get('off_ftr'),
                'def_efg': team.get('def_efg'),
                'def_to_ratio': team.get('def_to_ratio'),
                'def_orb': team.get('def_orb'),
                'def_ftr': team.get('def_ftr'),
                'pace': team.get('pace'),
                'srs': team.get('srs'),
                'primary_color': team.get('primary_color'),
                'secondary_color': team.get('secondary_color'),
                'logo_url': team.get('logo'),
                'abbreviation': team.get('abbreviation'),
                'last_updated': datetime.now().isoformat(),
            })

        # 4. Upsert to database
        print(f"Saving {len(db_records)} records to database...")
        supabase.table('team_ratings').upsert(
            db_records,
            on_conflict='team_name,season'
        ).execute()

        print(f"Successfully updated {len(db_records)} teams")

        return jsonify({
            'success': True,
            'teams_updated': len(db_records),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics."""
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500

    season = request.args.get('season', 2026, type=int)

    try:
        response = supabase.table('team_ratings').select('*').eq('season', season).execute()

        if not response.data:
            return jsonify({'success': True, 'stats': {'total_teams': 0, 'last_updated': None}})

        teams = response.data
        last_updated = max(t.get('last_updated', '') for t in teams)

        return jsonify({
            'success': True,
            'stats': {
                'total_teams': len(teams),
                'last_updated': last_updated,
                'conferences': len(set(t.get('conference') for t in teams if t.get('conference')))
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
