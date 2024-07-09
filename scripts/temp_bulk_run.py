import subprocess
import time

def run_fetch_google(*args):
    command = ["python3", "fetch_google.py", *args]
    subprocess.run(command)

run_fetch_google("-n", "1", "--date", "2023-05-10")
run_fetch_google("-n", "2", "--date", "2023-05-17")
run_fetch_google("-n", "3", "--date", "2023-05-24")
run_fetch_google("-n", "4", "--date", "2023-05-31")
run_fetch_google("-n", "5", "--date", "2023-06-07")
run_fetch_google("-n", "6", "--date", "2023-06-14")
run_fetch_google("-n", "7", "--date", "2023-06-21")
run_fetch_google("-n", "8", "--date", "2023-06-28")
run_fetch_google("-n", "9", "--date", "2023-07-05")
run_fetch_google("-n", "10","--date", "2023-07-12")
run_fetch_google("-n", "11","--date", "2023-07-19")