
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

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


def derive_key(passphrase: bytes, salt: bytes, iterations: int) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    )
    return kdf.derive(passphrase)

def encrypt(passphrase: str, plaintext: str, iterations: int = 310_000) -> str:
    p_bytes = plaintext.encode()
    pass_bytes = passphrase.encode()

    salt = os.urandom(16)
    iv   = os.urandom(12)
    key  = derive_key(pass_bytes, salt, iterations)

    encryptor = Cipher(
        algorithms.AES(key), modes.GCM(iv), backend=default_backend()
    ).encryptor()

    ct = encryptor.update(p_bytes) + encryptor.finalize()
    tag = encryptor.tag

    payload = (
        struct.pack(">I", iterations) + salt + iv + ct + tag
    )
    return base64.b64encode(payload).decode()

def dencrypt(passphrase: str, b64_payload: str) -> str:
    data = base64.b64decode(b64_payload)
    iterations = struct.unpack(">I", data[:4])[0]
    salt = data[4:20]
    iv   = data[20:32]
    tag  = data[-16:]
    ct   = data[32:-16]

    key = derive_key(passphrase.encode(), salt, iterations)
    decryptor = Cipher(
        algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend()
    ).decryptor()

    pt = decryptor.update(ct) + decryptor.finalize()
    return pt.decode()
