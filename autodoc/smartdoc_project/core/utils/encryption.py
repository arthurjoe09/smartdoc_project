from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from pathlib import Path

# Define key directory and paths
KEY_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent / "rsa_keys"
PRIVATE_KEY_PATH = KEY_DIR / "private.pem"
PUBLIC_KEY_PATH = KEY_DIR / "public.pem"

def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as key_file:
        return serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

def encrypt_text(text: str) -> bytes:
    public_key = load_public_key()
    encrypted = public_key.encrypt(
        text.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def decrypt_text(encrypted_data: bytes) -> str:
    private_key = load_private_key()
    decrypted = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode("utf-8")
