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


def _fetch_conditional_summary():
  url = "https://raw.githubusercontent.com/matthewkirby/plando-random-settings/master/weights/conditional_summary.json"
  try:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
  except requests.exceptions.RequestException as e:
    print(f"Error fetching RSL Conditional Summary:\n${e}")
    return None


def _summarize_conditionals(cond_weights):
  base_cond_info_list = _fetch_conditional_summary()
  if base_cond_info_list is None:
    return [], []

  cond_list, settings_to_skip = [], []
  for base_cond_info in base_cond_info_list:
    cond = {
      "name": base_cond_info["id"].replace('_', ' '),
      "state": cond_weights[base_cond_info["id"]][0],
      "opts": "",
      "desc": base_cond_info["description"]
    }

    weights = cond_weights[base_cond_info["id"]][1:]
    if len(weights) > 0:
      str_opts = [ str(w) for w in weights ]
      str_opts[0] = str_opts[0] + '%'
      cond["opts"] = f'({", ".join(str_opts)})'
      cond["desc"] = base_cond_info["description"].format(*str_opts)

    if cond["state"]:
      settings_to_skip += base_cond_info["settings_to_skip"]
    cond_list.append(cond)

  return cond_list, settings_to_skip


def _summarize_weights(weights, settings_to_skip):
  # This should exclude everything that is managed as
  # a multiselect or a conditional
  randomized, static = {}, {}
  for name, options in weights.items():
    if name in settings_to_skip:
      continue

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
  cond_weights = global_settings.pop("conditionals")
  conditionals, settings_to_skip = _summarize_conditionals(cond_weights)
  multiselects = raw["multiselect"]
  randomized, static = _summarize_weights(raw["weights"], settings_to_skip)
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
