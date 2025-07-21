#!/usr/bin/env python3
"""
Comprehensive Benchmarking Suite for EncryptDecrypt System
Author: KleaSCM <KleaSCM@gmail.com>

This script performs extensive benchmarking of the encryption/decryption system
with large datasets, measuring performance, memory usage, and file integrity.
"""

import os
import sys
import time
import psutil
import hashlib
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from encryptdecrypt.core.engine import EncryptionEngine
from encryptdecrypt.utils.file_utils import is_encrypted_file
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text

class BenchmarkSuite:
    """
    Comprehensive benchmarking suite for testing encryption/decryption performance
    with large datasets and generating detailed metrics.
    """
    
    def __init__(self, test_directory: str, metrics_directory: str = "metrics"):
        """
        Initialize the benchmark suite.
        
        Args:
            test_directory: Directory containing test files
            metrics_directory: Directory to store benchmark results
        """
        self.test_directory = Path(test_directory)
        self.metrics_directory = Path(metrics_directory)
        self.metrics_directory.mkdir(exist_ok=True)
        
        self.console = Console()
        self.engine = EncryptionEngine()
        
        # Benchmark results storage
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "system_info": self._get_system_info(),
            "file_analysis": {},
            "encryption_benchmarks": {},
            "decryption_benchmarks": {},
            "memory_usage": {},
            "integrity_checks": {},
            "summary": {}
        }
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information for benchmarking context."""
        return {
            "platform": sys.platform,
            "python_version": sys.version,
            "cpu_count": os.cpu_count(),
            "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "disk_usage": {
                "total_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
                "free_gb": round(psutil.disk_usage('/').free / (1024**3), 2)
            }
        }
    
    def analyze_test_files(self) -> Dict[str, Any]:
        """
        Analyze all files in the test directory to understand the dataset.
        
        Returns:
            Dictionary containing file analysis results
        """
        self.console.print(Panel.fit("🔍 Analyzing Test Files", style="bold magenta"))
        
        file_info = {
            "total_files": 0,
            "total_size_bytes": 0,
            "file_types": {},
            "size_distribution": {
                "small": 0,      # < 1MB
                "medium": 0,     # 1MB - 10MB
                "large": 0,      # 10MB - 100MB
                "huge": 0        # > 100MB
            },
            "files": []
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Scanning files...", total=None)
            
            for file_path in self.test_directory.rglob("*"):
                if file_path.is_file():
                    try:
                        stat = file_path.stat()
                        size = stat.st_size
                        ext = file_path.suffix.lower()
                        
                        file_info["total_files"] += 1
                        file_info["total_size_bytes"] += size
                        
                        # Categorize by size
                        if size < 1024 * 1024:  # < 1MB
                            file_info["size_distribution"]["small"] += 1
                        elif size < 10 * 1024 * 1024:  # < 10MB
                            file_info["size_distribution"]["medium"] += 1
                        elif size < 100 * 1024 * 1024:  # < 100MB
                            file_info["size_distribution"]["large"] += 1
                        else:
                            file_info["size_distribution"]["huge"] += 1
                        
                        # Track file types
                        file_info["file_types"][ext] = file_info["file_types"].get(ext, 0) + 1
                        
                        file_info["files"].append({
                            "path": str(file_path),
                            "size_bytes": size,
                            "size_mb": round(size / (1024 * 1024), 2),
                            "extension": ext,
                            "is_encrypted": is_encrypted_file(str(file_path))
                        })
                        
                        progress.update(task, description=f"Found {file_info['total_files']} files...")
                        
                    except Exception as e:
                        self.console.print(f"[red]Error analyzing {file_path}: {e}[/red]")
        
        # Sort files by size for better benchmarking
        file_info["files"].sort(key=lambda x: x["size_bytes"], reverse=True)
        
        self.results["file_analysis"] = file_info
        
        # Display summary
        total_mb = round(file_info["total_size_bytes"] / (1024 * 1024), 2)
        self.console.print(f"\n[green]📊 Dataset Analysis Complete![/green]")
        self.console.print(f"📁 Total Files: {file_info['total_files']}")
        self.console.print(f"💾 Total Size: {total_mb} MB")
        self.console.print(f"📈 Size Distribution: {file_info['size_distribution']}")
        
        return file_info
    
    def measure_memory_usage(self, operation: str) -> Dict[str, float]:
        """
        Measure memory usage during operations.
        
        Args:
            operation: Name of the operation being measured
            
        Returns:
            Dictionary with memory usage metrics
        """
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            "rss_mb": round(memory_info.rss / (1024 * 1024), 2),
            "vms_mb": round(memory_info.vms / (1024 * 1024), 2),
            "percent": round(process.memory_percent(), 2)
        }
    
    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of a file for integrity verification."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def benchmark_encryption(self, files: List[Dict]) -> Dict[str, Any]:
        """
        Benchmark encryption performance with detailed metrics.
        
        Args:
            files: List of file information dictionaries
            
        Returns:
            Dictionary containing encryption benchmark results
        """
        self.console.print(Panel.fit("🔐 Encryption Benchmarking", style="bold blue"))
        
        results = {
            "total_files": len(files),
            "total_size_bytes": sum(f["size_bytes"] for f in files),
            "encryption_times": [],
            "memory_usage": [],
            "file_results": [],
            "errors": []
        }
        
        # Create temporary directory for encrypted files
        temp_dir = Path("temp_encrypted")
        temp_dir.mkdir(exist_ok=True)
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=self.console
            ) as progress:
                task = progress.add_task("Encrypting files...", total=len(files))
                
                for file_info in files:
                    try:
                        file_path = Path(file_info["path"])
                        temp_path = temp_dir / f"{file_path.name}.encrypted"
                        
                        # Measure memory before
                        memory_before = self.measure_memory_usage("encryption_start")
                        
                        # Time the encryption
                        start_time = time.time()
                        self.engine.encrypt_file(str(file_path), str(temp_path))
                        encryption_time = time.time() - start_time
                        
                        # Measure memory after
                        memory_after = self.measure_memory_usage("encryption_end")
                        
                        # Calculate file hash for integrity
                        original_hash = self.calculate_file_hash(str(file_path))
                        encrypted_hash = self.calculate_file_hash(str(temp_path))
                        
                        file_result = {
                            "file": str(file_path),
                            "size_mb": file_info["size_mb"],
                            "encryption_time_seconds": round(encryption_time, 3),
                            "speed_mbps": round(file_info["size_mb"] / encryption_time, 2),
                            "memory_before_mb": memory_before["rss_mb"],
                            "memory_after_mb": memory_after["rss_mb"],
                            "memory_delta_mb": round(memory_after["rss_mb"] - memory_before["rss_mb"], 2),
                            "original_hash": original_hash,
                            "encrypted_hash": encrypted_hash,
                            "success": True
                        }
                        
                        results["encryption_times"].append(encryption_time)
                        results["memory_usage"].append(memory_after["rss_mb"])
                        results["file_results"].append(file_result)
                        
                        progress.update(task, advance=1, description=f"Encrypted {file_path.name}")
                        
                    except Exception as e:
                        error_info = {
                            "file": str(file_path),
                            "error": str(e),
                            "success": False
                        }
                        results["errors"].append(error_info)
                        self.console.print(f"[red]Error encrypting {file_path}: {e}[/red]")
                        progress.update(task, advance=1)
        
        finally:
            # Clean up temporary directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        
        # Calculate summary statistics
        if results["encryption_times"]:
            results["summary"] = {
                "total_time_seconds": round(sum(results["encryption_times"]), 3),
                "average_time_seconds": round(sum(results["encryption_times"]) / len(results["encryption_times"]), 3),
                "total_size_mb": round(results["total_size_bytes"] / (1024 * 1024), 2),
                "average_speed_mbps": round(
                    (results["total_size_bytes"] / (1024 * 1024)) / sum(results["encryption_times"]), 2
                ),
                "max_memory_mb": max(results["memory_usage"]),
                "min_memory_mb": min(results["memory_usage"]),
                "avg_memory_mb": round(sum(results["memory_usage"]) / len(results["memory_usage"]), 2)
            }
        
        self.results["encryption_benchmarks"] = results
        return results
    
    def benchmark_decryption(self, files: List[Dict]) -> Dict[str, Any]:
        """
        Benchmark decryption performance with detailed metrics.
        
        Args:
            files: List of file information dictionaries
            
        Returns:
            Dictionary containing decryption benchmark results
        """
        self.console.print(Panel.fit("🔓 Decryption Benchmarking", style="bold green"))
        
        results = {
            "total_files": len(files),
            "total_size_bytes": sum(f["size_bytes"] for f in files),
            "decryption_times": [],
            "memory_usage": [],
            "file_results": [],
            "errors": []
        }
        
        # Create temporary directory for decrypted files
        temp_dir = Path("temp_decrypted")
        temp_dir.mkdir(exist_ok=True)
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=self.console
            ) as progress:
                task = progress.add_task("Decrypting files...", total=len(files))
                
                for file_info in files:
                    try:
                        file_path = Path(file_info["path"])
                        temp_path = temp_dir / f"{file_path.name}.decrypted"
                        
                        # Measure memory before
                        memory_before = self.measure_memory_usage("decryption_start")
                        
                        # Time the decryption
                        start_time = time.time()
                        self.engine.decrypt_file(str(file_path), str(temp_path))
                        decryption_time = time.time() - start_time
                        
                        # Measure memory after
                        memory_after = self.measure_memory_usage("decryption_end")
                        
                        # Calculate file hash for integrity
                        original_hash = self.calculate_file_hash(str(file_path))
                        decrypted_hash = self.calculate_file_hash(str(temp_path))
                        
                        file_result = {
                            "file": str(file_path),
                            "size_mb": file_info["size_mb"],
                            "decryption_time_seconds": round(decryption_time, 3),
                            "speed_mbps": round(file_info["size_mb"] / decryption_time, 2),
                            "memory_before_mb": memory_before["rss_mb"],
                            "memory_after_mb": memory_after["rss_mb"],
                            "memory_delta_mb": round(memory_after["rss_mb"] - memory_before["rss_mb"], 2),
                            "original_hash": original_hash,
                            "decrypted_hash": decrypted_hash,
                            "success": True
                        }
                        
                        results["decryption_times"].append(decryption_time)
                        results["memory_usage"].append(memory_after["rss_mb"])
                        results["file_results"].append(file_result)
                        
                        progress.update(task, advance=1, description=f"Decrypted {file_path.name}")
                        
                    except Exception as e:
                        error_info = {
                            "file": str(file_path),
                            "error": str(e),
                            "success": False
                        }
                        results["errors"].append(error_info)
                        self.console.print(f"[red]Error decrypting {file_path}: {e}[/red]")
                        progress.update(task, advance=1)
        
        finally:
            # Clean up temporary directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        
        # Calculate summary statistics
        if results["decryption_times"]:
            results["summary"] = {
                "total_time_seconds": round(sum(results["decryption_times"]), 3),
                "average_time_seconds": round(sum(results["decryption_times"]) / len(results["decryption_times"]), 3),
                "total_size_mb": round(results["total_size_bytes"] / (1024 * 1024), 2),
                "average_speed_mbps": round(
                    (results["total_size_bytes"] / (1024 * 1024)) / sum(results["decryption_times"]), 2
                ),
                "max_memory_mb": max(results["memory_usage"]),
                "min_memory_mb": min(results["memory_usage"]),
                "avg_memory_mb": round(sum(results["memory_usage"]) / len(results["memory_usage"]), 2)
            }
        
        self.results["decryption_benchmarks"] = results
        return results
    
    def run_integrity_checks(self, files: List[Dict]) -> Dict[str, Any]:
        """
        Run comprehensive integrity checks on all files.
        
        Args:
            files: List of file information dictionaries
            
        Returns:
            Dictionary containing integrity check results
        """
        self.console.print(Panel.fit("🔍 Integrity Verification", style="bold yellow"))
        
        results = {
            "total_files": len(files),
            "integrity_checks": [],
            "encrypted_file_detection": [],
            "errors": []
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Verifying file integrity...", total=len(files))
            
            for file_info in files:
                try:
                    file_path = Path(file_info["path"])
                    
                    # Check if file is encrypted
                    is_encrypted = is_encrypted_file(str(file_path))
                    
                    # Calculate file hash
                    file_hash = self.calculate_file_hash(str(file_path))
                    
                    # Verify file is readable and has content
                    file_size = file_path.stat().st_size
                    is_readable = file_size > 0
                    
                    integrity_check = {
                        "file": str(file_path),
                        "size_bytes": file_size,
                        "size_mb": round(file_size / (1024 * 1024), 2),
                        "hash": file_hash,
                        "is_encrypted": is_encrypted,
                        "is_readable": is_readable,
                        "integrity_ok": is_readable and file_size > 0
                    }
                    
                    results["integrity_checks"].append(integrity_check)
                    results["encrypted_file_detection"].append({
                        "file": str(file_path),
                        "detected_as_encrypted": is_encrypted
                    })
                    
                    progress.update(task, advance=1, description=f"Checked {file_path.name}")
                    
                except Exception as e:
                    error_info = {
                        "file": str(file_path),
                        "error": str(e)
                    }
                    results["errors"].append(error_info)
                    self.console.print(f"[red]Error checking {file_path}: {e}[/red]")
                    progress.update(task, advance=1)
        
        # Calculate summary
        results["summary"] = {
            "total_files": len(files),
            "readable_files": sum(1 for check in results["integrity_checks"] if check["integrity_ok"]),
            "encrypted_files": sum(1 for check in results["integrity_checks"] if check["is_encrypted"]),
            "total_size_mb": round(sum(check["size_bytes"] for check in results["integrity_checks"]) / (1024 * 1024), 2)
        }
        
        self.results["integrity_checks"] = results
        return results
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report of all benchmarks."""
        self.console.print(Panel.fit("📊 Generating Summary Report", style="bold cyan"))
        
        # Calculate overall summary
        file_analysis = self.results["file_analysis"]
        encryption_results = self.results.get("encryption_benchmarks", {})
        decryption_results = self.results.get("decryption_benchmarks", {})
        integrity_results = self.results.get("integrity_checks", {})
        
        summary = {
            "benchmark_timestamp": self.results["timestamp"],
            "dataset_info": {
                "total_files": file_analysis.get("total_files", 0),
                "total_size_mb": round(file_analysis.get("total_size_bytes", 0) / (1024 * 1024), 2),
                "file_types": len(file_analysis.get("file_types", {})),
                "size_distribution": file_analysis.get("size_distribution", {})
            },
            "encryption_performance": encryption_results.get("summary", {}),
            "decryption_performance": decryption_results.get("summary", {}),
            "integrity_summary": integrity_results.get("summary", {}),
            "system_info": self.results["system_info"]
        }
        
        self.results["summary"] = summary
        
        # Save detailed results to JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.metrics_directory / f"benchmark_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        self.console.print(f"[green]✅ Detailed results saved to: {results_file}[/green]")
        
        return summary
    
    def display_summary_table(self, summary: Dict[str, Any]):
        """Display a beautiful summary table of benchmark results."""
        self.console.print(Panel.fit("🏆 Benchmark Summary", style="bold magenta"))
        
        # Dataset Info Table
        dataset_table = Table(title="📁 Dataset Information", show_header=True, header_style="bold magenta")
        dataset_table.add_column("Metric", style="cyan")
        dataset_table.add_column("Value", style="green")
        
        dataset_info = summary["dataset_info"]
        dataset_table.add_row("Total Files", str(dataset_info["total_files"]))
        dataset_table.add_row("Total Size", f"{dataset_info['total_size_mb']} MB")
        dataset_table.add_row("File Types", str(dataset_info["file_types"]))
        dataset_table.add_row("Small Files (<1MB)", str(dataset_info["size_distribution"]["small"]))
        dataset_table.add_row("Medium Files (1-10MB)", str(dataset_info["size_distribution"]["medium"]))
        dataset_table.add_row("Large Files (10-100MB)", str(dataset_info["size_distribution"]["large"]))
        dataset_table.add_row("Huge Files (>100MB)", str(dataset_info["size_distribution"]["huge"]))
        
        self.console.print(dataset_table)
        
        # Performance Table
        perf_table = Table(title="⚡ Performance Metrics", show_header=True, header_style="bold blue")
        perf_table.add_column("Operation", style="cyan")
        perf_table.add_column("Total Time (s)", style="green")
        perf_table.add_column("Avg Speed (MB/s)", style="yellow")
        perf_table.add_column("Max Memory (MB)", style="red")
        
        if summary["encryption_performance"]:
            enc_perf = summary["encryption_performance"]
            perf_table.add_row(
                "Encryption",
                str(enc_perf.get("total_time_seconds", "N/A")),
                str(enc_perf.get("average_speed_mbps", "N/A")),
                str(enc_perf.get("max_memory_mb", "N/A"))
            )
        
        if summary["decryption_performance"]:
            dec_perf = summary["decryption_performance"]
            perf_table.add_row(
                "Decryption",
                str(dec_perf.get("total_time_seconds", "N/A")),
                str(dec_perf.get("average_speed_mbps", "N/A")),
                str(dec_perf.get("max_memory_mb", "N/A"))
            )
        
        self.console.print(perf_table)
        
        # System Info Table
        sys_table = Table(title="🖥️ System Information", show_header=True, header_style="bold green")
        sys_table.add_column("Component", style="cyan")
        sys_table.add_column("Specification", style="green")
        
        sys_info = summary["system_info"]
        sys_table.add_row("Platform", sys_info["platform"])
        sys_table.add_row("Python Version", sys_info["python_version"])
        sys_table.add_row("CPU Cores", str(sys_info["cpu_count"]))
        sys_table.add_row("Total Memory", f"{sys_info['memory_total_gb']} GB")
        sys_table.add_row("Disk Space", f"{sys_info['disk_usage']['free_gb']} GB free")
        
        self.console.print(sys_table)
    
    def run_full_benchmark(self):
        """Run the complete benchmarking suite."""
        self.console.print(Panel.fit("🚀 Starting Comprehensive Benchmark Suite", style="bold magenta"))
        
        # Step 1: Analyze test files
        file_analysis = self.analyze_test_files()
        
        if not file_analysis["files"]:
            self.console.print("[red]❌ No files found for benchmarking![/red]")
            return
        
        # Step 2: Run integrity checks
        integrity_results = self.run_integrity_checks(file_analysis["files"])
        
        # Step 3: Benchmark encryption (only for non-encrypted files)
        non_encrypted_files = [f for f in file_analysis["files"] if not f["is_encrypted"]]
        if non_encrypted_files:
            encryption_results = self.benchmark_encryption(non_encrypted_files)
        else:
            self.console.print("[yellow]⚠️ No non-encrypted files found for encryption benchmarking[/yellow]")
        
        # Step 4: Benchmark decryption (only for encrypted files)
        encrypted_files = [f for f in file_analysis["files"] if f["is_encrypted"]]
        if encrypted_files:
            decryption_results = self.benchmark_decryption(encrypted_files)
        else:
            self.console.print("[yellow]⚠️ No encrypted files found for decryption benchmarking[/yellow]")
        
        # Step 5: Generate and display summary
        summary = self.generate_summary_report()
        self.display_summary_table(summary)
        
        self.console.print(Panel.fit("🎉 Benchmark Suite Complete!", style="bold green"))


def main():
    """Main entry point for the benchmark suite."""
    console = Console()
    
    # Check if test directory exists
    test_dir = "Folderwithstuff"
    if not os.path.exists(test_dir):
        console.print(f"[red]❌ Test directory '{test_dir}' not found![/red]")
        console.print("Please ensure the test directory exists and contains files to benchmark.")
        return
    
    # Create and run benchmark suite
    benchmark = BenchmarkSuite(test_dir)
    benchmark.run_full_benchmark()


if __name__ == "__main__":
    main() 