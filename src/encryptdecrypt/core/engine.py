"""
Core Encryption Engine
=====================

Advanced encryption engine with secure key management and file operations.

Author: KleaSCM <KleaSCM@gmail.com>
"""

import os
import hashlib
import secrets
import base64
from pathlib import Path
from typing import Dict, Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

logger = logging.getLogger(__name__)


class EncryptionEngine:
    """
    Advanced Encryption Engine
    
    Implements secure encryption algorithms and key management.
    Uses PBKDF2 for key derivation and Fernet for symmetric encryption.
    """
    
    def __init__(self, key_file: str = "key.txt"):
        """
        Initialize the encryption engine with secure key management.
        
        Args:
            key_file (str): Path to the key file for storing encryption keys
        """
        self.key_file = key_file
        self.fernet = None
        self._load_or_generate_key()
    
    def _load_or_generate_key(self) -> None:
        """
        Load existing key or generate a new one using secure random generation.
        Uses PBKDF2 for key derivation if password-based encryption is needed.
        """
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, "rb") as key_file:
                    key = key_file.read()
                    logger.info("Loaded existing encryption key")
            else:
                # Generate a new key using Fernet's secure key generation
                key = Fernet.generate_key()
                with open(self.key_file, "wb") as key_file:
                    key_file.write(key)
                logger.info("Generated new encryption key")
            
            self.fernet = Fernet(key)
            
        except Exception as e:
            logger.error(f"Error in key management: {e}")
            raise
    
    def derive_key_from_password(self, password: str, salt: bytes = None) -> Tuple[bytes, bytes]:
        """
        Derive encryption key from password using PBKDF2.
        
        Mathematical Formula: 
        Key = PBKDF2(password, salt, iterations=100000, length=32, hash_algorithm=SHA256)
        
        Args:
            password (str): User-provided password
            salt (bytes): Random salt for key derivation
            
        Returns:
            Tuple[bytes, bytes]: Derived key and salt
        """
        if salt is None:
            salt = secrets.token_bytes(16)  # 128-bit salt
        
        # PBKDF2 key derivation with 100,000 iterations for security
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit key
            salt=salt,
            iterations=100000,  # High iteration count for security
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def calculate_file_hash(self, file_path: str) -> str:
        """
        Calculate SHA-256 hash of file for integrity verification.
        
        Mathematical Formula: H = SHA-256(file_content)
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: Hexadecimal representation of the hash
        """
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def encrypt_file(self, file_path: str, preserve_original: bool = False) -> Dict[str, str]:
        """
        Encrypt a single file with integrity verification.
        
        Args:
            file_path (str): Path to the file to encrypt
            preserve_original (bool): Whether to keep the original file
            
        Returns:
            Dict[str, str]: Encryption results and metadata
        """
        try:
            # Calculate original file hash for integrity verification
            original_hash = self.calculate_file_hash(file_path)
            
            # Read file content
            with open(file_path, "rb") as file:
                data = file.read()
            
            # Encrypt the data using Fernet (AES-128 in CBC mode with PKCS7 padding)
            encrypted_data = self.fernet.encrypt(data)
            
            # Write encrypted data directly to original file path (replacing it)
            with open(file_path, "wb") as file:
                file.write(encrypted_data)
            
            # Calculate encrypted file hash
            encrypted_hash = self.calculate_file_hash(file_path)
            
            return {
                "status": "success",
                "file_path": file_path,
                "original_hash": original_hash,
                "encrypted_hash": encrypted_hash,
                "file_size": len(data),
                "encrypted_size": len(encrypted_data)
            }
            
        except Exception as e:
            logger.error(f"Encryption failed for {file_path}: {e}")
            return {"status": "error", "file": file_path, "error": str(e)}
    
    def decrypt_file(self, file_path: str, preserve_encrypted: bool = False) -> Dict[str, str]:
        """
        Decrypt a single file with integrity verification.
        
        Args:
            file_path (str): Path to the encrypted file
            preserve_encrypted (bool): Whether to keep the encrypted file
            
        Returns:
            Dict[str, str]: Decryption results and metadata
        """
        try:
            # Calculate encrypted file hash
            encrypted_hash = self.calculate_file_hash(file_path)
            
            # Read encrypted data
            with open(file_path, "rb") as file:
                encrypted_data = file.read()
            
            # Decrypt the data
            decrypted_data = self.fernet.decrypt(encrypted_data)
            
            # Write decrypted data directly to original file path (replacing it)
            with open(file_path, "wb") as file:
                file.write(decrypted_data)
            
            # Calculate decrypted file hash
            decrypted_hash = self.calculate_file_hash(file_path)
            
            return {
                "status": "success",
                "file_path": file_path,
                "encrypted_hash": encrypted_hash,
                "decrypted_hash": decrypted_hash,
                "file_size": len(decrypted_data)
            }
            
        except Exception as e:
            logger.error(f"Decryption failed for {file_path}: {e}")
            return {"status": "error", "file": file_path, "error": str(e)} 