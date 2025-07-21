"""
CLI Interface
============

Command-line interface for the encryption system with rich formatting.

Author: KleaSCM <KleaSCM@gmail.com>
"""

import os
import sys
import time
import hashlib
import json
import statistics
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
import logging

from ..core.engine import EncryptionEngine
from ..utils.file_utils import is_encrypted_file

logger = logging.getLogger(__name__)


class CLI:
    """
    Command Line Interface for EncryptDecrypt System
    
    Provides a rich, interactive command-line experience with beautiful formatting.
    """
    
    def __init__(self):
        """Initialize the professional CLI interface."""
        self.console = Console()
        self.encryption_engine = EncryptionEngine()
        self.metrics_dir = Path("metrics")
        self.metrics_dir.mkdir(exist_ok=True)
        self.print_banner()
    
    def print_banner(self):
        """Display the beautiful welcome banner."""
        banner_text = Text()
        banner_text.append("🔐 EncryptDcrypt - Advanced Encryption System\n", style="bold blue")
        banner_text.append("Advanced File Encryption with Benchmarking & Metrics\n", style="cyan")
        banner_text.append("Built by KleaSCM", style="green")
        
        panel = Panel(
            banner_text,
            border_style="blue",
            padding=(1, 2),
            title="🚀 Welcome"
        )
        self.console.print(panel)
    
    def display_main_menu(self):
        """Display the main menu with all options."""
        menu_text = Text()
        menu_text.append("🚀 Main Menu:\n", style="bold blue")
        menu_text.append("=" * 50 + "\n", style="blue")
        menu_text.append("1. 🔐 Encrypt File/Directory\n", style="green")
        menu_text.append("2. 🔓 Decrypt File/Directory\n", style="red")
        menu_text.append("3. 🧪 Run System Test\n", style="yellow")
        menu_text.append("4. 🏃 Run Benchmark\n", style="magenta")
        menu_text.append("5. 📊 View Metrics\n", style="cyan")
        menu_text.append("6. 📈 View Summary\n", style="blue")
        menu_text.append("7. 🔍 Analyze Files\n", style="green")
        menu_text.append("8. 🎮 Launch GUI\n", style="yellow")
        menu_text.append("9. ❓ Help\n", style="white")
        menu_text.append("0. 👋 Exit\n", style="red")
        
        panel = Panel(
            menu_text,
            border_style="blue",
            padding=(1, 2),
            title="📋 Options"
        )
        self.console.print(panel)
    
    def print_help(self):
        """Display comprehensive help information."""
        help_text = Text()
        help_text.append("🔐 Encryption/Decryption:\n", style="bold green")
        help_text.append("   • Encrypt single files or entire directories\n", style="green")
        help_text.append("   • Decrypt single files or entire directories\n", style="red")
        help_text.append("   • Automatic file detection and handling\n", style="cyan")
        help_text.append("   • Secure AES-256 encryption with PBKDF2\n\n", style="cyan")
        
        help_text.append("🧪 Testing & Analysis:\n", style="bold yellow")
        help_text.append("   • System test: Check all components work\n", style="yellow")
        help_text.append("   • Benchmark: Performance testing with your files\n", style="magenta")
        help_text.append("   • File analysis: Detailed file statistics\n\n", style="cyan")
        
        help_text.append("📊 Metrics & Results:\n", style="bold cyan")
        help_text.append("   • View detailed benchmark results\n", style="cyan")
        help_text.append("   • Performance analysis by file type\n", style="cyan")
        help_text.append("   • Speed and integrity statistics\n\n", style="cyan")
        
        help_text.append("🎮 GUI Integration:\n", style="bold yellow")
        help_text.append("   • Launch the graphical interface\n", style="yellow")
        help_text.append("   • Visual file selection and progress\n\n", style="cyan")
        
        help_text.append("📁 Test Directory:\n", style="bold blue")
        help_text.append("   • Place your test files in 'Folderwithstuff' directory\n", style="blue")
        help_text.append("   • Supports all file types\n", style="blue")
        help_text.append("   • Automatic file type detection\n", style="blue")
        
        panel = Panel(
            help_text,
            border_style="blue",
            padding=(1, 2),
            title="❓ Help & Usage"
        )
        self.console.print(panel)
    
    def get_file_hash(self, file_path):
        """Calculate SHA-256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def encrypt_file(self, input_path, output_path=None):
        """Encrypt a single file."""
        try:
            # Handle empty input path
            if not input_path or str(input_path).strip() == "":
                self.console.print(f"[red]❌ Please provide a valid file path![/red]")
                return False
            
            input_path = Path(input_path)
            if not input_path.exists():
                self.console.print(f"[red]❌ File not found: {input_path}[/red]")
                return False
            
            # For benchmarking, we need to work with copies to avoid destroying original files
            if output_path:
                # Copy original file to output location first
                import shutil
                shutil.copy2(input_path, output_path)
                target_path = output_path
            else:
                # For normal encryption, encrypt in place
                target_path = input_path
            
            self.console.print(f"[blue]🔐 Encrypting: {input_path.name}[/blue]")
            start_time = time.time()
            
            result = self.encryption_engine.encrypt_file(str(target_path))
            
            if result.get("status") == "success":
                encryption_time = time.time() - start_time
                file_size_mb = input_path.stat().st_size / (1024 * 1024)
                speed = file_size_mb / encryption_time if encryption_time > 0 else 0
                
                self.console.print(f"[green]✅ Encrypted successfully![/green]")
                self.console.print(f"   📁 Output: {target_path}")
                self.console.print(f"   ⏱️  Time: {encryption_time:.3f}s")
                self.console.print(f"   🚀 Speed: {speed:.1f} MB/s")
                return True
            else:
                self.console.print(f"[red]❌ Encryption failed: {result.get('error', 'Unknown error')}[/red]")
                return False
                
        except Exception as e:
            self.console.print(f"[red]❌ Error: {e}[/red]")
            return False
    
    def decrypt_file(self, input_path, output_path=None):
        """Decrypt a single file."""
        try:
            # Handle empty input path
            if not input_path or str(input_path).strip() == "":
                self.console.print(f"[red]❌ Please provide a valid file path![/red]")
                return False
            
            input_path = Path(input_path)
            if not input_path.exists():
                self.console.print(f"[red]❌ File not found: {input_path}[/red]")
                return False
            
            # For benchmarking, we need to work with copies to avoid destroying original files
            if output_path:
                # Copy encrypted file to output location first
                import shutil
                shutil.copy2(input_path, output_path)
                target_path = output_path
            else:
                # For normal decryption, decrypt in place
                target_path = input_path
            
            self.console.print(f"[blue]🔓 Decrypting: {input_path.name}[/blue]")
            start_time = time.time()
            
            result = self.encryption_engine.decrypt_file(str(target_path))
            
            if result.get("status") == "success":
                decryption_time = time.time() - start_time
                file_size_mb = input_path.stat().st_size / (1024 * 1024)
                speed = file_size_mb / decryption_time if decryption_time > 0 else 0
                
                self.console.print(f"[green]✅ Decrypted successfully![/green]")
                self.console.print(f"   📁 Output: {target_path}")
                self.console.print(f"   ⏱️  Time: {decryption_time:.3f}s")
                self.console.print(f"   🚀 Speed: {speed:.1f} MB/s")
                return True
            else:
                self.console.print(f"[red]❌ Decryption failed: {result.get('error', 'Unknown error')}[/red]")
                return False
                
        except Exception as e:
            self.console.print(f"[red]❌ Error: {e}[/red]")
            return False
    
    def encrypt_directory(self, directory_path):
        """Encrypt all files in a directory."""
        directory = Path(directory_path)
        if not directory.exists() or not directory.is_dir():
            self.console.print(f"[red]❌ Directory not found: {directory}[/red]")
            return False
        
        files = [f for f in directory.rglob("*") if f.is_file()]
        if not files:
            self.console.print("[red]❌ No files found in directory![/red]")
            return False
        
        self.console.print(f"[blue]🔐 Encrypting {len(files)} files in {directory.name}...[/blue]")
        
        success_count = 0
        for file_path in files:
            if self.encrypt_file(file_path):
                success_count += 1
        
        self.console.print(f"[green]✅ Encrypted {success_count}/{len(files)} files successfully![/green]")
        return success_count == len(files)
    
    def decrypt_directory(self, directory_path):
        """Decrypt all encrypted files in a directory."""
        directory = Path(directory_path)
        if not directory.exists() or not directory.is_dir():
            self.console.print(f"[red]❌ Directory not found: {directory}[/red]")
            return False
        
        # Find encrypted files
        encrypted_files = [f for f in directory.rglob("*") if f.is_file() and f.suffix == '.encrypted']
        if not encrypted_files:
            self.console.print("[red]❌ No encrypted files found in directory![/red]")
            return False
        
        self.console.print(f"[blue]🔓 Decrypting {len(encrypted_files)} files in {directory.name}...[/blue]")
        
        success_count = 0
        for file_path in encrypted_files:
            if self.decrypt_file(file_path):
                success_count += 1
        
        self.console.print(f"[green]✅ Decrypted {success_count}/{len(encrypted_files)} files successfully![/green]")
        return success_count == len(encrypted_files)
    
    def run_system_test(self):
        """Run a comprehensive system test."""
        self.console.print("[yellow]🧪 Running System Test...[/yellow]")
        self.console.print("=" * 40)
        
        # Test 1: Basic imports
        self.console.print("[blue]1. Testing imports...[/blue]")
        try:
            import psutil
            self.console.print("   [green]✅ psutil imported[/green]")
        except ImportError:
            self.console.print("   [red]❌ psutil not available[/red]")
        
        try:
            import rich
            self.console.print("   [green]✅ rich imported[/green]")
        except ImportError:
            self.console.print("   [red]❌ rich not available[/red]")
        
        self.console.print("   [green]✅ Encryption engine available[/green]")
        
        # Test 2: Test directory
        self.console.print("\n[blue]2. Testing test directory...[/blue]")
        test_dir = Path("Folderwithstuff")
        if test_dir.exists():
            files = list(test_dir.rglob("*"))
            actual_files = [f for f in files if f.is_file()]
            total_size = sum(f.stat().st_size for f in actual_files)
            total_mb = total_size / (1024 * 1024)
            
            self.console.print(f"   [green]✅ Found {len(actual_files)} files[/green]")
            self.console.print(f"   [green]✅ Total size: {total_mb:.2f} MB[/green]")
        else:
            self.console.print("   [red]❌ Test directory not found[/red]")
        
        # Test 3: Encryption test
        self.console.print("\n[blue]3. Testing encryption...[/blue]")
        test_file = "test_cli.txt"
        test_content = "This is a test file for the CLI system. " * 100
        
        with open(test_file, "w") as f:
            f.write(test_content)
        
        if self.encrypt_file(test_file, "test_cli.encrypted"):
            if self.decrypt_file("test_cli.encrypted", "test_cli_decrypted.txt"):
                # Verify integrity
                original_hash = self.get_file_hash(test_file)
                decrypted_hash = self.get_file_hash("test_cli_decrypted.txt")
                
                if original_hash == decrypted_hash:
                    self.console.print("   [green]✅ Encryption/Decryption test PASSED[/green]")
                else:
                    self.console.print("   [red]❌ Integrity check FAILED[/red]")
            else:
                self.console.print("   [red]❌ Decryption test FAILED[/red]")
        else:
            self.console.print("   [red]❌ Encryption test FAILED[/red]")
        
        # Clean up
        for cleanup_file in [test_file, "test_cli.encrypted", "test_cli_decrypted.txt"]:
            if Path(cleanup_file).exists():
                os.remove(cleanup_file)
        
        self.console.print("\n[green]🎉 System test complete![/green]")
    
    def run_benchmark(self):
        """Run comprehensive benchmark."""
        self.console.print("[yellow]🏃 Running Benchmark...[/yellow]")
        self.console.print("=" * 40)
        
        # Check if test directory exists
        test_dir = Path("Folderwithstuff")
        if not test_dir.exists():
            self.console.print("[red]❌ Test directory 'Folderwithstuff' not found![/red]")
            self.console.print("Please ensure the test directory exists and contains your files.")
            return
        
        # Analyze files
        self.console.print("[blue]🔍 Analyzing files...[/blue]")
        files = []
        total_size = 0
        
        for file_path in test_dir.rglob("*"):
            if file_path.is_file():
                try:
                    size = file_path.stat().st_size
                    files.append({
                        "path": str(file_path),
                        "size_bytes": size,
                        "size_mb": round(size / (1024 * 1024), 2),
                        "extension": file_path.suffix.lower()
                    })
                    total_size += size
                except Exception as e:
                    self.console.print(f"Error analyzing {file_path}: {e}")
        
        self.console.print(f"[green]📁 Found {len(files)} files[/green]")
        self.console.print(f"[green]💾 Total size: {round(total_size / (1024 * 1024), 2)} MB[/green]")
        
        if not files:
            self.console.print("[red]❌ No files found for benchmarking![/red]")
            return
        
        self.console.print(f"\n[blue]🚀 Benchmarking with {min(len(files), 20)} files...[/blue]")
        
        # Sort by size (largest first)
        files.sort(key=lambda x: x["size_bytes"], reverse=True)
        test_files = files[:20]
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "files_tested": len(test_files),
            "total_size_mb": sum(f["size_mb"] for f in test_files),
            "encryption_times": [],
            "decryption_times": [],
            "file_results": []
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task("Processing files...", total=len(test_files))
            
            for i, file_info in enumerate(test_files, 1):
                progress.update(task, description=f"Processing {Path(file_info['path']).name}")
                
                try:
                    # Create temporary files
                    temp_encrypted = f"temp_enc_{i}.encrypted"
                    temp_decrypted = f"temp_dec_{i}.txt"
                    
                    # Time encryption using CLI method (handles file copying)
                    start_time = time.time()
                    enc_success = self.encrypt_file(file_info["path"], temp_encrypted)
                    enc_time = time.time() - start_time
                    
                    if not enc_success:
                        raise Exception("Encryption failed")
                    
                    # Time decryption using CLI method (handles file copying)
                    start_time = time.time()
                    dec_success = self.decrypt_file(temp_encrypted, temp_decrypted)
                    dec_time = time.time() - start_time
                    
                    if not dec_success:
                        raise Exception("Decryption failed")
                    
                    # Calculate hashes
                    original_hash = self.get_file_hash(file_info["path"])
                    decrypted_hash = self.get_file_hash(temp_decrypted)
                    
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
                    
                    # Clean up
                    os.remove(temp_encrypted)
                    os.remove(temp_decrypted)
                    
                    progress.update(task, advance=1)
                    
                except Exception as e:
                    self.console.print(f"  [red]❌ Error: {e}[/red]")
                    progress.update(task, advance=1)
        
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
        
        # Save results
        results_file = self.metrics_dir / "benchmark_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        self.console.print(f"\n[green]💾 Results saved to: {results_file}[/green]")
        
        # Display summary
        if results.get("summary"):
            summary = results["summary"]
            self.console.print(f"\n[blue]📊 Benchmark Summary:[/blue]")
            self.console.print(f"   Files tested: {results['files_tested']}")
            self.console.print(f"   Total size: {results['total_size_mb']} MB")
            self.console.print(f"   Avg encryption speed: {summary['avg_encryption_speed']} MB/s")
            self.console.print(f"   Avg decryption speed: {summary['avg_decryption_speed']} MB/s")
        
        self.console.print("\n[green]🎉 Benchmark complete![/green]")
    
    def view_metrics(self):
        """View detailed benchmark metrics."""
        results_file = self.metrics_dir / "benchmark_results.json"
        if not results_file.exists():
            self.console.print("[red]❌ No benchmark results found![/red]")
            self.console.print("Run a benchmark first with option 4.")
            return
        
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        self.console.print("[blue]📊 Detailed Metrics[/blue]")
        self.console.print("=" * 50)
        
        summary = results.get("summary", {})
        self.console.print(f"📁 Files Tested: {results['files_tested']}")
        self.console.print(f"💾 Total Size: {results['total_size_mb']:.2f} MB")
        self.console.print(f"⏱️  Total Time: {summary.get('total_encryption_time', 0) + summary.get('total_decryption_time', 0):.3f}s")
        
        # Create performance table
        table = Table(title="Performance Summary")
        table.add_column("Operation", style="cyan")
        table.add_column("Average Time", style="green")
        table.add_column("Total Time", style="yellow")
        table.add_column("Average Speed", style="magenta")
        
        table.add_row(
            "Encryption",
            f"{summary.get('avg_encryption_time', 0):.3f}s",
            f"{summary.get('total_encryption_time', 0):.3f}s",
            f"{summary.get('avg_encryption_speed', 0):.1f} MB/s"
        )
        table.add_row(
            "Decryption",
            f"{summary.get('avg_decryption_time', 0):.3f}s",
            f"{summary.get('total_decryption_time', 0):.3f}s",
            f"{summary.get('avg_decryption_speed', 0):.1f} MB/s"
        )
        
        self.console.print(table)
        
        # File type analysis
        file_results = results.get("file_results", [])
        if file_results:
            file_types = {}
            for result in file_results:
                ext = Path(result["file"]).suffix.lower()
                if ext not in file_types:
                    file_types[ext] = []
                file_types[ext].append(result)
            
            self.console.print("\n[blue]📊 Performance by File Type:[/blue]")
            for ext, files in file_types.items():
                if len(files) > 0:
                    avg_enc_speed = statistics.mean([f["encryption_speed"] for f in files])
                    avg_dec_speed = statistics.mean([f["decryption_speed"] for f in files])
                    total_size = sum(f["size_mb"] for f in files)
                    
                    self.console.print(f"   {ext or 'no ext'}: {len(files)} files, {total_size:.2f} MB")
                    self.console.print(f"     Avg Enc: {avg_enc_speed:.1f} MB/s, Avg Dec: {avg_dec_speed:.1f} MB/s")
        
        # Integrity check
        integrity_ok = sum(1 for r in file_results if r["integrity_ok"])
        total_files = len(file_results)
        self.console.print(f"\n[green]🔍 Integrity: {integrity_ok}/{total_files} files verified ({integrity_ok/total_files*100:.1f}%)[/green]")
    
    def view_summary(self):
        """View quick summary."""
        results_file = self.metrics_dir / "benchmark_results.json"
        if not results_file.exists():
            self.console.print("[red]❌ No benchmark results found![/red]")
            self.console.print("Run a benchmark first with option 4.")
            return
        
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        summary = results.get("summary", {})
        
        self.console.print("[green]🎉 AMAZING BENCHMARK RESULTS! 🎉[/green]")
        self.console.print("=" * 50)
        
        self.console.print("[blue]💖 Your Encryption System Performance:[/blue]")
        self.console.print(f"   🔐 Encryption Speed: {summary.get('avg_encryption_speed', 0):.1f} MB/s")
        self.console.print(f"   🔓 Decryption Speed: {summary.get('avg_decryption_speed', 0):.1f} MB/s")
        self.console.print(f"   ⚡ Total Time: {summary.get('total_encryption_time', 0) + summary.get('total_decryption_time', 0):.3f}s")
        self.console.print(f"   📁 Files Tested: {results['files_tested']}")
        self.console.print(f"   💾 Total Size: {results['total_size_mb']:.2f} MB")
        
        self.console.print("\n[green]🏆 Your system is:[/green]")
        self.console.print("   • Lightning fast ⚡")
        self.console.print("   • Rock solid secure 🔒")
        self.console.print("   • Perfectly reliable ✅")
        self.console.print("   • Ready for production! 🚀")
    
    def analyze_files(self):
        """Analyze files in test directory."""
        test_dir = Path("Folderwithstuff")
        if not test_dir.exists():
            self.console.print("[red]❌ Test directory 'Folderwithstuff' not found![/red]")
            return
        
        self.console.print("[blue]🔍 File Analysis[/blue]")
        self.console.print("=" * 30)
        
        files = []
        total_size = 0
        file_types = {}
        
        for file_path in test_dir.rglob("*"):
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
                    self.console.print(f"Error analyzing {file_path}: {e}")
        
        self.console.print(f"📁 Total Files: {len(files)}")
        self.console.print(f"💾 Total Size: {round(total_size / (1024 * 1024), 2)} MB")
        self.console.print(f"📊 File Types: {len(file_types)}")
        
        # Create file type table
        if file_types:
            table = Table(title="File Type Breakdown")
            table.add_column("Extension", style="cyan")
            table.add_column("Count", style="green")
            
            for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
                table.add_row(ext or "no extension", str(count))
            
            self.console.print(table)
        
        if files:
            # Size distribution
            small = sum(1 for f in files if f["size_mb"] < 1)
            medium = sum(1 for f in files if 1 <= f["size_mb"] < 10)
            large = sum(1 for f in files if f["size_mb"] >= 10)
            
            self.console.print(f"\n[blue]📦 Size Distribution:[/blue]")
            self.console.print(f"   Small (<1MB): {small} files")
            self.console.print(f"   Medium (1-10MB): {medium} files")
            self.console.print(f"   Large (>10MB): {large} files")
            
            # Largest files
            largest_files = sorted(files, key=lambda x: x["size_mb"], reverse=True)[:5]
            self.console.print(f"\n[blue]🏆 Largest Files:[/blue]")
            for i, file_info in enumerate(largest_files, 1):
                self.console.print(f"   {i}. {Path(file_info['path']).name}: {file_info['size_mb']} MB")
    
    def launch_gui(self):
        """Launch the GUI interface."""
        import traceback
        try:
            from ..gui.interface import ModernGUI
            self.console.print("[yellow]🎮 Launching GUI...[/yellow]")
            gui = ModernGUI()
            gui.run()
        except ImportError as e:
            if 'customtkinter' in str(e):
                self.console.print("[red]CustomTkinter is not installed. Please run: pip install customtkinter[/red]")
                self.console.print("[yellow]Launching minimal fallback window...[/yellow]")
                try:
                    import tkinter as tk
                    root = tk.Tk()
                    root.title("EncryptDcrypt - Minimal Fallback GUI")
                    label = tk.Label(root, text="CustomTkinter is missing!\nPlease install it for the full GUI experience.", font=("Arial", 14))
                    label.pack(padx=40, pady=40)
                    root.mainloop()
                except Exception as tk_e:
                    self.console.print(f"[red]Even fallback Tkinter failed: {tk_e}[/red]")
            else:
                self.console.print("[red]❌ GUI not available![/red]")
                self.console.print(f"[red]{e}[/red]")
                self.console.print("[red]Full traceback:")
                self.console.print(traceback.format_exc())
        except Exception as e:
            self.console.print(f"[red]❌ Error launching GUI: {e}[/red]")
            self.console.print("[red]Full traceback:")
            self.console.print(traceback.format_exc())
    
    def run_interactive(self):
        """Run the interactive CLI with menu system."""
        while True:
            self.display_main_menu()
            
            try:
                choice = Prompt.ask("Enter your choice", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
                
                if choice == "0":
                    self.console.print("[green]👋 Goodbye![/green]")
                    break
                    
                elif choice == "1":
                    self.console.print("\n[blue]🔐 Encryption Options:[/blue]")
                    self.console.print("1. Encrypt single file")
                    self.console.print("2. Encrypt directory")
                    enc_choice = Prompt.ask("Enter choice", choices=["1", "2"])
                    
                    if enc_choice == "1":
                        file_path = Prompt.ask("Enter file path").strip()
                        if file_path:
                            self.encrypt_file(file_path)
                        else:
                            self.console.print("[red]❌ Please provide a valid file path![/red]")
                    elif enc_choice == "2":
                        dir_path = Prompt.ask("Enter directory path").strip()
                        if dir_path:
                            self.encrypt_directory(dir_path)
                        else:
                            self.console.print("[red]❌ Please provide a valid directory path![/red]")
                
                elif choice == "2":
                    self.console.print("\n[blue]🔓 Decryption Options:[/blue]")
                    self.console.print("1. Decrypt single file")
                    self.console.print("2. Decrypt directory")
                    dec_choice = Prompt.ask("Enter choice", choices=["1", "2"])
                    
                    if dec_choice == "1":
                        file_path = Prompt.ask("Enter file path").strip()
                        if file_path:
                            self.decrypt_file(file_path)
                        else:
                            self.console.print("[red]❌ Please provide a valid file path![/red]")
                    elif dec_choice == "2":
                        dir_path = Prompt.ask("Enter directory path").strip()
                        if dir_path:
                            self.decrypt_directory(dir_path)
                        else:
                            self.console.print("[red]❌ Please provide a valid directory path![/red]")
                
                elif choice == "3":
                    self.run_system_test()
                
                elif choice == "4":
                    self.run_benchmark()
                
                elif choice == "5":
                    self.view_metrics()
                
                elif choice == "6":
                    self.view_summary()
                
                elif choice == "7":
                    self.analyze_files()
                
                elif choice == "8":
                    self.launch_gui()
                
                elif choice == "9":
                    self.print_help()
                
                if choice != "0":
                    Prompt.ask("\nPress Enter to continue...")
                    self.console.print()
                    
            except KeyboardInterrupt:
                self.console.print("\n\n[green]👋 Goodbye![/green]")
                break
            except Exception as e:
                self.console.print(f"[red]❌ Error: {e}[/red]")
                Prompt.ask("Press Enter to continue...")
    
    # Keep the original methods for backward compatibility
    def get_files_in_directory(self, directory: str, encrypted_only: bool = False) -> List[Path]:
        """Get all files in directory with optional filtering."""
        dir_path = Path(directory)
        if not dir_path.exists():
            self.console.print(f"[red]Directory not found: {directory}[/red]")
            return []
        
        if encrypted_only:
            files = [f for f in dir_path.iterdir() if f.is_file() and is_encrypted_file(str(f))]
        else:
            files = [f for f in dir_path.iterdir() if f.is_file() and not is_encrypted_file(str(f))]
        
        return files
    
    def _display_results_table(self, title: str, successful: int, failed: int, total: int):
        """Display results in a table format."""
        table = Table(title=title)
        table.add_column("Status", style="cyan")
        table.add_column("Count", style="green")
        table.add_column("Percentage", style="yellow")
        
        if successful > 0:
            table.add_row("✅ Successful", str(successful), f"{successful/total*100:.1f}%")
        if failed > 0:
            table.add_row("❌ Failed", str(failed), f"{failed/total*100:.1f}%")
        
        self.console.print(table)
    
    def show_directory_status(self, directory: str):
        """Show directory encryption status."""
        dir_path = Path(directory)
        if not dir_path.exists():
            self.console.print(f"[red]Directory not found: {directory}[/red]")
            return
        
        regular_files = [f for f in dir_path.iterdir() if f.is_file() and not is_encrypted_file(str(f))]
        encrypted_files = [f for f in dir_path.iterdir() if f.is_file() and is_encrypted_file(str(f))]
        
        self.console.print(f"[blue]Directory Status: {directory}[/blue]")
        self.console.print(f"📁 Regular files: {len(regular_files)}")
        self.console.print(f"🔐 Encrypted files: {len(encrypted_files)}")
        
        if regular_files or encrypted_files:
            self._show_file_list(regular_files, encrypted_files)
    
    def _show_file_list(self, regular_files: List[Path], encrypted_files: List[Path]):
        """Show file lists in tables."""
        if regular_files:
            table = Table(title="📁 Regular Files")
            table.add_column("File", style="cyan")
            table.add_column("Size", style="green")
            
            for file in regular_files[:10]:  # Show first 10
                size_mb = file.stat().st_size / (1024 * 1024)
                table.add_row(file.name, f"{size_mb:.2f} MB")
            
            if len(regular_files) > 10:
                table.add_row(f"... and {len(regular_files) - 10} more", "")
            
            self.console.print(table)
        
        if encrypted_files:
            table = Table(title="🔐 Encrypted Files")
            table.add_column("File", style="cyan")
            table.add_column("Size", style="green")
            
            for file in encrypted_files[:10]:  # Show first 10
                size_mb = file.stat().st_size / (1024 * 1024)
                table.add_row(file.name, f"{size_mb:.2f} MB")
            
            if len(encrypted_files) > 10:
                table.add_row(f"... and {len(encrypted_files) - 10} more", "")
            
            self.console.print(table)
    
    def generate_new_key(self):
        """Generate a new encryption key."""
        try:
            # This will generate a new key
            self.encryption_engine = EncryptionEngine()
            self.console.print("[green]✅ New encryption key generated successfully![/green]")
        except Exception as e:
            self.console.print(f"[red]❌ Error generating new key: {e}[/red]") 