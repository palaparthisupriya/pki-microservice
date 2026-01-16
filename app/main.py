import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.crypto_utils import decrypt_seed
from app.totp_utils import generate_totp, verify_totp

app = FastAPI(title="Secure PKI-TOTP Microservice")

# Paths defined by Docker Volume requirements
SEED_FILE = "/data/seed.txt"
PRIVATE_KEY_PATH = "student_private.pem"

# Pydantic models for request validation
class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

@app.get("/")
async def root():
    return {"message": "Auth Microservice is running"}

@app.post("/decrypt-seed")
async def api_decrypt(payload: DecryptRequest):
    """
    POST/decrypt-seed: 
    Accepts base64 encrypted seed, decrypts via RSA/OAEP-SHA256,
    and stores it persistently at /data/seed.txt.
    """
    try:
        # Step 1: Decrypt using utility
        hex_seed = decrypt_seed(payload.encrypted_seed, PRIVATE_KEY_PATH)
        
        # Step 2: Ensure persistent directory exists
        os.makedirs(os.path.dirname(SEED_FILE), exist_ok=True)
        
        # Step 3: Save seed to volume
        with open(SEED_FILE, "w") as f:
            f.write(hex_seed)
            
        return {"status": "ok"}
    except Exception as e:
        print(f"Decryption Error: {e}")
        # Requirements specify HTTP 500 on failure
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.get("/generate-2fa")
async def api_generate():
    """
    GET/generate-2fa:
    Reads stored seed and returns a 6-digit TOTP code and its validity.
    """
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    
    try:
        with open(SEED_FILE, "r") as f:
            hex_seed = f.read().strip()
        
        # Generate TOTP using utility
        code, valid_for = generate_totp(hex_seed)
        
        return {"code": code, "valid_for": valid_for}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify-2fa")
async def api_verify(payload: VerifyRequest):
    """
    POST/verify-2fa:
    Verifies a 6-digit code against the stored seed with ±1 period tolerance.
    """
    if not payload.code:
        raise HTTPException(status_code=400, detail="Missing code")
        
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    
    try:
        with open(SEED_FILE, "r") as f:
            hex_seed = f.read().strip()
        
        # Verify using utility (handles ±30s window)
        is_valid = verify_totp(hex_seed, payload.code)
        
        return {"valid": is_valid}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Verification error")

if __name__ == "__main__":
    import uvicorn
    # Runs on port 8080 as per Docker configuration
    uvicorn.run(app, host="0.0.0.0", port=8080)