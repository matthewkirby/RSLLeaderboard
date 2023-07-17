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
        settings.playerlist_schema_path,
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
        settings.playerlist_db_path,
        settings.leaderboard_db_path
    ]

    # Delete the databases if they exist
    for db_path in database_paths:
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Deleted database: {db_path}")

    print("All databases deleted.")


def insert_racelist(race_data):
    """ Inserts an entry into the racelist table. First checks to ensure the race does not already have an entry.
    Returns: status_code (boolean indicating if the race was added)
    """
    status_code = False
    conn = create_connection(settings.racelist_db_path)
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
        conn.commit()
        status_code = True

    conn.close()
    return status_code


def insert_entrant(race_data, entrant):
    print(f"\tAdding {entrant['user']['id']} to {race_data['slug']}.")
    conn = create_connection(settings.racelist_db_path)
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

    conn.commit()
    conn.close()


def load_json_races():
    """
    If a race needs to be manually added to the database, place it in the add_races folder.
    Deletes the json afterwards. (NOT YET IMPLEMENTED)
    """
    newdata = {}
    json_list = glob.glob(os.path.join(settings.script_dir, "add_races", "**.json"))
    print(f"Found {len(json_list)} json races.")
    for newrace in json_list:
        # Load and add the race to the racelist table
        with open(newrace, 'r') as fpointer:
            race_data = json.load(fpointer)
        status_code = insert_racelist(race_data)

        # If the race was added, add the entrants
        if status_code:
            for entrant in race_data['entrants']:
                insert_entrant(race_data, entrant)