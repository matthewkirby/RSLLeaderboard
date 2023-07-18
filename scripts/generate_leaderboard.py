import argparse
import data_access as dba
import calculate_ratings as cr
import settings


def main():
    dba.initialize_databases()
    dba.load_json_races()
    cr.calculate_ratings(settings.current_season)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Leaderboard')
    parser.add_argument('--reset', action='store_true', help='Reset the database')
    args = parser.parse_args()

    if args.reset:
        dba.delete_databases()
    else:
        main()