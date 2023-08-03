from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from endpoints.leaderboard_endpoints import leaderboard_bp
from endpoints.racelist_endpoints import racelist_bp


rsl_api = Flask(__name__)
cors = CORS(rsl_api)
limiter = Limiter(
    get_remote_address,
    app=rsl_api,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)


# Register the endpoint blueprints
rsl_api.register_blueprint(leaderboard_bp, url_prefix='/api')
rsl_api.register_blueprint(racelist_bp, url_prefix='/api')


if __name__ == "__main__":
    rsl_api.run()