""" Functions that interact with the databases """
import os
import sqlite3
import glob
import json
import settings


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
            conn = sqlite3.connect(settings.racelist_db_path)
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