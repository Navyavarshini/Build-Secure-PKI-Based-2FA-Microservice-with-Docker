import base64, pyotp
from datetime import datetime
import os

seed_path = "/data/seed.txt"
if os.path.exists(seed_path):
    seed = open(seed_path).read().strip()
    b32 = base64.b32encode(bytes.fromhex(seed)).decode()
    totp = pyotp.TOTP(b32)
    code = totp.now()
    print(f"{datetime.utcnow()} - 2FA Code: {code}")
