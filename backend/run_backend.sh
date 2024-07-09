#!/bin/bash

# Make sure that you have loaded the python venv with
# $ source venv/bin/activate

gunicorn --bind 0.0.0.0:5000 backend_app:rsl_api