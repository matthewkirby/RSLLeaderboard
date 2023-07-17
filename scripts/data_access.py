""" Functions that interact with the databases """
import os
import sqlite3
import glob
import json
import settings


def create_connection(db_path):
    """ Create database connection and execute any queries that should be run every time. """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_databases():
    schema_paths = [
        settings.racelist_schema_path,
        settings.leaderboard_schema_path
    ]

    for sc_path in schema_paths:
        # First check if the schema file exists
        if os.path.exists(sc_path):
            # Open the schema file
            with open(sc_path, 'r') as file:
                sql_commands = file.read()

            # Establish connection to the database
            conn = create_connection(settings.racelist_db_path)
            c = conn.cursor()

            # Execute SQL commands from the file
            print(f"SQL Execute > {sc_path}")
            c.executescript(sql_commands)

            # Commit changes and close the connection
            conn.commit()
            conn.close()


def delete_databases():
    # Get the paths to the databases from settings
    database_paths = [
        settings.racelist_db_path,
        settings.leaderboard_db_path
    ]

    # Delete the databases if they exist
    for db_path in database_paths:
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Deleted database: {db_path}")

    print("All databases deleted.")


def insert_racelist(conn, race_data):
    """ Inserts an entry into the racelist table. First checks to ensure the race does not already have an entry.
    Returns: status_code (boolean indicating if the race was added)
    """
    status_code = False
    c = conn.cursor()

    # Check if the entry already exists
    c.execute("SELECT COUNT(*) FROM racelist WHERE slug = ?", (race_data['slug'],))
    if c.fetchone()[0] == 0:
        print(f"Adding new race: {race_data['slug']}")
        insert_sql = """
            INSERT INTO racelist (slug, url, ended_at, season)
            VALUES (?, ?, ?, ?)
        """

        c.execute(insert_sql, (
            race_data['slug'],
            race_data['url'],
            race_data['ended_at'],
            settings.current_season
        ))
        status_code = True

    return status_code


def fetch_all_races(conn, season=settings.current_season, columns=None):
    c = conn.cursor()

    # Build the SELECT statement
    if columns is None:
        select_columns = "*"
    else:
        select_columns = ", ".join(columns)

    # Build the WHERE clause for the season
    where_clause = f"WHERE season = {season}"

    c.execute(f"SELECT {select_columns} FROM racelist {where_clause} ORDER BY ended_at ASC")
    races = c.fetchall()
    return races


def insert_player(conn, player):
    c = conn.cursor()

    # Check if the entrant exists in the player table already
    c.execute("SELECT COUNT(*) FROM players WHERE userid = ?", (player['id'],))
    count = c.fetchone()[0]
    if count > 0:
        return

    insert_sql = """
        INSERT INTO players (userid, name, discriminator, racetime_url, twitch_display_name, twitch_url)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    c.execute(insert_sql, (
        player['id'],
        player['name'],
        player['discriminator'],
        player['url'],
        player['twitch_display_name'],
        player['twitch_channel']
    ))


def insert_entrant(conn, race_data, entrant):
    print(f"\tAdding {entrant['user']['id']} to {race_data['slug']}.")
    c = conn.cursor()

    insert_sql = """
        INSERT INTO entrants (race_slug, user_id, status, finish_time, place, comment)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    c.execute(insert_sql, (
        race_data['slug'],
        entrant['user']['id'],
        entrant['status']['value'],
        entrant['finish_time'],
        entrant['place'],
        entrant['comment']
    ))


def fetch_entrants_by_race(conn, race_slug):
    c = conn.cursor()
    c.execute("SELECT * FROM entrants WHERE race_slug = ?", (race_slug,))
    entrants = c.fetchall()
    return entrants


def load_json_races():
    """
    If a race needs to be manually added to the database, place it in the add_races folder.
    Deletes the json afterwards. (NOT YET IMPLEMENTED)
    """
    newdata = {}
    json_list = glob.glob(os.path.join(settings.script_dir, "add_races", "**.json"))
    if len(json_list) < 1:
        return

    print(f"Found {len(json_list)} new json races.")
    conn = create_connection(settings.racelist_db_path)
    for newrace in json_list:
        # Load and add the race to the racelist table
        with open(newrace, 'r') as fpointer:
            race_data = json.load(fpointer)
        status_code = insert_racelist(conn, race_data)

        # If the race was added, add the entrants
        if status_code:
            for entrant in race_data['entrants']:
                insert_player(conn, entrant['user'])
                insert_entrant(conn, race_data, entrant)
        conn.commit()

    conn.close()