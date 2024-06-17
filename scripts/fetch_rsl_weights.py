import os
import requests
import settings
import json

_rsl_version_path = os.path.join(settings.data_dir, "rslversion.py")
_rsl_weights_path = os.path.join(settings.data_dir, "rsl_weight_summary.json")

def fetch_rsl_version():
  url = "https://raw.githubusercontent.com/matthewkirby/plando-random-settings/master/rslversion.py"
  try:
    response = requests.get(url)
    response.raise_for_status()
    with open(_rsl_version_path, 'w') as fpointer:
      fpointer.write(response.text)
  except requests.exceptions.RequestException as e:
    print(f"Error fetching RSL Version File:\n${e}")
    return None


def _fetch_raw_rsl_weights():
  url = "https://raw.githubusercontent.com/matthewkirby/plando-random-settings/master/weights/rsl_season6.json"
  try:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
  except requests.exceptions.RequestException as e:
    print(f"Error fetching RSL Weights File:\n${e}")
    return None


def _summarize_weights(weights):
  # This should exclude everything that is managed as
  # a multiselect or a conditional
  randomized, static = {}, {}
  for name, options in weights.items():
    total_weight = 0
    for _, w in options.items():
      total_weight += w

    if total_weight < 1.5:
      static[name] = [k for k,v in options.items() if v > 0.5][0]
    else:
      randomized[name] = options

  return randomized, static


def _parse_raw_rsl_weights(raw):
  global_settings = raw["options"]
  conditionals = global_settings.pop("conditionals")
  multiselects = raw["multiselect"]
  randomized, static = _summarize_weights(raw["weights"])
  output = {
    "global_settings": global_settings,
    "conditionals": conditionals,
    "multiselects": multiselects,
    "randomized": randomized,
    "static": static
  }
  return output


def fetch_rsl_weights():
  raw_weights = _fetch_raw_rsl_weights()
  output = _parse_raw_rsl_weights(raw_weights)
  with open(_rsl_weights_path, 'w') as fpointer:
    json.dump(output, fpointer)


fetch_rsl_weights()
