""" Functions to fetch data from google sheets """
import os
import json
import argparse
import datetime
from collections import namedtuple
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import data_access as dba
import settings
from models.rated_async_player import RatedAsyncPlayer


# Build datatypes for the downloaded data
RequestData = namedtuple('RequestData', ['name', 'optin', 'url', 'ruleset', 'number'])
SubmitData = namedtuple('SubmitData', ['name', 'url', 'number', 'time', 'vod_link', 'finished'])


# Define base strings for all rated asyncs
base_season_string = "season{}"
base_ra_slug = "rated-async-{}"
base_ra_datetime = "{}T04:00:00Z"


def create_connection_google():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(settings.google_sheets_key_path, scope)
    client = gspread.authorize(credentials)
    return client


def load_ra_info():
    if os.path.exists(settings.rated_async_info_path):
        with open(settings.rated_async_info_path, 'r') as fpointer:
            data = json.load(fpointer)
        return data
    else:
        return {}


def save_ra_info(ra_info):
    with open(settings.rated_async_info_path, 'w') as fpointer:
        json.dump(ra_info, fpointer, indent=4)


def add_ra_info(season_number, race_number, race_date, force_add):
    ra_info = load_ra_info()
    season_string = base_season_string.format(season_number)
    race_slug = base_ra_slug.format(race_number)
    race_datetime = base_ra_datetime.format(race_date)

    # Ensure season exists in metadata record
    if season_string not in ra_info.keys():
        ra_info[season_string] = {}

    # Check if we need to add the race or not
    if race_slug in ra_info[season_string].keys() and not force_add:
        print(f"  {race_slug} info already exists in rated async info file. Skipping...")
        return

    # Add the new entry
    ra_info[season_string][race_slug] = {
        'number': race_number,
        'finish_time': race_datetime
    }

    # Save the metadata file
    save_ra_info(ra_info)


def delete_ra_info(season_number, race_slug):
    season_string = base_season_string.format(season_number)
    ra_info = load_ra_info()
    del ra_info[season_string][race_slug]
    save_ra_info(ra_info)


def fetch_ra_request_data(client):
    request_sheet = client.open_by_key(settings.sheets_id_ra_request)
    worksheet = request_sheet.get_worksheet(0)
    raw_request_data = worksheet.get("B:F")
    full_data = [RequestData(*row[:4], int(row[4])) for row in raw_request_data[1:]]
    return full_data


def fetch_ra_submit_data(client):
    submit_sheet = client.open_by_key(settings.sheets_id_ra_submit)
    worksheet = submit_sheet.get_worksheet(0)
    raw_submit_data = worksheet.get("B:G")
    full_data = [SubmitData(*row[:2], int(row[2]), *row[3:]) for row in raw_submit_data[1:]]
    return full_data


def filter_google_data(data, *conditions):
    filtered_list = []
    for row in data:
        if all(all(getattr(row, attr) == value for attr, value in condition.items()) for condition in conditions):
            filtered_list.append(row)
    return filtered_list


def parse_userid(url):
    patreon_lut = {
        "emosoda": "07QXz83Ke6WeZDjr",
        "rando-god": "PyZ2Dv30Q4oewXma",
        "BrotinderDose": "NY0OkW1Y2vWKalP1",
        "drooness": "JN9rVpW90ojq8Llv",
        "TrenteR": "rVwLN8B8Y43Pa52R",
        "tanjo3": "07QXz83KQkWeZDjr"
    }
    userid = url.split('/')[-1]
    if userid in patreon_lut.keys():
        userid = patreon_lut[userid]
    return userid


def combine_request_submit_data(requests, submits):
    entrants = { parse_userid(row.url): RatedAsyncPlayer(row.name, parse_userid(row.url), row.ruleset) for row in requests }
    for row in submits:
        userid = parse_userid(row.url)
        entrants[userid].done = True
        entrants[userid].time = row.time
        entrants[userid].media = row.vod_link

    ruleset_filtered = {key: entrants[key] for key in entrants.keys() if entrants[key].ruleset == "Standard"}
    return ruleset_filtered


