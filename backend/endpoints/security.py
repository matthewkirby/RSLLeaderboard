import functools
from flask import request
import settings

def is_valid(api_key):
    if api_key and api_key == settings.rslbot_api_key:
        return True
    return False


def api_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.json:
            api_key = request.json.get("api_key")
        else:
            return "Please provide an API key", 400
        
        if request.method == "POST" and is_valid(api_key):
            return func(*args, **kwargs)
        else:
            return "The provided API key is invalid.", 403
    
    return decorator