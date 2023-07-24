import argparse
import settings
import data_access as dba
import calculate_ratings as cr
from fetch_racetime import get_new_racetime_races, reset_racetime_data
from leaderboard import summarize_seasonal_leaderboard


def main():
    # If required, set up the environment
    dba.initialize_databases()

    # Load any missing races
    dba.load_json_races()
    get_new_racetime_races()

    # Calculate the leaderboard ratings
    cr.calculate_ratings(settings.current_season)
    summarize_seasonal_leaderboard()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Leaderboard')
    parser.add_argument('--reset', action='store_true', help='Reset the database')
    args = parser.parse_args()

    if args.reset:
        dba.delete_databases()
        reset_racetime_data()
    else:
        main()