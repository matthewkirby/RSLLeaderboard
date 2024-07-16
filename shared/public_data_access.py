import sqlite3
import settings
from collections import namedtuple


RaceRecord = namedtuple('RaceRecord', ['slug', 'url', 'ended_at', 'season'])
EntrantRecord = namedtuple('EntrantRecord', [
    'name', 'discriminator', 'status', 'finish_time', 'place', 'comment', 'delta', 'ruleset'
])


def create_connection():
    """ Create database connection and execute any queries that should be run every time. """
    conn = sqlite3.connect(settings.racelist_db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def get_racelist(conn, where_clause=""):
    cursor = conn.cursor()
    query = ["SELECT DISTINCT rl.slug, rl.url, rl.ended_at, rl.season",
             "FROM entrants AS e",
             "LEFT JOIN racelist AS rl ON e.race_slug = rl.slug",
             where_clause,
             "ORDER BY rl.ended_at DESC"]
    cursor.execute(" ".join(query))
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
               {delta}, entrants.ruleset
        FROM entrants
        LEFT JOIN players ON entrants.user_id = players.userid
        WHERE entrants.race_slug=?
        ORDER BY COALESCE(entrants.finish_time, 'p0DT09H59M59.99S')
    """, (slug,))
    rawentrants = cursor.fetchall()
    entrants = [EntrantRecord(*row)._asdict() for row in rawentrants]
    return entrants