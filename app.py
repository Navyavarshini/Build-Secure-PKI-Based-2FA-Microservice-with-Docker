import os
import base64
import pyotp
from fastapi import FastAPI, HTTPException
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

app = FastAPI()

with open("student_private.pem","rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), None)

DATA_PATH = "/data/seed.txt"

@app.post("/decrypt-seed")
async def decrypt_seed(encrypted_seed: dict):
    try:
        raw = base64.b64decode(encrypted_seed["encrypted_seed"])
        seed = private_key.decrypt(
            raw,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()

        if len(seed) != 64:
            raise Exception("Invalid seed length")

        os.makedirs("/data", exist_ok=True)
        with open(DATA_PATH,"w") as f:
            f.write(seed)

        return {"status": "ok"}

    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.get("/generate-2fa")
async def generate_2fa():
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    seed = open(DATA_PATH).read().strip()
    b32 = base64.b32encode(bytes.fromhex(seed)).decode()
    totp = pyotp.TOTP(b32)

    import time  

    remaining = totp.interval - (time.time() % totp.interval)


    return {
        "code": totp.now(),
        "valid_for": int(remaining)
    }

@app.post("/verify-2fa")
async def verify_2fa(data: dict):
    if "code" not in data:
        raise HTTPException(status_code=400, detail="Missing code")

    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    seed = open(DATA_PATH).read().strip()
    b32 = base64.b32encode(bytes.fromhex(seed)).decode()
    totp = pyotp.TOTP(b32)

    return {"valid": totp.verify(data["code"], valid_window=1)}

