from flask import Blueprint, jsonify, request
import os
from settings import racelist_db_path, current_season
import public_data_access as pub


racelist_bp = Blueprint('racelist', __name__)


def does_database_exist():
    if not os.path.exists(racelist_db_path):
        return False
    return True


@racelist_bp.route('/racelist', methods=['GET'])
def get_racelist():
    # Parse additional args
    userid = request.args.get('player', type=str)
    season = request.args.get('season', type=int)

    # Setup
    if not does_database_exist():
        return jsonify({})
    conn = pub.create_connection()
    data = {}

    # Make the appropriate racelist query
    if userid is not None:
        data['racelist'] = pub.get_racelist_by_player(conn, userid)
    elif season is not None:
        data['racelist'] = pub.get_racelist_by_season(conn, season)
    else:
        data['racelist'] = pub.get_racelist_all(conn)

    # Get race entrant information
    data['entrants'] = { race["slug"]: pub.get_race_entrants(conn, race["slug"]) for race in data['racelist'][:5] }

    conn.close()
    return jsonify(data)


@racelist_bp.route('/race_entrants', methods=['GET'])
def get_race_entrants():
    slug = request.args.get('slug', type=str)

    if does_database_exist():
        conn = pub.create_connection()
        response = { slug: pub.get_race_entrants(conn, slug) }
        conn.close()

    return jsonify(response)