def compute_placements(race_data):
    def time_to_seconds(entry):
        h, m, s = map(int, entry[1].split(':'))
        return h*3600 + m*60 + s

    finish_times = [[row.userid, row.time] for row in race_data.values() if row.done]
    sorted_times = sorted(finish_times, key=time_to_seconds)
    for i in range(len(sorted_times)):
        userid = sorted_times[i][0]
        race_data[userid].place = i + 1

    return race_data


def add_new_race(season_number, race_number, race_date, force_add):
    race_slug = base_ra_slug.format(race_number)

    # If --force, delete existing db data for the race
    conn = dba.create_connection(settings.racelist_db_path)
    if force_add:
        dba.delete_race(conn, race_slug)
    conn.close()

    # Add the new metadata
    add_ra_info(season_number, race_number, race_date, force_add)
    update_race_data(season_number, refresh=False)


def update_race_data(season_number, refresh):
    # Load the list of rated async data
    season_string = base_season_string.format(season_number)
    ra_info = load_ra_info()

    # Identify which rated asyncs that we need to download and clean existing data
    race_download_queue = []
    conn = dba.create_connection(settings.racelist_db_path)
    for race_slug in ra_info[season_string].keys():
        if not dba.race_exists(conn, race_slug) or refresh:
            race_download_queue.append(race_slug)
            dba.delete_race(conn, race_slug)

    # Exit if no races to download
    if len(race_download_queue) == 0:
        print("No new race data to fetch.")
        return

    # Download the data
    google_client = create_connection_google()
    request_data = fetch_ra_request_data(google_client)
    submit_data = fetch_ra_submit_data(google_client)

    # Filter and compute placements for each race
    for race_slug in race_download_queue:
        print(f"Adding {race_slug}...")

        # Filter down to a single race
        race_info = ra_info[season_string][race_slug]
        requests = filter_google_data(request_data, {'number': race_info['number']})
        submits = filter_google_data(submit_data, {'number': race_info['number']}, {'finished': 'Yes'})

        # Calculate results
        joint_data = combine_request_submit_data(requests, submits)
        race_results = compute_placements(joint_data)

        # Record the race
        race_data = {
            'slug': race_slug, 'ended_at': race_info['finish_time'], 'url': None,
            'entrants': [entry.rtgg_style_output() for entry in race_results.values()]
        }
        dba.insert_new_race(conn, race_data)
        conn.commit()        

    google_client.session.close()
    conn.close()


def delete_race(season_number, race_number, dbonly):
    race_slug = base_ra_slug.format(race_number)
    conn = dba.create_connection(settings.racelist_db_path)
    dba.delete_race(conn, race_slug)
    if not dbonly:
        delete_ra_info(season_number, race_slug)
    conn.close()


def validate_date(date_str):
    # Check if the date string has the correct format (YYYY-MM-DD)
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Expected YYYY-MM-DD.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download rated async data from google sheets")

    # Make the main functionality mutually exclusive
    primary_arg_group = parser.add_mutually_exclusive_group()
    primary_arg_group.add_argument("--refresh", action="store_true", help="Refresh db data for all existing races.")
    primary_arg_group.add_argument("--new", action="store_true", help="Add a race.")
    primary_arg_group.add_argument("--delete", action="store_true", help="Delete a race.")

    # Mode specific args
    parser.add_argument("-s", "--season", type=int, default=settings.current_season, help="Seasonal data to access.")
    parser.add_argument("-n", "--number", type=int, help="Which rated async to modify.")
    parser.add_argument("-d", "--date", type=validate_date, help="Recorded date for a new race.")
    parser.add_argument("--force", action="store_true", help="Add the race metadata even if the race already exists.")
    parser.add_argument("--dbonly", action="store_true", help="Only delete the database entry and leave metadata.")
    args = parser.parse_args()

    # Call the appropriate function for the given usage mode
    if args.refresh:
        print(f"Refreshing Season {args.season} data.")
        update_race_data(args.season, refresh=True)
    elif args.new:
        if args.number is None or args.date is None:
            parser.error("Both -n and -d are required to add a new race.")
        print(f"Adding Season {args.season} Rated Async {args.number}.")
        add_new_race(args.season, args.number, args.date, args.force)
    elif args.delete:
        if args.number is None:
            parser.error("-n is required when deleting a seed.")
        print(f"Deleting Rated Async {args.number}")
        delete_race(args.season, args.number, args.dbonly)
    else:
        parser.print_help()