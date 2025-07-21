#!/usr/bin/env python3
"""
Simple Benchmark Script
Author: KleaSCM <KleaSCM@gmail.com>

A simplified benchmarking script that tests the encryption system.
"""

import os
import time
import hashlib
from pathlib import Path
import json
from datetime import datetime
import sys

def get_file_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def analyze_files(directory):
    """Analyze all files in the directory."""
    print(f"🔍 Analyzing files in {directory}...")
    
    files = []
    total_size = 0
    file_types = {}
    
    for file_path in Path(directory).rglob("*"):
        if file_path.is_file():
            try:
                size = file_path.stat().st_size
                ext = file_path.suffix.lower()
                
                files.append({
                    "path": str(file_path),
                    "size_bytes": size,
                    "size_mb": round(size / (1024 * 1024), 2),
                    "extension": ext
                })
                
                total_size += size
                file_types[ext] = file_types.get(ext, 0) + 1
                
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
    
    print(f"📁 Found {len(files)} files")
    print(f"💾 Total size: {round(total_size / (1024 * 1024), 2)} MB")
    print(f"📊 File types: {len(file_types)} different types")
    
    return files, total_size, file_types

def test_encryption_engine():
    """Test the encryption engine with a simple file."""
    print("\n🔐 Testing encryption engine...")
    
    # Create a test file
    test_file = "test_benchmark.txt"
    test_content = "This is a test file for benchmarking the encryption system. " * 1000
    
    with open(test_file, "w") as f:
        f.write(test_content)
    
    try:
        # Import the standalone encryption engine from same directory
        from standalone_engine import StandaloneEncryptionEngine
        
        engine = StandaloneEncryptionEngine()
        
        # Test encryption
        start_time = time.time()
        result = engine.encrypt_file(test_file, "test_encrypted.txt")
        encryption_time = time.time() - start_time
        
        if result["status"] != "success":
            raise Exception(f"Encryption failed: {result.get('error', 'Unknown error')}")
        
        # Test decryption
        start_time = time.time()
        result = engine.decrypt_file("test_encrypted.txt", "test_decrypted.txt")
        decryption_time = time.time() - start_time
        
        if result["status"] != "success":
            raise Exception(f"Decryption failed: {result.get('error', 'Unknown error')}")
        
        # Verify integrity
        original_hash = get_file_hash(test_file)
        decrypted_hash = get_file_hash("test_decrypted.txt")
        
        print(f"✅ Encryption time: {encryption_time:.3f}s")
        print(f"✅ Decryption time: {decryption_time:.3f}s")
        print(f"✅ Integrity check: {'PASS' if original_hash == decrypted_hash else 'FAIL'}")
        
        # Clean up
        os.remove(test_file)
        os.remove("test_encrypted.txt")
        os.remove("test_decrypted.txt")
        
        return True
        
    except Exception as e:
        print(f"❌ Encryption engine test failed: {e}")
        return False

def benchmark_files(files, max_files=10):
    """Benchmark encryption/decryption with actual files."""
    print(f"\n🚀 Benchmarking with {min(len(files), max_files)} files...")
    
    # Sort by size (largest first)
    files.sort(key=lambda x: x["size_bytes"], reverse=True)
    test_files = files[:max_files]
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "files_tested": len(test_files),
        "total_size_mb": sum(f["size_mb"] for f in test_files),
        "encryption_times": [],
        "decryption_times": [],
        "file_results": []
    }
    
    try:
        from standalone_engine import StandaloneEncryptionEngine
        
        engine = StandaloneEncryptionEngine()
        
        for i, file_info in enumerate(test_files, 1):
            print(f"Processing {i}/{len(test_files)}: {Path(file_info['path']).name}")
            
            try:
                # Create temporary encrypted file
                temp_encrypted = f"temp_enc_{i}.encrypted"
                temp_decrypted = f"temp_dec_{i}.txt"
                
                # Time encryption
                start_time = time.time()
                result = engine.encrypt_file(file_info["path"], temp_encrypted)
                enc_time = time.time() - start_time
                
                if result["status"] != "success":
                    raise Exception(f"Encryption failed: {result.get('error', 'Unknown error')}")
                
                # Time decryption
                start_time = time.time()
                result = engine.decrypt_file(temp_encrypted, temp_decrypted)
                dec_time = time.time() - start_time
                
                if result["status"] != "success":
                    raise Exception(f"Decryption failed: {result.get('error', 'Unknown error')}")
                
                # Calculate hashes
                original_hash = get_file_hash(file_info["path"])
                decrypted_hash = get_file_hash(temp_decrypted)
                
                file_result = {
                    "file": Path(file_info["path"]).name,
                    "size_mb": file_info["size_mb"],
                    "encryption_time": round(enc_time, 3),
                    "decryption_time": round(dec_time, 3),
                    "encryption_speed": round(file_info["size_mb"] / enc_time, 2),
                    "decryption_speed": round(file_info["size_mb"] / dec_time, 2),
                    "integrity_ok": original_hash == decrypted_hash
                }
                
                results["encryption_times"].append(enc_time)
                results["decryption_times"].append(dec_time)
                results["file_results"].append(file_result)
                
                print(f"  ✅ Enc: {enc_time:.3f}s, Dec: {dec_time:.3f}s")
                
                # Clean up
                os.remove(temp_encrypted)
                os.remove(temp_decrypted)
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        # Calculate summary
        if results["encryption_times"]:
            results["summary"] = {
                "avg_encryption_time": round(sum(results["encryption_times"]) / len(results["encryption_times"]), 3),
                "avg_decryption_time": round(sum(results["decryption_times"]) / len(results["decryption_times"]), 3),
                "total_encryption_time": round(sum(results["encryption_times"]), 3),
                "total_decryption_time": round(sum(results["decryption_times"]), 3),
                "avg_encryption_speed": round(results["total_size_mb"] / sum(results["encryption_times"]), 2),
                "avg_decryption_speed": round(results["total_size_mb"] / sum(results["decryption_times"]), 2)
            }
        
        return results
        
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        return None

def save_results(results, filename="benchmark_results.json"):
    """Save benchmark results to JSON file."""
    metrics_dir = Path("../metrics")
    metrics_dir.mkdir(exist_ok=True)
    
    results_file = metrics_dir / filename
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {results_file}")

def main():
    """Main benchmark function."""
    print("🚀 EncryptDecrypt Benchmark Suite")
    print("=" * 50)
    
    # Analyze files
    files, total_size, file_types = analyze_files("../Folderwithstuff")
    
    if not files:
        print("❌ No files found for benchmarking!")
        return
    
    # Test encryption engine
    if not test_encryption_engine():
        print("❌ Encryption engine test failed!")
        return
    
    # Run benchmarks
    results = benchmark_files(files, max_files=20)  # Test with up to 20 files
    
    if results:
        # Display summary
        print("\n📊 Benchmark Summary:")
        print("=" * 30)
        summary = results.get("summary", {})
        print(f"Files tested: {results['files_tested']}")
        print(f"Total size: {results['total_size_mb']} MB")
        print(f"Avg encryption time: {summary.get('avg_encryption_time', 'N/A')}s")
        print(f"Avg decryption time: {summary.get('avg_decryption_time', 'N/A')}s")
        print(f"Avg encryption speed: {summary.get('avg_encryption_speed', 'N/A')} MB/s")
        print(f"Avg decryption speed: {summary.get('avg_decryption_speed', 'N/A')} MB/s")
        
        # Save results
        save_results(results)
    
    print("\n🎉 Benchmark complete!")

if __name__ == "__main__":
    main() 