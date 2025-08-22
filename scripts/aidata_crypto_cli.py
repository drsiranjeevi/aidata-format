# AIDATA CRYPTO CLI TOOL
# This script provides encryption and decryption utilities for .aidata files

import argparse
import hashlib
import os
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class AIDataCryptoCLI:
    def __init__(self):
        self.backend = default_backend()
    
    def generate_key(self, key_file=None):
        """Generate a new AES-256 encryption key."""
        # Generate a random 32-byte (256-bit) key
        key = secrets.token_bytes(32)
        
        if key_file:
            # Save the key to a file
            with open(key_file, 'wb') as f:
                f.write(key)
            print(f"Encryption key saved to: {key_file}")
        else:
            # Print the key as hex
            print(f"Generated encryption key: {key.hex()}")
        
        return key
    
    def _derive_key(self, password, salt):
        """Derive a key from a password and salt using PBKDF2."""
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from cryptography.hazmat.primitives import hashes
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(password.encode())
    
    def encrypt_file(self, input_file, output_file=None, password=None, key_file=None):
        """Encrypt a file using AES-256."""
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found.")
            return False
        
        # Determine output file name
        if not output_file:
            output_file = input_file + ".enc"
        
        # Get the encryption key
        if key_file:
            # Load key from file
            if not os.path.exists(key_file):
                print(f"Error: Key file '{key_file}' not found.")
                return False
            
            with open(key_file, 'rb') as f:
                key = f.read()
            
            if len(key) != 32:
                print("Error: Key file must contain exactly 32 bytes for AES-256.")
                return False
        elif password:
            # Derive key from password
            salt = secrets.token_bytes(16)  # Generate a random salt
            key = self._derive_key(password, salt)
        else:
            print("Error: Either a password or key file must be provided for encryption.")
            return False
        
        try:
            # Read the input file
            with open(input_file, 'rb') as f:
                plaintext = f.read()
            
            # Pad the plaintext to be a multiple of 16 bytes (AES block size)
            padder = padding.PKCS7(128).padder()
            padded_plaintext = padder.update(plaintext)
            padded_plaintext += padder.finalize()
            
            # Generate a random IV
            iv = secrets.token_bytes(16)
            
            # Create the cipher and encryptor
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
            encryptor = cipher.encryptor()
            
            # Encrypt the padded plaintext
            ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
            
            # Write the encrypted data to the output file
            # If using a password, we need to store the salt and IV with the ciphertext
            with open(output_file, 'wb') as f:
                if password:
                    # Write salt + IV + ciphertext
                    f.write(salt)
                f.write(iv)
                f.write(ciphertext)
            
            print(f"File encrypted successfully: {output_file}")
            return True
        except Exception as e:
            print(f"Error during encryption: {e}")
            return False
    
    def decrypt_file(self, input_file, output_file=None, password=None, key_file=None):
        """Decrypt a file using AES-256."""
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found.")
            return False
        
        # Determine output file name
        if not output_file:
            if input_file.endswith(".enc"):
                output_file = input_file[:-4]
            else:
                output_file = input_file + ".dec"
        
        # Get the decryption key
        if key_file:
            # Load key from file
            if not os.path.exists(key_file):
                print(f"Error: Key file '{key_file}' not found.")
                return False
            
            with open(key_file, 'rb') as f:
                key = f.read()
            
            if len(key) != 32:
                print("Error: Key file must contain exactly 32 bytes for AES-256.")
                return False
            
            # Read the IV (first 16 bytes after salt if using password)
            with open(input_file, 'rb') as f:
                file_data = f.read()
            
            # For key file encryption, IV is first 16 bytes
            iv = file_data[:16]
            ciphertext = file_data[16:]
        elif password:
            # Read the salt and IV from the file
            with open(input_file, 'rb') as f:
                salt = f.read(16)  # First 16 bytes are the salt
                iv = f.read(16)   # Next 16 bytes are the IV
                ciphertext = f.read()  # The rest is the ciphertext
            
            # Derive key from password and salt
            key = self._derive_key(password, salt)
        else:
            print("Error: Either a password or key file must be provided for decryption.")
            return False
        
        try:
            # Create the cipher and decryptor
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
            decryptor = cipher.decryptor()
            
            # Decrypt the ciphertext
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Remove padding
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(padded_plaintext)
            plaintext += unpadder.finalize()
            
            # Write the decrypted data to the output file
            with open(output_file, 'wb') as f:
                f.write(plaintext)
            
            print(f"File decrypted successfully: {output_file}")
            return True
        except Exception as e:
            print(f"Error during decryption: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Encrypt/Decrypt .aidata files")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a file')
    encrypt_parser.add_argument('input_file', help='Input file to encrypt')
    encrypt_parser.add_argument('-o', '--output', help='Output file (default: input_file.enc)')
    encrypt_parser.add_argument('-p', '--password', help='Password for encryption')
    encrypt_parser.add_argument('-k', '--key-file', help='Key file for encryption')
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt a file')
    decrypt_parser.add_argument('input_file', help='Input file to decrypt')
    decrypt_parser.add_argument('-o', '--output', help='Output file (default: input_file without .enc)')
    decrypt_parser.add_argument('-p', '--password', help='Password for decryption')
    decrypt_parser.add_argument('-k', '--key-file', help='Key file for decryption')
    
    # Generate key command
    keygen_parser = subparsers.add_parser('generate-key', help='Generate a new encryption key')
    keygen_parser.add_argument('-o', '--output', help='Output file for the key (default: prints to console)')
    
    args = parser.parse_args()
    
    crypto_cli = AIDataCryptoCLI()
    
    if args.command == 'encrypt':
        if not args.password and not args.key_file:
            print("Error: Either a password (-p) or key file (-k) must be provided for encryption.")
            return
        
        crypto_cli.encrypt_file(
            args.input_file, 
            args.output, 
            args.password, 
            args.key_file
        )
    elif args.command == 'decrypt':
        if not args.password and not args.key_file:
            print("Error: Either a password (-p) or key file (-k) must be provided for decryption.")
            return
        
        crypto_cli.decrypt_file(
            args.input_file, 
            args.output, 
            args.password, 
            args.key_file
        )
    elif args.command == 'generate-key':
        crypto_cli.generate_key(args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()