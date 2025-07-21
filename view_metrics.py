#!/usr/bin/env python3
"""
Beautiful Metrics Viewer
Author: KleaSCM <KleaSCM@gmail.com>

Display benchmark results with beautiful formatting and analysis.
"""

import json
import glob
from pathlib import Path
from datetime import datetime
import statistics

def load_latest_results():
    """Load the most recent benchmark results."""
    pattern = "metrics/benchmark_results_*.json"
    files = glob.glob(pattern)
    
    if not files:
        # Try the default filename
        default_file = "metrics/benchmark_results.json"
        if Path(default_file).exists():
            with open(default_file, 'r') as f:
                return json.load(f)
        return None
    
    # Get the most recent file
    latest_file = max(files, key=Path(f).stat().st_mtime)
    with open(latest_file, 'r') as f:
        return json.load(f)

def display_header():
    """Display a beautiful header."""
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                     EncryptDecrypt Benchmark Results                         ║")
    print("║                              Author: KleaSCM                                 ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

def display_summary(results):
    """Display the benchmark summary."""
    print("📊 BENCHMARK SUMMARY")
    print("=" * 60)
    
    summary = results.get("summary", {})
    
    print(f"📁 Files Tested:     {results['files_tested']}")
    print(f"💾 Total Size:       {results['total_size_mb']:.2f} MB")
    print(f"⏱️  Total Time:       {summary.get('total_encryption_time', 0) + summary.get('total_decryption_time', 0):.3f}s")
    print()
    
    print("🔐 ENCRYPTION PERFORMANCE")
    print("-" * 40)
    print(f"   Average Time:     {summary.get('avg_encryption_time', 0):.3f}s")
    print(f"   Total Time:       {summary.get('total_encryption_time', 0):.3f}s")
    print(f"   Average Speed:    {summary.get('avg_encryption_speed', 0):.1f} MB/s")
    print()
    
    print("🔓 DECRYPTION PERFORMANCE")
    print("-" * 40)
    print(f"   Average Time:     {summary.get('avg_decryption_time', 0):.3f}s")
    print(f"   Total Time:       {summary.get('total_decryption_time', 0):.3f}s")
    print(f"   Average Speed:    {summary.get('avg_decryption_speed', 0):.1f} MB/s")
    print()

def display_file_analysis(results):
    """Display detailed file analysis."""
    print("📋 FILE ANALYSIS")
    print("=" * 60)
    
    file_results = results.get("file_results", [])
    if not file_results:
        return
    
    # Group by file type
    file_types = {}
    for result in file_results:
        ext = Path(result["file"]).suffix.lower()
        if ext not in file_types:
            file_types[ext] = []
        file_types[ext].append(result)
    
    print("📊 Performance by File Type:")
    print("-" * 40)
    
    for ext, files in file_types.items():
        if len(files) == 0:
            continue
            
        avg_enc_speed = statistics.mean([f["encryption_speed"] for f in files])
        avg_dec_speed = statistics.mean([f["decryption_speed"] for f in files])
        total_size = sum(f["size_mb"] for f in files)
        
        print(f"   {ext or 'no ext'}:")
        print(f"     Files: {len(files)}, Size: {total_size:.2f} MB")
        print(f"     Avg Enc Speed: {avg_enc_speed:.1f} MB/s")
        print(f"     Avg Dec Speed: {avg_dec_speed:.1f} MB/s")
        print()

def display_top_performers(results):
    """Display top performing files."""
    print("🏆 TOP PERFORMERS")
    print("=" * 60)
    
    file_results = results.get("file_results", [])
    if not file_results:
        return
    
    # Sort by encryption speed
    fastest_enc = sorted(file_results, key=lambda x: x["encryption_speed"], reverse=True)[:5]
    
    print("🚀 Fastest Encryption:")
    print("-" * 40)
    for i, result in enumerate(fastest_enc, 1):
        print(f"   {i}. {result['file'][:40]:<40} {result['encryption_speed']:>8.1f} MB/s")
    
    print()
    
    # Sort by decryption speed
    fastest_dec = sorted(file_results, key=lambda x: x["decryption_speed"], reverse=True)[:5]
    
    print("⚡ Fastest Decryption:")
    print("-" * 40)
    for i, result in enumerate(fastest_dec, 1):
        print(f"   {i}. {result['file'][:40]:<40} {result['decryption_speed']:>8.1f} MB/s")
    
    print()

def display_largest_files(results):
    """Display performance on largest files."""
    print("📦 LARGEST FILES PERFORMANCE")
    print("=" * 60)
    
    file_results = results.get("file_results", [])
    if not file_results:
        return
    
    # Sort by file size
    largest_files = sorted(file_results, key=lambda x: x["size_mb"], reverse=True)[:5]
    
    print("📊 Performance on Largest Files:")
    print("-" * 50)
    print(f"{'File':<35} {'Size (MB)':<10} {'Enc (s)':<8} {'Dec (s)':<8} {'Enc Speed':<10} {'Dec Speed':<10}")
    print("-" * 50)
    
    for result in largest_files:
        filename = result['file'][:34] + "..." if len(result['file']) > 34 else result['file']
        print(f"{filename:<35} {result['size_mb']:<10.2f} {result['encryption_time']:<8.3f} "
              f"{result['decryption_time']:<8.3f} {result['encryption_speed']:<10.1f} {result['decryption_speed']:<10.1f}")
    
    print()

def display_statistics(results):
    """Display statistical analysis."""
    print("📈 STATISTICAL ANALYSIS")
    print("=" * 60)
    
    file_results = results.get("file_results", [])
    if not file_results:
        return
    
    enc_speeds = [r["encryption_speed"] for r in file_results]
    dec_speeds = [r["decryption_speed"] for r in file_results]
    enc_times = [r["encryption_time"] for r in file_results]
    dec_times = [r["decryption_time"] for r in file_results]
    
    print("🔐 Encryption Statistics:")
    print("-" * 30)
    print(f"   Mean Speed:       {statistics.mean(enc_speeds):.1f} MB/s")
    print(f"   Median Speed:     {statistics.median(enc_speeds):.1f} MB/s")
    print(f"   Min Speed:        {min(enc_speeds):.1f} MB/s")
    print(f"   Max Speed:        {max(enc_speeds):.1f} MB/s")
    print(f"   Std Deviation:    {statistics.stdev(enc_speeds):.1f} MB/s")
    print()
    
    print("🔓 Decryption Statistics:")
    print("-" * 30)
    print(f"   Mean Speed:       {statistics.mean(dec_speeds):.1f} MB/s")
    print(f"   Median Speed:     {statistics.median(dec_speeds):.1f} MB/s")
    print(f"   Min Speed:        {min(dec_speeds):.1f} MB/s")
    print(f"   Max Speed:        {max(dec_speeds):.1f} MB/s")
    print(f"   Std Deviation:    {statistics.stdev(dec_speeds):.1f} MB/s")
    print()

def display_integrity_check(results):
    """Display integrity check results."""
    print("🔍 INTEGRITY VERIFICATION")
    print("=" * 60)
    
    file_results = results.get("file_results", [])
    if not file_results:
        return
    
    integrity_ok = sum(1 for r in file_results if r["integrity_ok"])
    total_files = len(file_results)
    
    print(f"✅ Files with integrity verified: {integrity_ok}/{total_files}")
    print(f"📊 Integrity success rate: {(integrity_ok/total_files)*100:.1f}%")
    
    if integrity_ok == total_files:
        print("🎉 All files passed integrity verification!")
    else:
        print("⚠️  Some files failed integrity verification!")
    
    print()

def display_timestamp(results):
    """Display benchmark timestamp."""
    timestamp = results.get("timestamp", "")
    if timestamp:
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            print(f"🕒 Benchmark run: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        except:
            pass

def main():
    """Main function to display metrics."""
    results = load_latest_results()
    
    if not results:
        print("❌ No benchmark results found!")
        print("Run the benchmark first with: python3 simple_benchmark.py")
        return
    
    display_header()
    display_summary(results)
    display_file_analysis(results)
    display_top_performers(results)
    display_largest_files(results)
    display_statistics(results)
    display_integrity_check(results)
    display_timestamp(results)
    
    print("🎉 Analysis complete! Your encryption system is performing excellently! 💕")

if __name__ == "__main__":
    main() 