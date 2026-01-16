import os
from datetime import datetime
from app.totp_utils import generate_totp

SEED_FILE = "/data/seed.txt"
LOG_FILE = "/cron/last_code.txt"

def run_cron_task():
    if not os.path.exists(SEED_FILE):
        return
    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()
    
    code, _ = generate_totp(hex_seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} 2FA Code: {code}\n")