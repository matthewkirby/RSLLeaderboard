import os
import json
from datetime import datetime
from configparser import ConfigParser

# Load an environment variables
environment = os.getenv("RSL_LEADERBOARD_ENV", "dev")

# Define the root directory of the project
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
script_dir = os.path.join(project_root, 'scripts')
data_dir = os.path.join(project_root, 'data')
frontend_dir = os.path.join(project_root, 'frontend')
backend_dir = os.path.join(project_root, 'backend')

# Read the configuration file
_config = ConfigParser()
_config.read(os.path.join(project_root, 'config', 'config.ini'))

# Define global app settings
current_season = _config.get('AppSettings', 'current_season')

# Define the season dates
with open(os.path.join(data_dir, 'season_dates.json'), 'r') as fpointer:
    _season_dates = json.load(fpointer)
season_dates = {}
for _snum, _sdata in _season_dates.items():
    _start_date = datetime.fromisoformat(_sdata["start_date"])
    _season_in_progress = _sdata["end_date"] is None
    _end_date = datetime.fromisoformat(_sdata["end_date"]) if not _season_in_progress else None
    season_dates[_snum] = (_start_date, _end_date)

# Define paths to the data files
racelist_db_path = os.path.join(data_dir, _config.get('RacelistDatabase', 'database_file'))
racelist_schema_path = os.path.join(project_root, "schema", _config.get('RacelistDatabase', 'schema_file'))
racelist_schema_v2_path = os.path.join(project_root, "schema", _config.get('RacelistDatabase', 'v2_file'))
leaderboard_file_path = os.path.join(data_dir, _config.get('LeaderboardData', 'data_file'))
weights_file_path = os.path.join(data_dir, "rsl_weight_summary.json")

# Define google sheets api config
google_sheets_key_path = os.path.join(project_root, _config.get('RatedAsync', 'google_sheets_path'))
spreadsheet_ids_path = os.path.join(project_root, _config.get('RatedAsync', 'spreadsheet_ids_path'))
rated_async_info_path = os.path.join(project_root, _config.get('RatedAsync', 'rated_async_info_path'))

# Load the ids for the two spreadsheets used for the rated async
_idconfig = ConfigParser()
_idconfig.read(spreadsheet_ids_path)
sheets_id_ra_request = _idconfig.get('RatedAsync', 'request_form')
sheets_id_ra_submit = _idconfig.get('RatedAsync', 'submit_form')

# Load the API key for RSLBot
rslbot_api_key = _idconfig.get('RSLBot', 'api_key')