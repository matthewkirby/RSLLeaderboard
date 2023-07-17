import os
from configparser import ConfigParser

# Define the root directory of the project
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
script_dir = os.path.join(project_root, 'scripts')

# Read the configuration file
config = ConfigParser()
config.read(os.path.join(project_root, 'config', 'config.ini'))

# Define global app settings
current_season = config.getint('AppSettings', 'current_season')

# Define paths from config file
racelist_db_path = os.path.join(project_root, config.get('RacelistDB', 'database_path'))
racelist_schema_path = os.path.join(project_root, config.get('RacelistDB', 'schema_path'))
playerlist_db_path = os.path.join(project_root, config.get('PlayerlistDB', 'database_path'))
playerlist_schema_path = os.path.join(project_root, config.get('PlayerlistDB', 'schema_path'))
leaderboard_db_path = os.path.join(project_root, config.get('LeaderboardDB', 'database_path'))
leaderboard_schema_path = os.path.join(project_root, config.get('LeaderboardDB', 'schema_path'))