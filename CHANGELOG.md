# Changelog

All notable changes to the nCrypt project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This project adheres to [Semantic Versioning](https://semver.org/).


## [1.2.1] - 2025-07-18
### Added
- Added `config.yaml` for static parameters, currently containing only KDF iteration bounds.

### Changed
- KDF iteration clamping now respects values from `config.yaml`.
- Updated default KDF iteration count to 310,000 (per OWASP recommendation).
- Increased maximum allowed iterations to 50 million.\
- Minor revisions to README.md.


## [1.2.0] - 2025-07-16
### Added
- Encrypted payloads now include a version byte and embedded PBKDF2 iteration count, enabling self-contained decryption metadata.
- App secret key generation.
- CSRF protection added to all forms using `Flask-WTF`.

### Changed
- Refactored to move cryptographic primitives behind a dedicated module (crypto_backend.py).
- Added MIT license headers to all source code files.
- Replaced AES-256-CBC with AES-256-GCM for authenticated encryption (AEAD).
- Increased base PBKDF2 iteration count from 1,000 to 200,000.
- Refactored `ncrypt()` and `dencrypt()` functions to reflect new encryption scheme and internalized iteration metadata.
- Updated Flask view logic (`encrypt` and `decrypt` routes) to align with cryptographic changes and improve exception handling.
- `decrypt.html` UI simplified by removing iteration input field (decryption now derives this value from the ciphertext itself).
- Clamped number of iterations to between 100,000 and 5 million.
- Updated README.md appropriately.

### Fixed
- Improved error messaging.
- Unneeded comments removed throughout.


## [1.1.0] - 2025-07-15
### Added
- Status messages for encryption/decryption operations.


## [1.0.1] - 2025-07-14
### Added
- Added MIT LICENSE.

### Changed
- Updated README.md.


## [1.0.0] - 2025-07-14
### Added
- Initial release of nCrypt web application.
