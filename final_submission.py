import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

COMMIT_HASH = "PASTE_YOUR_HASH_HERE"

with open("student_private.pem", "rb") as f:
    priv_key = serialization.load_pem_private_key(f.read(), password=None)
with open("instructor_public.pem", "rb") as f:
    inst_pub = serialization.load_pem_public_key(f.read())

# RSA-PSS Signature
sig = priv_key.sign(
    COMMIT_HASH.encode(),
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)
# RSA-OAEP Encryption
proof = inst_pub.encrypt(
    sig,
    padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)
print(base64.b64encode(proof).decode())