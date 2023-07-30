import os


def safe_file_delete(file_path):
    if os.path.exists(file_path):
        print(f"rm {file_path}")
        os.remove(file_path)


def convert_duration_ISO8601(duration):
    """ Format of parameter should be H:M:S separated by colons any number of digits. 
    No support for units more than H
    """
    isobase = "P0DT{}H{}M{}S"
    duration = duration.split(":")
    if len(duration) < 2:
        duration = [0,0] + duration
    elif len(duration) < 3:
        duration = [0] + duration
    elif len(duration) > 3:
        print(f"Duration {duration} not valid!")
    iso = isobase.format(duration[0], duration[1], duration[2])
    return iso