""" Functions to fetch data from the racetime.gg API """
import os
import json
import requests
import tools
import settings
import datetime as dt
import data_access as dba


_last_race_path = os.path.join(settings.data_dir, "last_race_id.txt")
_racetime_cache_path = os.path.join(settings.data_dir, "racetime_cache.json")
_page_limit = 110
_racetime_goal_name = "Random settings league"
_base_racelist_endpoint = "races/data?page={}"
_base_race_endpoint = "{}/data"


def _read_last_race_id():
    if os.path.exists(_last_race_path):
        with open(_last_race_path, 'r') as fpointer:
            last_race_id = fpointer.readline()
        return last_race_id
    return None


def _write_last_race_id(last_race_id):
    print(f"Last race seen: {last_race_id}")
    with open(_last_race_path, 'w') as fpointer:
        fpointer.write(last_race_id)


def _cache_racetime_data(data):
    print("--Caching race data.")
    output_data = {
        "download_date": dt.datetime.now().isoformat(),
        "race_data": data
    }
    with open(_racetime_cache_path, 'w') as fpointer:
        json.dump(output_data, fpointer, indent=4)


def _read_racetime_cache():
    print("Loading race data from cache.")
    if os.path.exists(_racetime_cache_path):
        with open(_racetime_cache_path, 'r') as fpointer:
            data = json.load(fpointer)

        # Check that the data is from the last 24 hours
        current_time = dt.datetime.now()
        cache_date = dt.datetime.fromisoformat(data["download_date"])
        cache_age = current_time - cache_date
        if cache_age.total_seconds() > 24 * 60 * 60:
            print("--Cache is over 24 hours old, discarding.")
            tools.safe_file_delete(_racetime_cache_path)
            return None
        return data["race_data"]

    else:
        print("--Race data cache file does not exist")
        return None


def _reset_racetime_cache():
    tools.safe_file_delete(_racetime_cache_path)


def _racetime_api_call(api_endpoint):
    url = f"https://racetime.gg/ootr/{api_endpoint}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was not successful
        return response.json()  # Parse the JSON response and return it as a Python dictionary
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def _fetch_new_race_list_racetime():
    print("Getting race data from racetime.gg.")
    last_race_id = _read_last_race_id()

    race_data = []
    done_fetching = False
    for page_number in range(1, _page_limit):
        print(f"--Fetching page {page_number}.")
        one_page = _racetime_api_call(_base_racelist_endpoint.format(page_number))
        race_list_page = one_page["races"]

        for race in race_list_page:
            # If we have seen this race before, stop fetching data
            if last_race_id is not None and race["name"] == last_race_id:
                done_fetching = True
                break
            race_data.append(race)
        if done_fetching:
            break

    print(f"--Fetched data on {len(race_data)} new races.")
    return race_data


def _filter_new_race_data(race_data):
    slug_list = []
    for race in race_data:
        if race["goal"]["name"] == _racetime_goal_name:
            race_slug = race["name"].split("/")[1]
            slug_list.append(race_slug)
    return slug_list


def _fetch_new_race_list():
    full_race_data = None
    most_recent_race = None
    if settings.environment == "dev":
        full_race_data = _read_racetime_cache()
    if full_race_data is None:
        full_race_data = _fetch_new_race_list_racetime()
        if settings.environment == "dev":
            _cache_racetime_data(full_race_data)
        if len(full_race_data) > 0:
            most_recent_race = full_race_data[0]["name"]
    filtered_slug_list = _filter_new_race_data(full_race_data)
    return most_recent_race, filtered_slug_list


def _add_single_race(conn, race_slug):
    print(f"--Fetching data on {race_slug}")
    race_data = _racetime_api_call(_base_race_endpoint.format(race_slug))
    dba.insert_new_race(conn, race_data)


def get_new_racetime_races():
    most_recent_race, rsl_slug_list = _fetch_new_race_list()
    if len(rsl_slug_list) > 0:
        conn = dba.create_connection(settings.racelist_db_path)
        for race_slug in rsl_slug_list:
            _add_single_race(conn, race_slug)
        conn.commit()
        conn.close()
    _reset_racetime_cache()
    if most_recent_race is not None:
        _write_last_race_id(most_recent_race)


def reset_racetime_data():
    tools.safe_file_delete(_last_race_path)
    tools.safe_file_delete(_racetime_cache_path)