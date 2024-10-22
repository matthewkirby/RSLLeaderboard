import os
import requests
import settings
import json

# Leaving this commented because I am not currently using it but its next on to do list

# _rsl_version_path = os.path.join(settings.data_dir, "rslversion.py")
_rsl_weights_path = os.path.join(settings.data_dir, "rsl_weight_summary.json")
_alphabet = 'abcdefghijklmnopqrstuvwxyz'

# def fetch_rsl_version():
#   url = "https://raw.githubusercontent.com/matthewkirby/plando-random-settings/master/rslversion.py"
#   try:
#     response = requests.get(url)
#     response.raise_for_status()
#     with open(_rsl_version_path, 'w') as fpointer:
#       fpointer.write(response.text)
#   except requests.exceptions.RequestException as e:
#     print(f"Error fetching RSL Version File:\n${e}")
#     return None


def _fetch_rsl_file(path):
  url = f"https://raw.githubusercontent.com/matthewkirby/plando-random-settings/release/{path}"
  try:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
  except requests.exceptions.RequestException as e:
    print(f"Error fetching {path}:\n${e}")
    return None


def _summarize_conditionals(cond_weights):
  base_cond_info_list = _fetch_rsl_file("weights/conditional_summary.json")
  if base_cond_info_list is None:
    return [], []

  cond_list, settings_to_skip = [], []
  for base_cond_info in base_cond_info_list:
    cond = {
      "id": base_cond_info["id"],
      "name": base_cond_info["id"].replace('_', ' '),
      "state": cond_weights[base_cond_info["id"]][0],
      "defaults": [],
      "optstr": "",
      "desc": base_cond_info["description"]
    }

    weights = cond_weights[base_cond_info["id"]][1:]
    if len(weights) > 0:
      defaults = [ str(w) for w in weights ]
      cond["defaults"] = defaults
      cond["optstr"] = '(' + ', '.join(['{}' for i in range(len(defaults))]) + ')'
      
    if cond["state"]:
      settings_to_skip += base_cond_info["settings_to_skip"]
    cond_list.append(cond)

  return cond_list, settings_to_skip


def _summarize_weights(weights, settings_to_skip):
  randomized, static = {}, {}
  for name, options in weights.items():
    if name in settings_to_skip:
      continue
    randomized[name] = options

  return randomized


def _parse_raw_rsl_weights(raw):
  global_settings = raw["options"]
  cond_weights = global_settings.pop("conditionals")
  conditionals, settings_to_skip = _summarize_conditionals(cond_weights)
  multiselects = raw["multiselect"]
  randomized = _summarize_weights(raw["weights"], settings_to_skip)
  output = {
    "global_settings": global_settings,
    "conditionals": conditionals,
    "multiselects": multiselects,
    "weights": randomized,
    "overrides": {}
  }
  return output


def __extract_section(bigdict, key):
  return bigdict[key] if key in bigdict.keys() else {}


def _attach_override(override_name, summary):
  raw_override_file = _fetch_rsl_file(f"weights/{override_name}_override.json")
  override = {}

  # Parse overrides for options and conditionals
  list_options = ["tricks", "disabled_locations", "misc_hints"]
  raw_options = __extract_section(raw_override_file, "options")
  for opt, value in raw_options.items():
    if opt == "conditionals":
      for deepopt, deepval in value.items():
        override[deepopt] = deepval

    elif not (opt.startswith("extra_") or opt.startswith("remove_")):
      override[opt] = value

    # Handle extra_ and remove_ Refactor once refactor RSL script overrides. Conditionals dont have to be extra_ or remove_
    else:
      baseopt = "_".join(opt.split("_")[1:])
      if baseopt in list_options:
        baseval = summary["global_settings"][baseopt]
        if opt.startswith("extra_"):
          override[baseopt] = baseval + [ x for x in value if x not in baseval ]
        else:
          override[baseopt] = [ x for x in baseval if x not in value ]
      else:
        for deepopt, deepval in value.items():
          override[deepopt] = deepval

  # Parse overrides for weights
  raw_weights = __extract_section(raw_override_file, "weights")
  override.update(raw_weights)
  raw_multiselect = __extract_section(raw_override_file, "multiselect")
  override.update(raw_multiselect)
  summary["overrides"][override_name] = override


def fetch_rsl_weights():
  raw_weights = _fetch_rsl_file("weights/rsl_season6.json")
  output = _parse_raw_rsl_weights(raw_weights)
  _attach_override("beginner", output)
  _attach_override("intermediate", output)
  with open(_rsl_weights_path, 'w') as fpointer:
    json.dump(output, fpointer)


fetch_rsl_weights()
