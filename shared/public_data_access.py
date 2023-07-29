import sqlite3
import settings
from collections import namedtuple


RaceRecord = namedtuple('RaceRecord', ['slug', 'url', 'ended_at', 'season'])
EntrantRecord = namedtuple('EntrantRecord', [
    'name', 'discriminator', 'status', 'finish_time', 'place', 'comment'
])


def create_connection():
    """ Create database connection and execute any queries that should be run every time. """
    conn = sqlite3.connect(settings.racelist_db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def get_racelist_by_season(conn, season):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT slug, url, ended_at FROM racelist
        WHERE season=?
        ORDER BY ended_at DESC
    """, (season,))
    rows = cursor.fetchall()
    racelist = [RaceRecord(*row, season)._asdict() for row in rows]
    return racelist


def get_race_entrants(conn, slug):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT players.name, players.discriminator, entrants.status, 
               entrants.finish_time, entrants.place, entrants.comment
        FROM entrants
        LEFT JOIN players ON entrants.user_id = players.userid
        WHERE entrants.race_slug=?
        ORDER BY entrants.place
    """, (slug,))
    rawentrants = cursor.fetchall()
    entrants = [EntrantRecord(*row)._asdict() for row in rawentrants]
    return entrants