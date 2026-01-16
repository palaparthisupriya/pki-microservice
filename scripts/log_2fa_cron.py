import sys
import os

# Ensure the app folder is in the python path
sys.path.append('/app')

from app.cron_job import run_cron_task

if __name__ == "__main__":
    try:
        run_cron_task()
        print("Cron task executed successfully")
    except Exception as e:
        print(f"Error: {e}")