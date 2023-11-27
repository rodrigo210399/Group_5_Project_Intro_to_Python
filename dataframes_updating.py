import time
import subprocess
from datetime import datetime, timedelta
import pytz

def job():
    print("Running your program...")
    subprocess.run(['python', 'data_to_dataframes.py'], capture_output=True, text=True)
    print("Result for data_to_dataframes.py")

    subprocess.run(['python', 'dataframes_to_database.py'], capture_output=True, text=True)
    print("Result for dataframes_to_database.py")

# Set the time zone to Eastern Time (Toronto/Windsor)
ontario_timezone = pytz.timezone("America/Toronto")

# Define the start and end times in Ontario time zone
today = datetime.now(ontario_timezone).replace(hour=0, minute=0, second=0, microsecond=0)
start_time = today + timedelta(hours=10)
end_time = today + timedelta(hours=16)

while True:
    current_time = datetime.now(ontario_timezone)

    # Check if the current time is within the specified time range
    print(f"Current time: {current_time}")
    if start_time <= current_time <= end_time:
        print("Within the specified time range. Running jobs...")
        job()
    else:
        print("The Stock Market is closed.")

    # Sleep for 2 minutes before checking again
    time.sleep(120)
