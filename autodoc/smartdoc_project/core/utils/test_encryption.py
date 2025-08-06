from encryption import encrypt_text, decrypt_text

# Sample plain text
original_text = "This is a secret message."

# Encrypt
encrypted = encrypt_text(original_text)
print("Encrypted Bytes:", encrypted)

# Decrypt
decrypted = decrypt_text(encrypted)
print("Decrypted Text:", decrypted)
