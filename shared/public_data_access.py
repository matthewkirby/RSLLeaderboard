import sqlite3
import settings
from collections import namedtuple


RaceRecord = namedtuple('RaceRecord', ['slug', 'url', 'ended_at', 'season'])
EntrantRecord = namedtuple('EntrantRecord', [
    'name', 'discriminator', 'status', 'finish_time', 'place', 'comment', 'delta'
])


def create_connection():
    """ Create database connection and execute any queries that should be run every time. """
    conn = sqlite3.connect(settings.racelist_db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def get_racelist_all(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT slug, url, ended_at, season FROM racelist ORDER BY ended_at DESC")
    rows = cursor.fetchall()
    racelist = [RaceRecord(*row)._asdict() for row in rows]
    return racelist


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


def get_racelist_by_player(conn, userid):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rl.slug, rl.url, rl.ended_at, rl.season
        FROM entrants AS e
        LEFT JOIN racelist AS rl ON e.race_slug = rl.slug
        WHERE e.user_id=?
        ORDER BY rl.ended_at DESC
    """, (userid,))
    rows = cursor.fetchall()
    racelist = [RaceRecord(*row)._asdict() for row in rows]
    return racelist


def get_race_entrants(conn, slug):
    delta = "100*(entrants.rating_after_mu - entrants.rating_before_mu \
    - 2*(entrants.rating_after_sigma - entrants.rating_before_sigma))"
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT players.name, players.discriminator, entrants.status, 
               entrants.finish_time, entrants.place, entrants.comment,
               {delta}
        FROM entrants
        LEFT JOIN players ON entrants.user_id = players.userid
        WHERE entrants.race_slug=?
        ORDER BY COALESCE(entrants.place, 99999)
    """, (slug,))
    rawentrants = cursor.fetchall()
    entrants = [EntrantRecord(*row)._asdict() for row in rawentrants]
    return entrants