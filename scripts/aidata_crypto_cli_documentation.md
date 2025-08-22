# AIDATA CRYPTO CLI TOOL DOCUMENTATION

This document provides detailed information about the `aidata_crypto_cli.py` script, which is designed to provide encryption and decryption utilities for `.aidata` files.

## Overview

The `aidata_crypto_cli.py` script implements a command-line interface for encrypting and decrypting `.aidata` files using AES-256 encryption. It provides functionalities for:
- Encrypting files with a password or key file
- Decrypting files with a password or key file
- Generating new encryption keys

This tool is part of the broader AI learning ecosystem that works with `.aidata` files and enhances their security as described in the `base.aidata` Security and Privacy Framework.

## Installation and Setup

The script is located in the `C:\ai_learnings` directory as `aidata_crypto_cli.py`. To use it, you need to have Python installed on your system along with the required dependencies:
- `cryptography` library

Install the dependencies with:
```bash
pip install cryptography
```

## Usage

The script is designed to be run from the command line with different commands:

```bash
python C:\ai_learnings\aidata_crypto_cli.py [command] [options]
```

### Available Commands

1. **encrypt**: Encrypt a file using AES-256
2. **decrypt**: Decrypt a file using AES-256
3. **generate-key**: Generate a new encryption key

## Command Details

### Encrypt Command
Encrypts a file using AES-256 encryption.

```bash
python C:\ai_learnings\aidata_crypto_cli.py encrypt [input_file] [options]
```

#### Options
- `-o`, `--output`: Output file (default: input_file.enc)
- `-p`, `--password`: Password for encryption
- `-k`, `--key-file`: Key file for encryption

#### Examples
```bash
# Encrypt a file with a password
python C:\ai_learnings\aidata_crypto_cli.py encrypt sensitive_section.md -p mysecretpassword

# Encrypt a file with a key file
python C:\ai_learnings\aidata_crypto_cli.py encrypt sensitive_section.md -k mykey.key
```

### Decrypt Command
Decrypts a file using AES-256 encryption.

```bash
python C:\ai_learnings\aidata_crypto_cli.py decrypt [input_file] [options]
```

#### Options
- `-o`, `--output`: Output file (default: input_file without .enc)
- `-p`, `--password`: Password for decryption
- `-k`, `--key-file`: Key file for decryption

#### Examples
```bash
# Decrypt a file with a password
python C:\ai_learnings\aidata_crypto_cli.py decrypt sensitive_section.enc -p mysecretpassword

# Decrypt a file with a key file
python C:\ai_learnings\aidata_crypto_cli.py decrypt sensitive_section.enc -k mykey.key
```

### Generate Key Command
Generates a new AES-256 encryption key.

```bash
python C:\ai_learnings\aidata_crypto_cli.py generate-key [options]
```

#### Options
- `-o`, `--output`: Output file for the key (default: prints to console)

#### Examples
```bash
# Generate a key and print to console
python C:\ai_learnings\aidata_crypto_cli.py generate-key

# Generate a key and save to file
python C:\ai_learnings\aidata_crypto_cli.py generate-key -o mykey.key
```

## AIDataCryptoCLI Class

The core functionality is implemented in the `AIDataCryptoCLI` class.

### Constructor
```python
crypto_cli = AIDataCryptoCLI()
```

### Key Methods
- `generate_key(key_file=None)`: Generate a new AES-256 encryption key
- `encrypt_file(input_file, output_file=None, password=None, key_file=None)`: Encrypt a file using AES-256
- `decrypt_file(input_file, output_file=None, password=None, key_file=None)`: Decrypt a file using AES-256

## Security Features

### AES-256 Encryption
The tool uses AES-256 encryption, which is a strong symmetric encryption algorithm:
- 256-bit key size
- CBC mode with random IV
- PKCS7 padding

### Key Management
The tool supports two methods for key management:
1. **Password-based encryption**: Uses PBKDF2 to derive a key from a password
2. **Key file encryption**: Uses a randomly generated 32-byte key stored in a file

### Salt and IV Generation
When using password-based encryption:
- A random 16-byte salt is generated for each encryption
- A random 16-byte IV (Initialization Vector) is generated for each encryption
- The salt and IV are stored with the ciphertext to enable decryption

## Integration with .aidata Ecosystem

This tool is part of the broader `.aidata` ecosystem and works alongside:
- `aidata_cli.py`: For command-line processing of files
- Session management tools like `qwen_session_manager.py`
- The security framework described in `base.aidata`

The crypto CLI tool directly implements the encryption/decryption capabilities described in the "Encryption/Decryption CLI Tool" section of `base.aidata`.

## Error Handling

The tool includes error handling for:
- File not found errors
- Permission errors
- Invalid key sizes
- General exceptions during encryption/decryption
- Missing required parameters

If an error occurs, the tool will display an informative error message.

## Cross-Platform Compatibility

The tool is designed to work on Windows, Linux, and macOS. When using it on different platforms, ensure that:
- Python 3 is installed
- The `cryptography` library is installed
- The file paths use appropriate separators for the platform

## Relationship to Base Specification

This tool implements the encryption capabilities described in the `base.aidata` file:
1. **Example Encryption Commands**: The tool provides a programmatic implementation of the example OpenSSL commands
2. **CLI Tool Integration**: It's a dedicated CLI tool for encryption/decryption as recommended
3. **Security Framework Support**: It supports the security framework described in the SPECIFICATIONS section

For the most up-to-date information about `.aidata` file specifications, refer to the `base.aidata` file in the same directory.