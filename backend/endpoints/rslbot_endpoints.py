from flask import Blueprint, request
from datetime import datetime, timezone

from settings import current_season
from fetch_google import add_new_race, delete_race
from generate_leaderboard import generate_leaderboard


rslbot_blueprint = Blueprint('rslbot', __name__)

@rslbot_blueprint.route('/record_rated_async', methods=['POST'])
def record_rated_async():
    async_number = request.get_json().get("async_number", None)
    if async_number is None:
        return f"Async number invalid.", 400
    async_number = int(async_number)

    datetime_string = datetime.now(timezone.utc).strftime(r"%Y-%m-%dT%H:%M:%SZ")
    n_races_added = add_new_race(current_season, async_number, datetime_string, False)

    if n_races_added > 0:
        generate_leaderboard()
        return f"Rated async {async_number} successfully recorded!", 201
    else:
        return f"Rated async {async_number} already exists.", 201


@rslbot_blueprint.route('/delete_rated_async', methods=['POST'])
def delete_rated_async():
    async_number = request.get_json().get("async_number", None)
    if async_number is None:
        return f"Async number invalid.", 400
    async_number = int(async_number)

    delete_race(current_season, async_number, False)
    return f"Rated async {async_number} successfully deleted.", 201


@rslbot_blueprint.route('/refresh_rated_async', methods=['POST'])
def refresh_rated_async():
    async_number = request.get_json().get("async_number", None)
    if async_number is None:
        return f"Async number invalid.", 400
    async_number = int(async_number)

    datetime_string = datetime.now(timezone.utc).strftime(r"%Y-%m-%dT%H:%M:%SZ")
    delete_race(current_season, async_number, False)
    add_new_race(current_season, async_number, datetime_string, False)
    generate_leaderboard()
    return f"Rated async {async_number} successfully refreshed!", 201