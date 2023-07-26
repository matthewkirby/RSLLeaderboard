import os
import json
from datetime import datetime
from trueskill import Rating
import settings
import data_access as dba
from models.player import Player


_required_races_to_qualify = 3


def _save_player_list(data):
    with open(settings.leaderboard_file_path, 'w') as fpointer:
        json.dump(data, fpointer, indent=4)


def _load_player_list():
    conn = dba.create_connection(settings.racelist_db_path)
    column_list = ['userid', 'name', 'discriminator', 'entries', 'finishes', 'rating_mu', 'rating_sigma']
    player_data = dba.fetch_all_players(conn, columns=column_list)
    conn.close()

    player_list = []
    for player in player_data:
        pl = Player(player[0], player[1], player[2], Rating(mu=player[5], sigma=player[6]))
        pl.set_entry_data(entries=player[3], finishes=player[4])
        player_list.append(pl.export_player_info())
    return player_list


def summarize_seasonal_leaderboard():
    full_player_list = _load_player_list()

    # Sort qualified players by rating and add a 'placement' key to the dict
    qualified_players = [player for player in full_player_list if player['finishes'] >= _required_races_to_qualify]
    qualified_players = sorted(qualified_players, key=lambda player: player['rating'], reverse=True)
    qualified_players = [{**qualified_players[i], 'placement': i+1} for i in range(len(qualified_players))]

    # Sort the unqualified players alphabetically
    unqualified_players = [player for player in full_player_list if player['finishes'] < _required_races_to_qualify]
    unqualified_players = sorted(unqualified_players, key=lambda player: player['name'])

    # Output the data
    leaderboard = {
        'metadata': {
            'season': settings.current_season,
            'datetime': datetime.utcnow().isoformat(),
            'required_races': _required_races_to_qualify
        },
        'qualified': qualified_players,
        'unqualified': unqualified_players
    }
    _save_player_list(leaderboard)