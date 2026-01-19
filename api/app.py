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

from fetch_data import CBBDataFetcher, validate_team_data
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
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/teams', methods=['GET'])
def get_teams():
    """
    Get all team ratings from database

    Query Parameters:
        season (int): Season year (default: 2025)
        sort_by (str): Field to sort by (default: overall_rating)
        order (str): Sort order 'asc' or 'desc' (default: desc)
    """
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500

    season = request.args.get('season', 2025, type=int)
    sort_by = request.args.get('sort_by', 'overall_rating')
    order = request.args.get('order', 'desc')

    try:
        # Build query
        query = supabase.table('team_ratings').select('*').eq('season', season)

        # Add sorting
        ascending = order.lower() == 'asc'
        query = query.order(sort_by, desc=not ascending)

        # Execute query
        response = query.execute()

        return jsonify({
            'success': True,
            'count': len(response.data),
            'teams': response.data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/teams/<team_name>', methods=['GET'])
def get_team(team_name):
    """
    Get specific team data

    Path Parameters:
        team_name (str): Name of the team

    Query Parameters:
        season (int): Season year (default: 2025)
    """
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500

    season = request.args.get('season', 2025, type=int)

    try:
        response = supabase.table('team_ratings') \
            .select('*') \
            .eq('team_name', team_name) \
            .eq('season', season) \
            .execute()

        if not response.data:
            return jsonify({
                'success': False,
                'error': 'Team not found'
            }), 404

        return jsonify({
            'success': True,
            'team': response.data[0]
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """
    Refresh all team data from CBBD API

    Request Body (JSON):
        season (int): Season year (default: 2025 for 2024-25 season)
        scaling_factor (float): Optional custom scaling factor
    """
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500

    try:
        # Get request parameters
        data = request.get_json() or {}
        season = data.get('season', 2025)  # Use 2025 for current season
        scaling_factor = data.get('scaling_factor')

        print(f"Starting data refresh for season {season}...")

        # Fetch data from CBBD API
        fetcher = CBBDataFetcher()
        raw_data = fetcher.fetch_all_data(season)

        # Process and combine all data
        processed_teams = fetcher.process_team_data(raw_data, season)

        # Filter valid teams
        valid_teams = [t for t in processed_teams if validate_team_data(t)]

        if not valid_teams:
            return jsonify({
                'success': False,
                'error': 'No valid team data received'
            }), 500

        print(f"Processing {len(valid_teams)} valid teams...")

        # Calculate ratings
        calculator = RatingCalculator(scaling_factor=scaling_factor)
        rated_teams = calculator.process_teams(valid_teams)

        # Prepare data for database
        db_records = []
        for team in rated_teams:
            record = {
                'team_name': team.get('team'),
                'season': season,
                'conference': team.get('conference'),
                'overall_rating': team.get('overall_rating'),
                'offensive_rating': team.get('offensive_rating'),
                'defensive_rating': team.get('defensive_rating'),
                'off_efg': team.get('off_efg_pct'),
                'off_orb': team.get('off_orb_pct'),
                'off_tov': team.get('off_tov_pct'),
                'off_ftr': team.get('off_ftr'),
                'def_efg': team.get('def_efg_pct'),
                'def_orb': team.get('def_orb_pct'),
                'def_tov': team.get('def_tov_pct'),
                'def_ftr': team.get('def_ftr'),
                'tempo': team.get('tempo'),
                'primary_color': team.get('color'),
                'secondary_color': team.get('alt_color'),
                'logo_url': team.get('logo'),
                'last_updated': datetime.now().isoformat()
            }
            db_records.append(record)

        print(f"Saving {len(db_records)} records to database...")

        # Upsert to database (insert or update if exists)
        response = supabase.table('team_ratings').upsert(
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
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get statistics about the database

    Query Parameters:
        season (int): Season year (default: 2025)
    """
    if not supabase:
        return jsonify({'error': 'Database not configured'}), 500

    season = request.args.get('season', 2025, type=int)

    try:
        response = supabase.table('team_ratings').select('*').eq('season', season).execute()

        if not response.data:
            return jsonify({
                'success': True,
                'stats': {
                    'total_teams': 0,
                    'last_updated': None
                }
            })

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
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
