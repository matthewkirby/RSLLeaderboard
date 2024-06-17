from flask import Blueprint, jsonify
import os
import json
from settings import weights_file_path


weights_blueprint = Blueprint('weights', __name__)

@weights_blueprint.route('/weights', methods=['GET'])
def get_weights():
  with open(weights_file_path) as fpointer:
    weights = json.load(fpointer)
  return jsonify(weights)