#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# Write output to file
with open("test_output.txt", "w") as f:
    f.write("🚀 Starting test...\n")
    
    # Test basic imports
    try:
        import psutil
        f.write("✅ psutil imported\n")
    except Exception as e:
        f.write(f"❌ psutil failed: {e}\n")
    
    try:
        import rich
        f.write("✅ rich imported\n")
    except Exception as e:
        f.write(f"❌ rich failed: {e}\n")
    
    # Test file system
    test_dir = Path("Folderwithstuff")
    if test_dir.exists():
        files = list(test_dir.rglob("*"))
        actual_files = [f for f in files if f.is_file()]
        total_size = sum(f.stat().st_size for f in actual_files)
        total_mb = total_size / (1024 * 1024)
        
        f.write(f"📁 Found {len(actual_files)} files\n")
        f.write(f"💾 Total size: {total_mb:.2f} MB\n")
        
        # Show file types
        extensions = {}
        for file_path in actual_files:
            ext = file_path.suffix.lower()
            extensions[ext] = extensions.get(ext, 0) + 1
        
        f.write("📊 File types:\n")
        for ext, count in sorted(extensions.items()):
            f.write(f"   {ext or 'no extension'}: {count} files\n")
    else:
        f.write(f"❌ Test directory not found: {test_dir}\n")
    
    f.write("🎉 Test complete!\n")

print("Test completed - check test_output.txt") 