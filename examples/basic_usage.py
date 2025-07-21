#!/usr/bin/env python3
"""
Basic Usage Example
==================

Simple example demonstrating how to use the EncryptDecrypt system.
"""

import os
import tempfile
from pathlib import Path

# Add src to path for imports
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from encryptdecrypt.core.engine import EncryptionEngine
from encryptdecrypt.utils.file_utils import is_encrypted_file


def create_test_file(content: str, file_path: str):
    """Create a test file with given content."""
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"Created test file: {file_path}")


def main():
    """Demonstrate basic encryption and decryption."""
    print("🔐 EncryptDecrypt Basic Usage Example")
    print("=" * 50)
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test files
        test_files = [
            ("hello.txt", "Hello, World! This is a test file."),
            ("data.txt", "Some important data that needs encryption."),
            ("config.json", '{"setting": "value", "enabled": true}')
        ]
        
        for filename, content in test_files:
            file_path = temp_path / filename
            create_test_file(content, str(file_path))
        
        print(f"\n📁 Working directory: {temp_dir}")
        print(f"📄 Files created: {len(test_files)}")
        
        # Initialize encryption engine
        print("\n🔧 Initializing encryption engine...")
        engine = EncryptionEngine()
        
        # Show original files
        print("\n📋 Original files:")
        for file_path in temp_path.iterdir():
            if file_path.is_file():
                size = file_path.stat().st_size
                encrypted = is_encrypted_file(str(file_path))
                status = "🔒 Encrypted" if encrypted else "📄 Regular"
                print(f"  {status}: {file_path.name} ({size} bytes)")
        
        # Encrypt all files
        print("\n🔐 Encrypting files...")
        for file_path in temp_path.iterdir():
            if file_path.is_file() and not is_encrypted_file(str(file_path)):
                result = engine.encrypt_file(str(file_path))
                if result["status"] == "success":
                    print(f"  ✅ {file_path.name} encrypted successfully")
                else:
                    print(f"  ❌ {file_path.name} failed: {result.get('error', 'Unknown error')}")
        
        # Show encrypted files
        print("\n📋 After encryption:")
        for file_path in temp_path.iterdir():
            if file_path.is_file():
                size = file_path.stat().st_size
                encrypted = is_encrypted_file(str(file_path))
                status = "🔒 Encrypted" if encrypted else "📄 Regular"
                print(f"  {status}: {file_path.name} ({size} bytes)")
        
        # Decrypt all files
        print("\n🔓 Decrypting files...")
        for file_path in temp_path.iterdir():
            if file_path.is_file() and is_encrypted_file(str(file_path)):
                result = engine.decrypt_file(str(file_path))
                if result["status"] == "success":
                    print(f"  ✅ {file_path.name} decrypted successfully")
                else:
                    print(f"  ❌ {file_path.name} failed: {result.get('error', 'Unknown error')}")
        
        # Show final files
        print("\n📋 After decryption:")
        for file_path in temp_path.iterdir():
            if file_path.is_file():
                size = file_path.stat().st_size
                encrypted = is_encrypted_file(str(file_path))
                status = "🔒 Encrypted" if encrypted else "📄 Regular"
                print(f"  {status}: {file_path.name} ({size} bytes)")
        
        # Verify content
        print("\n🔍 Verifying file contents:")
        for filename, original_content in test_files:
            file_path = temp_path / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    current_content = f.read()
                if current_content == original_content:
                    print(f"  ✅ {filename}: Content matches")
                else:
                    print(f"  ❌ {filename}: Content mismatch")
    
    print("\n🎉 Example completed successfully!")
    print("💡 Files were automatically cleaned up from temporary directory")


if __name__ == "__main__":
    main() 