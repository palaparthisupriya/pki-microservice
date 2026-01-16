import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_seed(encrypted_seed_b64: str, private_key_path: str) -> str:
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    
    ciphertext = base64.b64decode(encrypted_seed_b64)
    decrypted_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_bytes.decode('utf-8').strip()