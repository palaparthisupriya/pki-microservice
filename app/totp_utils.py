import base64
import pyotp
import time

def generate_totp(hex_seed: str):
    # Convert hex to bytes, then to base32 for pyotp
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed)
    return totp.now(), 30 - (int(time.time()) % 30)

def verify_totp(hex_seed: str, code: str):
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed)
    return totp.verify(code, valid_window=1)