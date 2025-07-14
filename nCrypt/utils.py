

# python -i C:\Users\swisn\OneDrive\Desktop\Portal\nCrypt\nCrypt\utils.py

import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def ncrypt(passphrase, data, iterations=1000):
    """Single round AES-256 encryption with PBKDF2 key derivation"""
    # Convert string input to bytes
    passphrase = _convert_str_to_bytes(passphrase)
    data = _convert_str_to_bytes(data)
    
    # Generate salt and derive key from passphrase
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 32 bytes = 256 bits for AES-256
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(passphrase)
    
    # Encrypt using AES-256-CBC
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    padder = padding.PKCS7(128).padder()
    encryptor = cipher.encryptor()
    padded_data = padder.update(data) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Combine salt + iv + ciphertext and encode as base64
    encrypted_data = salt + iv + ciphertext
    return base64.b64encode(encrypted_data).decode('utf-8')

def dencrypt(passphrase, encrypted_data, iterations=1000):
    """Single round AES-256 decryption"""
    # Convert string input to bytes
    passphrase = _convert_str_to_bytes(passphrase)
    
    # Decode from base64
    try:
        encrypted_bytes = base64.b64decode(encrypted_data)
    except Exception:
        raise ValueError("Invalid base64 encoded data")
    
    # Extract salt (first 16 bytes), IV (next 16 bytes), and ciphertext (rest)
    if len(encrypted_bytes) < 32:
        raise ValueError("Encrypted data too short")
        
    salt = encrypted_bytes[:16]
    iv = encrypted_bytes[16:32]
    ciphertext = encrypted_bytes[32:]
    
    # Validate ciphertext length (must be multiple of 16)
    if len(ciphertext) % 16 != 0:
        raise ValueError("Invalid ciphertext length")
    
    # Derive key from passphrase using the extracted salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    key = kdf.derive(passphrase)
    
    # Decrypt using AES-256-CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    
    return data.decode('utf-8')

def _convert_str_to_bytes(val):
    """Converts string input to bytes"""
    if isinstance(val, str):
        return val.encode('utf-8')
    return val
