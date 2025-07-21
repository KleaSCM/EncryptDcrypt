#!/usr/bin/env python3
"""
Simple Benchmark Test
Author: KleaSCM <KleaSCM@gmail.com>
"""

import os
import sys
from pathlib import Path

print("🚀 Starting benchmark test...")

# Test imports
try:
    import psutil
    print("✅ psutil imported successfully")
except ImportError as e:
    print(f"❌ psutil import failed: {e}")

try:
    import rich
    from rich.console import Console
    print("✅ rich imported successfully")
except ImportError as e:
    print(f"❌ rich import failed: {e}")

try:
    from cryptography.fernet import Fernet
    print("✅ cryptography imported successfully")
except ImportError as e:
    print(f"❌ cryptography import failed: {e}")

# Test file system
test_dir = Path("Folderwithstuff")
if test_dir.exists():
    print(f"✅ Test directory found: {test_dir}")
    files = list(test_dir.rglob("*"))
    print(f"📁 Found {len(files)} files/directories")
    
    # Count actual files
    actual_files = [f for f in files if f.is_file()]
    print(f"📄 Found {len(actual_files)} actual files")
    
    # Calculate total size
    total_size = sum(f.stat().st_size for f in actual_files)
    total_mb = total_size / (1024 * 1024)
    print(f"💾 Total size: {total_mb:.2f} MB")
    
    # Show file types
    extensions = {}
    for f in actual_files:
        ext = f.suffix.lower()
        extensions[ext] = extensions.get(ext, 0) + 1
    
    print("📊 File types:")
    for ext, count in sorted(extensions.items()):
        print(f"   {ext or 'no extension'}: {count} files")
    
else:
    print(f"❌ Test directory not found: {test_dir}")

print("�� Test complete!") 