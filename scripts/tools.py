import os


def safe_file_delete(file_path):
    if os.path.exists(file_path):
        print(f"rm {file_path}")
        os.remove(file_path)