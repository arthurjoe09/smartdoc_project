from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from pathlib import Path

# Define key directory path
KEY_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent / "rsa_keys"
KEY_DIR.mkdir(exist_ok=True)  # create rsa_keys/ if not present

PRIVATE_KEY_PATH = KEY_DIR / "private.pem"
PUBLIC_KEY_PATH = KEY_DIR / "public.pem"

def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048  # You can also use 4096 for higher security
    )

    # Store private key
    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Store public key
    public_key = private_key.public_key()
    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )



