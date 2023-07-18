import trueskill as ts
import data_access as dba
import settings
from models.player import Player
from models.race import Race


def load_seasonal_data(season, conn):
    # Load the list of all players
    players = dba.fetch_all_players(conn, columns=['userid', 'name', 'discriminator'])
    playerlist = {player[0]: Player(player[0], player[1], player[2], ts.Rating()) for player in players}

    # Load the list of all races
    races = dba.fetch_all_races(conn, season, columns=['slug', 'ended_at'])
    racelist = []
    for race in races:
        slug, end_time = race
        results = dba.fetch_entrants_by_race(conn, slug, columns=['id', 'user_id', 'place'])
        racelist.append(Race(slug, end_time, results))
    racelist.sort(key=lambda race: race.end_time)

    return playerlist, racelist


def calculate_ratings(season):
    conn = dba.create_connection(settings.racelist_db_path)

    # Load the data for the given season
    playerlist, racelist = load_seasonal_data(season, conn)

    # Iterate over the races and calculate ratings
    for race in racelist:
        # Mark that the player participated in the race (and finished)
        for player in race.entrants:
            playerlist[player.userid].joined(player.place)

        # Lists required for trueskill.rate
        ratings_before = [(playerlist[e.userid].rating,) for e in race.entrants]
        placements = [e.place for e in race.entrants]
        dnf_place = max(e for e in placements if e is not None) + 1
        placements = [e if e is not None else dnf_place for e in placements]

        # Calculate new ratings
        ratings_after = ts.rate(ratings_before, ranks=placements)

        # Record the results
        for i in range(len(race.entrants)):
            # Record the before/after ratings in the Race object
            race.entrants[i].rating_before = ratings_before[i][0]
            race.entrants[i].rating_after = ratings_after[i][0]

            # Record the new rating in the Player object
            playerlist[race.entrants[i].userid].rating = ratings_after[i][0]

    # Update the tables with the new values
    dba.update_entrants(conn, racelist)
    dba.update_players(conn, playerlist)

    conn.commit()
    conn.close()