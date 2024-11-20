from flask import Blueprint, request, jsonify
from datetime import datetime, timezone

from endpoints.security import api_required
from settings import current_season
from fetch_google import add_new_race, delete_race
from generate_leaderboard import generate_leaderboard


rslbot_blueprint = Blueprint('rslbot', __name__)

def pack_response(text):
    return jsonify({"message": text})

@rslbot_blueprint.route('/record_rated_async', methods=['POST'])
@api_required
def record_rated_async():
    async_number = request.get_json().get("async_number", None)
    if async_number is None:
        return pack_response(f"Async number invalid."), 400
    async_number = int(async_number)

    datetime_string = datetime.now(timezone.utc).strftime(r"%Y-%m-%dT%H:%M:%SZ")

    try:
        n_races_added = add_new_race(current_season, async_number, datetime_string, False)
    except:
        return pack_response("Error while trying to record the race.")

    if n_races_added > 0:
        try:
            generate_leaderboard()
        except:
            return pack_response("Race successfully recorded, but encountered an error while updating ratings.")
        return pack_response(f"Rated async {async_number} successfully recorded!"), 201
    else:
        return pack_response(f"Rated async {async_number} already exists."), 201


@rslbot_blueprint.route('/delete_rated_async', methods=['POST'])
@api_required
def delete_rated_async():
    async_number = request.get_json().get("async_number", None)
    if async_number is None:
        return pack_response(f"Async number invalid."), 400
    async_number = int(async_number)

    try:
        delete_race(current_season, async_number, False)
    except:
        return pack_response(f"Encounted an error while attempting to delete rated async {async_number}.")
    return pack_response(f"Rated async {async_number} successfully deleted."), 201


@rslbot_blueprint.route('/refresh_rated_async', methods=['POST'])
@api_required
def refresh_rated_async():
    async_number = request.get_json().get("async_number", None)
    if async_number is None:
        return pack_response(f"Async number invalid."), 400
    async_number = int(async_number)

    datetime_string = datetime.now(timezone.utc).strftime(r"%Y-%m-%dT%H:%M:%SZ")
    delete_race(current_season, async_number, False)
    add_new_race(current_season, async_number, datetime_string, False)
    generate_leaderboard()
    return pack_response(f"Rated async {async_number} successfully refreshed!"), 201