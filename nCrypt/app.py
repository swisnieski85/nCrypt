
# C:\Users\swisn\OneDrive\Desktop\Portal\nCrypt\nCrypt\app.py

from flask import Flask, render_template, url_for, redirect, request
from utils import ncrypt, dencrypt

app = Flask(__name__)

@app.route("/")
def home():
    # default page
    return redirect(url_for("encrypt"))

@app.route("/encrypt", methods=['GET', 'POST'])
def encrypt():
    # encryption page - POST
    if request.method == 'POST':
        # Get form data
        passphrase = request.form.get('passphrase')
        plaintext = request.form.get('plaintext')
        iterations = int(request.form.get('iterations', 1))
        
        # Encrypt the data
        try:
            encrypted_result = ncrypt(passphrase, plaintext, iterations)
            return render_template("encrypt.html", page="encrypt", 
                                 passphrase=passphrase, 
                                 plaintext=plaintext, 
                                 iterations=iterations,
                                 ciphertext=encrypted_result,
                                 status_message="Encryption completed successfully!",
                                 status_type="success")
        except Exception as e:
            error_message = f"Encryption failed: {str(e)}"
            return render_template("encrypt.html", page="encrypt", 
                                 status_message=error_message,
                                 status_type="error")
    
    # encryption page - GET
    return render_template("encrypt.html", page="encrypt")

@app.route("/decrypt", methods=['GET', 'POST'])
def decrypt():    
    if request.method == 'POST':
        try:
            # Get form data
            passphrase = request.form.get('passphrase')
            ciphertext = request.form.get('ciphertext')
            iterations = int(request.form.get('iterations', 1))
            
            # Decrypt the data
            decrypted_result = dencrypt(passphrase, ciphertext, iterations)
            return render_template("decrypt.html", page="decrypt", 
                                 passphrase=passphrase, 
                                 ciphertext=ciphertext, 
                                 iterations=iterations,
                                 plaintext=decrypted_result,
                                 status_message="Decryption completed successfully!",
                                 status_type="success")
        
        except ValueError:
            error_message = "Invalid passphrase or number of iterations."
            return render_template("decrypt.html", page="decrypt", 
                                 status_message=error_message,
                                 status_type="error")
        
        except:
            error_message = f"Decryption failed: {str(e)}"
            return render_template("decrypt.html", page="decrypt", 
                                 status_message=error_message,
                                 status_type="error")
    
    # GET request - just show the form
    return render_template("decrypt.html", page="decrypt")

if __name__ == "__main__":
    app.run(debug=True)
