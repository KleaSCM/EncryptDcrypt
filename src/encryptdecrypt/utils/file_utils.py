"""
File utility functions for the encryption system.

Author: KleaSCM <KleaSCM@gmail.com>
"""

import base64


def is_encrypted_file(file_path: str) -> bool:
    """
    Check if a file is encrypted by checking for Fernet token format.
    
    Args:
        file_path (str): Path to the file to check
        
    Returns:
        bool: True if file appears to be encrypted, False otherwise
    """
    try:
        with open(file_path, "rb") as file:
            # Read first 100 bytes to check format
            data = file.read(100)
            if len(data) < 44:  # Fernet token minimum size
                return False
            
            # Check if it starts with Fernet token format (base64 with specific pattern)
            # Fernet tokens start with specific base64 characters and have a specific structure
            if data.startswith(b'gAAAAA'):  # Common Fernet token start
                return True
            
            # More strict check: try to decode as base64 and verify Fernet structure
            try:
                # Only check if the data looks like base64 (contains mostly base64 chars)
                base64_chars = set(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_')
                if all(b in base64_chars for b in data[:50]):
                    decoded = base64.urlsafe_b64decode(data)
                    # Fernet tokens have a specific structure (version + timestamp + IV + ciphertext + HMAC)
                    if len(decoded) >= 32:  # Minimum Fernet token size
                        return True
            except:
                pass
            
            return False
    except Exception:
        # If any error occurs, assume it's not encrypted
        return False 