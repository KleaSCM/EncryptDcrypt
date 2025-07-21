#!/usr/bin/env python3
"""
🔑 Simple Key Generation Script 🔑
==================================

A simple script to generate encryption keys without GUI dependencies.
Built with love by Yuriko! 💕
"""

from cryptography.fernet import Fernet
import os

def generate_key():
    """Generate a new encryption key and save it to key.txt."""
    print("🔑 Generating new encryption key...")
    
    # Generate a new key using Fernet's secure key generation
    key = Fernet.generate_key()
    
    # Save the key to key.txt
    with open("key.txt", "wb") as key_file:
        key_file.write(key)
    
    print("✅ Key generated and saved to key.txt")
    print("🔐 Your encryption system is now ready to use!")
    
    return key

if __name__ == "__main__":
    try:
        generate_key()
    except Exception as e:
        print(f"❌ Error generating key: {e}")
        exit(1) 