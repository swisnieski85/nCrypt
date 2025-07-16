
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
import threading
import secrets

from flask import Flask, render_template, url_for, redirect, request
from flask_wtf import CSRFProtect
from utils import ncrypt, dencrypt, open_browser

app = Flask(__name__)
app.secret_key = secrets.token_hex(64)
csrf = CSRFProtect(app)

@app.route("/")
def home():
    # default page
    return redirect(url_for("encrypt"))

@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    if request.method == "POST":
        # POST
        passphrase   = request.form.get("passphrase", "")
        plaintext    = request.form.get("plaintext", "")
        iterations   = int(request.form.get("iterations", 200_000))
        
        try:
            # clamp iterations defensively
            iterations = max(1, min(iterations, 2_000_000))
            ciphertext = ncrypt(passphrase, plaintext, iterations)
            return render_template(
                "encrypt.html",
                page="encrypt",
                passphrase=passphrase,
                plaintext=plaintext,
                iterations=iterations,
                ciphertext=ciphertext,
                status_message="Encryption completed successfully!",
                status_type="success",
            )
        except Exception as err:
            return render_template(
                "encrypt.html",
                page="encrypt",
                status_message=f"Encryption failed: {err}",
                status_type="error",
            )
    
    # GET
    return render_template("encrypt.html", page="encrypt")

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    if request.method == "POST":
        passphrase = request.form.get("passphrase", "")
        ciphertext = request.form.get("ciphertext", "")
        
        try:
            plaintext = dencrypt(passphrase, ciphertext)
            return render_template(
                "decrypt.html",
                page="decrypt",
                passphrase=passphrase,
                ciphertext=ciphertext,
                plaintext=plaintext,
                status_message="Decryption completed successfully!",
                status_type="success",
            )
        except ValueError as err:
            # expected problems: bad base64, auth tag failure, etc.
            return render_template(
                "decrypt.html",
                page="decrypt",
                status_message=str(err),
                status_type="error",
            )
        except Exception as err:
            # anything else bubbles up here
            return render_template(
                "decrypt.html",
                page="decrypt",
                status_message=f"Decryption failed: {err}",
                status_type="error",
            )
    
    # GET
    return render_template("decrypt.html", page="decrypt")

if __name__ == "__main__":
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        threading.Timer(1, open_browser).start()
    
    app.run()
