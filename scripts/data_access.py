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
    conn = create_connection(settings.racelist_db_path)
    c = conn.cursor()

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
    conn.close()


def insert_entrants(race_data, entrant):
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