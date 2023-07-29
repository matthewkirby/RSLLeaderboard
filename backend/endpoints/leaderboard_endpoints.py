from flask import Blueprint, jsonify
import os
import json
from settings import leaderboard_file_path


leaderboard_bp = Blueprint('leaderboard', __name__)


def read_leaderboard():
    if not os.path.exists(leaderboard_file_path):
        return {}
    else:
        with open(leaderboard_file_path, 'r') as fpointer:
            data = json.load(fpointer)
        return data


@leaderboard_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    data = read_leaderboard()
    return jsonify(data)