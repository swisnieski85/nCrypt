
# Copyright (c) 2025 Sean Wisnieski
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import base64
import struct
import webbrowser

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from crypto_backend import encrypt as _enc, dencrypt as _dec
from typing import Union

def ncrypt(passphrase: str, data: str, iterations: int = 200_000) -> str:
    return _enc(passphrase, data, iterations)

def dencrypt(passphrase: str, encrypted_payload: str) -> str:
    return _dec(passphrase, encrypted_payload)

def open_browser():
    # Opens browser window
    webbrowser.open_new('http://127.0.0.1:5000/')

def _to_bytes(val: Union[str, bytes]) -> bytes:
    return val.encode("utf-8") if isinstance(val, str) else val

def _derive_key(passphrase: bytes, salt: bytes, iterations: int) -> bytes:
    """Derive a 32‑byte key with PBKDF2‑HMAC‑SHA‑256."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    )
    return kdf.derive(passphrase)
