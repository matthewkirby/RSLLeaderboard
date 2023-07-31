from flask import Blueprint, jsonify, request
import os
from settings import racelist_db_path, current_season
import public_data_access as pub


racelist_bp = Blueprint('racelist', __name__)


def does_database_exist():
    if not os.path.exists(racelist_db_path):
        return False
    return True


def get_seasonal_races(season=current_season):
    # Initial page load sends entrant info for most recent 5 races
    conn = pub.create_connection()
    racelist = pub.get_racelist_by_season(conn, season)
    entrants = { race["slug"]: pub.get_race_entrants(conn, race["slug"]) for race in racelist[:5] }
    response = { 'racelist': racelist, 'entrants': entrants }
    conn.close()
    return response


@racelist_bp.route('/racelist', methods=['GET'])
def get_racelist():
    data = {}

    if does_database_exist():
        data = get_seasonal_races()

    return jsonify(data)

@racelist_bp.route('/race_entrants', methods=['GET'])
def get_race_entrants():
    slug = request.args.get('slug', type=str)

    if does_database_exist():
        conn = pub.create_connection()
        response = { slug: pub.get_race_entrants(conn, slug) }
        conn.close()

    return jsonify(response)
