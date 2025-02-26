import argparse
import data_access as dba
import settings
from calculate_ratings import calculate_ratings
from leaderboard import summarize_seasonal_leaderboard


def cancel_race(conn, args):
    c = conn.cursor()
    # Verify that we have exactly 1 matching race
    c.execute("SELECT * FROM racelist WHERE slug = ? AND season = ?", (args.slug, args.season))
    results = c.fetchall()

    if len(results) == 0:
        print(f"Race with slug {args.slug} in season {args.season} not found.")
        return
    elif len(results) > 1:
        print(f"Found {len(results)} races with slug {args.slug} in season {args.season}.")
        print("========================================")
        print(results)
        print("Exiting...")

    # Cancel (or uncancel) the race
    sql = """
        UPDATE racelist
        SET dont_record = ?
        WHERE slug = ? AND season = ?
    """
    c.execute(sql, (
        1 if not args.inverse else 0,
        args.slug,
        args.season
    ))
    
    # Zero out the ratings information for the entrants in the race
    entrant_ids = dba.fetch_entrants_by_race(conn, args.slug, columns=["id"])
    entrant_ids = [e[0] for e in entrant_ids]
    sql = """
        UPDATE entrants
        SET rating_before_mu = NULL, rating_before_sigma = NULL, rating_after_mu = NULL, rating_after_sigma = NULL
        WHERE id = ?
    """
    for id in entrant_ids:
        c.execute(sql, (id,))

    conn.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Change a race in the database to be displayed on the website but not  included in rating calculation.")

    parser.add_argument("slug", help="Slug for the race to change.")
    parser.add_argument('-s', '--season', default=settings.current_season, help="Season for the race to change.")
    parser.add_argument('--inverse', action="store_true", help="Invert the operation and score a race previously cancelled.")
    args = parser.parse_args()

    conn = dba.create_connection(settings.racelist_db_path)
    cancel_race(conn, args)
    conn.close()

    calculate_ratings(settings.current_season)
    summarize_seasonal_leaderboard()