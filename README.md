# nCrypt

A Flask-based local web application for securely encrypting and decrypting sensitive text using modern cryptography. Designed for users who want to store passwords or other secrets encrypted locally with a custom passphrase and a user-defined security strength.

## Features

- **AES-256-GCM Encryption**: Authenticated symmetric encryption (secure and tamper-proof)
- **PBKDF2-SHA256 Key Derivation**: Key generation with user-defined iteration strength
- **All-In-One Payload**: Salt, IV, iteration count, and ciphertext stored together
- **Web Interface**: Clean, dark-themed UI with separate encrypt/decrypt pages
- **Auto-launch**: Automatically opens in your browser when you run the app
- **Clipboard Support**: One-click copy for encrypted/decrypted results
- **Base64 Encoding**: Output is safe for storage in plain-text files

## Screenshots

*(Add screenshots here if desired)*

## Installation

### Prerequisites
- Python 3.7+
- `pip` (Python package manager)

### Dependencies

Install dependencies with:

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:

```
Flask==3.1.1
cryptography==45.0.5
```

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/swisnieski85/nCrypt
   cd nCrypt
   ```

2. Run the app:
   ```bash
   python app.py
   ```

3. Your browser will automatically open to `http://localhost:5000`. If it doesn't, open a browser tab and paste in `http://localhost:5000` manually, then hit Enter.

## Usage

### Encrypt

1. Navigate to the **Encrypt** page
2. Enter your secret passphrase
3. Choose a key derivation strength (default: 200,000 iterations; range between 100,000 and 5,000,000)
4. Enter the text to encrypt
5. Click **ENCRYPT**
6. Copy the resulting encrypted text for storage

### Decrypt

1. Navigate to the **Decrypt** page
2. Enter the passphrase used for encryption (it is not necessary to enter the iteration count again; this is stored with the encrypted text)
3. Paste the encrypted text
4. Click **DECRYPT**
5. Copy the decrypted result

**Note**: You no longer need to specify the iteration count when decrypting. It's stored in the encrypted payload itself.

## Technical Details

### Encryption Overview

- **Algorithm**: AES-256 in GCM mode (provides integrity and confidentiality)
- **Key Derivation**: PBKDF2 with SHA-256
- **Salt**: 16 bytes, randomly generated per encryption
- **IV (Nonce)**: 12 bytes, randomly generated per encryption
- **Iterations**: 4-byte integer prepended to payload (default: 200,000)
- **Output**: Base64-encoded string of `[iterations][salt][iv][ciphertext][tag]`

### Payload Structure

```
[4-byte iteration count] +
[16-byte salt] +
[12-byte IV] +
[variable ciphertext] +
[16-byte GCM tag]
```

This design enables the decryption function to derive everything it needs from the input ciphertext, except for the passphrase.

## File Structure

```
nCrypt/
├── app.py              # Flask application logic
├── utils.py            # Cryptographic functions
├── templates/
│   ├── encrypt.html    # Encrypt page
│   └── decrypt.html    # Decrypt page
├── static/
│   ├── styles.css      # App styling
│   └── nCrypt-logo.png # Logo
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Security Considerations

- Use **strong, unique** passphrases
- Higher iteration counts improve brute-force resistance (default: 200k)
- Keep the passphrase secret; encryption is only as strong as the key
- This app performs **local** encryption only (data never leaves your machine)
- In production, consider running under HTTPS and using environment-based secrets

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file.

## Contributing

Pull requests are welcome!

1. Fork the repo
2. Create a feature branch (`git checkout -b my-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to your fork (`git push origin my-feature`)
5. Open a pull request

## Support

If you encounter an issue or want to suggest improvements:

- Open an [Issue](https://github.com/swisnieski85/nCrypt/issues)
- For sensitive questions, contact directly instead of posting publicly (you may e-mail me at the non-numeric portion of my username at gmail.com)

**Note**: This project is educational in nature. While the cryptographic implementation follows best practices, any use in real-world secure systems should be reviewed and audited appropriately.
