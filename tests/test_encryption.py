#!/usr/bin/env python3
"""
🧪 EncryptDecrypt Test Suite 🧪
==============================

test suite for the advanced encryption system.
Tests all functionality with comprehensive coverage and beautiful output! ✨

Author: Yuriko
Features:
- Comprehensive unit tests
- Integration tests
- Performance benchmarks
- Beautiful test output with Rich
- Mock file system testing
"""

import os
import sys
import tempfile
import shutil
import time
import hashlib
from pathlib import Path
from typing import List, Dict
import unittest
from unittest.mock import patch, MagicMock

# Rich imports for beautiful test output
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel
from rich.text import Text

# Import our encryption system
from main import EncryptionEngine
from cli import BeautifulCLI

# Configure beautiful test output
console = Console()

class BeautifulTestRunner:
    """
    🌸 Beautiful Test Runner
    
    A stunning test runner with rich formatting and detailed reporting!
    """
    
    def __init__(self):
        """Initialize the beautiful test runner."""
        self.console = Console()
        self.test_results = []
        self.start_time = None
        
    def print_banner(self):
        """Display beautiful test banner."""
        banner_text = Text()
        banner_text.append("🧪 ", style="bold magenta")
        banner_text.append("EncryptDecrypt Test Suite", style="bold cyan")
        banner_text.append(" 🧪", style="bold magenta")
        banner_text.append("\nComprehensive Testing with Love", style="italic green")
        banner_text.append("\nBuilt by Yuriko 💕", style="italic pink")
        
        panel = Panel(
            banner_text,
            border_style="magenta",
            padding=(1, 2),
            title="Testing in Progress! ✨"
        )
        self.console.print(panel)
    
    def run_tests(self):
        """Run all tests with beautiful progress tracking."""
        self.start_time = time.time()
        self.print_banner()
        
        # Discover and run tests
        loader = unittest.TestLoader()
        suite = loader.discover('.', pattern='test_*.py')
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Running tests...", total=suite.countTestCases())
            
            runner = unittest.TextTestRunner(verbosity=2, stream=open(os.devnull, 'w'))
            result = runner.run(suite)
            
            # Update progress for each test
            for test in suite:
                if hasattr(test, '_tests'):
                    for subtest in test._tests:
                        if hasattr(subtest, '_tests'):
                            for actual_test in subtest._tests:
                                progress.advance(task)
                        else:
                            progress.advance(task)
                else:
                    progress.advance(task)
        
        # Display results
        self.display_results(result)
        
        return result.wasSuccessful()
    
    def display_results(self, result):
        """Display beautiful test results."""
        end_time = time.time()
        duration = end_time - self.start_time
        
        # Create results table
        table = Table(title="🧪 Test Results Summary")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Count", style="magenta")
        table.add_column("Status", style="green")
        
        total_tests = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)
        skipped = len(result.skipped) if hasattr(result, 'skipped') else 0
        passed = total_tests - failures - errors - skipped
        
        # Calculate percentages
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        fail_rate = (failures / total_tests * 100) if total_tests > 0 else 0
        error_rate = (errors / total_tests * 100) if total_tests > 0 else 0
        
        table.add_row("✅ Passed", str(passed), f"{pass_rate:.1f}%")
        table.add_row("❌ Failed", str(failures), f"{fail_rate:.1f}%")
        table.add_row("⚠️  Errors", str(errors), f"{error_rate:.1f}%")
        table.add_row("⏭️  Skipped", str(skipped), "N/A")
        table.add_row("📊 Total", str(total_tests), "100.0%")
        table.add_row("⏱️  Duration", f"{duration:.2f}s", "N/A")
        
        self.console.print(table)
        
        # Show detailed results if there are failures
        if failures > 0 or errors > 0:
            self.show_detailed_failures(result)
        
        # Overall status
        if result.wasSuccessful():
            self.console.print("[green]🎉 All tests passed successfully![/green]")
        else:
            self.console.print("[red]❌ Some tests failed. Please review the details above.[/red]")
    
    def show_detailed_failures(self, result):
        """Show detailed failure information."""
        if result.failures:
            self.console.print("\n[bold red]❌ Test Failures:[/bold red]")
            for test, traceback in result.failures:
                self.console.print(f"[red]• {test}: {traceback.split('AssertionError:')[-1].strip()}[/red]")
        
        if result.errors:
            self.console.print("\n[bold red]⚠️  Test Errors:[/bold red]")
            for test, traceback in result.errors:
                self.console.print(f"[red]• {test}: {traceback.split('Exception:')[-1].strip()}[/red]")

class TestEncryptionEngine(unittest.TestCase):
    """
    🔐 Encryption Engine Tests
    
    Comprehensive tests for the encryption engine functionality.
    """
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.engine = EncryptionEngine()
        
        # Create test files
        self.test_files = []
        for i in range(5):
            test_file = os.path.join(self.temp_dir, f"test_file_{i}.txt")
            with open(test_file, 'w') as f:
                f.write(f"Test content for file {i}\n" * 100)
            self.test_files.append(test_file)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_key_generation(self):
        """Test encryption key generation."""
        console.print("🔑 Testing key generation...")
        
        # Test that key is generated
        self.assertIsNotNone(self.engine.fernet)
        
        # Test key format (Fernet keys are base64-encoded)
        key = self.engine.fernet._encryption_key
        self.assertEqual(len(key), 32)  # 256-bit key
        
        console.print("[green]✅ Key generation test passed[/green]")
    
    def test_file_encryption(self):
        """Test file encryption functionality."""
        console.print("🔐 Testing file encryption...")
        
        test_file = self.test_files[0]
        
        # Calculate original hash
        original_hash = self.engine.calculate_file_hash(test_file)
        
        # Encrypt file
        result = self.engine.encrypt_file(test_file, preserve_original=True)
        
        # Verify encryption was successful
        self.assertEqual(result["status"], "success")
        self.assertTrue(os.path.exists(result["encrypted_path"]))
        
        # Verify original file still exists
        self.assertTrue(os.path.exists(test_file))
        
        # Verify encrypted file is different
        encrypted_hash = self.engine.calculate_file_hash(result["encrypted_path"])
        self.assertNotEqual(original_hash, encrypted_hash)
        
        console.print("[green]✅ File encryption test passed[/green]")
    
    def test_file_decryption(self):
        """Test file decryption functionality."""
        console.print("🔓 Testing file decryption...")
        
        test_file = self.test_files[1]
        
        # Encrypt file first
        encrypt_result = self.engine.encrypt_file(test_file, preserve_original=True)
        self.assertEqual(encrypt_result["status"], "success")
        
        # Decrypt file
        decrypt_result = self.engine.decrypt_file(encrypt_result["encrypted_path"], preserve_encrypted=True)
        
        # Verify decryption was successful
        self.assertEqual(decrypt_result["status"], "success")
        self.assertTrue(os.path.exists(decrypt_result["decrypted_path"]))
        
        # Verify decrypted content matches original
        with open(test_file, 'rb') as f1, open(decrypt_result["decrypted_path"], 'rb') as f2:
            self.assertEqual(f1.read(), f2.read())
        
        console.print("[green]✅ File decryption test passed[/green]")
    
    def test_integrity_verification(self):
        """Test file integrity verification."""
        console.print("🔍 Testing integrity verification...")
        
        test_file = self.test_files[2]
        
        # Calculate hash
        original_hash = self.engine.calculate_file_hash(test_file)
        
        # Verify hash is consistent
        hash_again = self.engine.calculate_file_hash(test_file)
        self.assertEqual(original_hash, hash_again)
        
        # Verify hash format (SHA-256 produces 64-character hex string)
        self.assertEqual(len(original_hash), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in original_hash))
        
        console.print("[green]✅ Integrity verification test passed[/green]")
    
    def test_password_key_derivation(self):
        """Test password-based key derivation."""
        console.print("🔑 Testing password key derivation...")
        
        password = "MySecurePassword123!"
        
        # Derive key from password
        key, salt = self.engine.derive_key_from_password(password)
        
        # Verify key format
        self.assertEqual(len(key), 44)  # Base64-encoded 32-byte key
        self.assertEqual(len(salt), 16)  # 128-bit salt
        
        # Verify key is different with different salt
        key2, salt2 = self.engine.derive_key_from_password(password)
        self.assertNotEqual(key, key2)
        self.assertNotEqual(salt, salt2)
        
        console.print("[green]✅ Password key derivation test passed[/green]")
    
    def test_error_handling(self):
        """Test error handling for invalid operations."""
        console.print("⚠️  Testing error handling...")
        
        # Test decryption of non-encrypted file
        test_file = self.test_files[3]
        result = self.engine.decrypt_file(test_file, preserve_encrypted=True)
        self.assertEqual(result["status"], "error")
        
        # Test encryption of non-existent file
        result = self.engine.encrypt_file("/non/existent/file.txt", preserve_original=True)
        self.assertEqual(result["status"], "error")
        
        console.print("[green]✅ Error handling test passed[/green]")
    
    def test_batch_processing(self):
        """Test batch processing of multiple files."""
        console.print("📦 Testing batch processing...")
        
        results = []
        for test_file in self.test_files:
            result = self.engine.encrypt_file(test_file, preserve_original=True)
            results.append(result)
        
        # Verify all files were processed
        self.assertEqual(len(results), len(self.test_files))
        
        # Verify all operations were successful
        successful = sum(1 for r in results if r["status"] == "success")
        self.assertEqual(successful, len(self.test_files))
        
        console.print("[green]✅ Batch processing test passed[/green]")

class TestBeautifulCLI(unittest.TestCase):
    """
    🌸 Beautiful CLI Tests
    
    Tests for the command-line interface functionality.
    """
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.cli = BeautifulCLI()
        
        # Create test files
        for i in range(3):
            test_file = os.path.join(self.temp_dir, f"cli_test_{i}.txt")
            with open(test_file, 'w') as f:
                f.write(f"CLI test content {i}\n" * 50)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_directory_analysis(self):
        """Test directory analysis functionality."""
        console.print("📊 Testing directory analysis...")
        
        # Test with regular files
        files = self.cli.get_files_in_directory(self.temp_dir)
        self.assertEqual(len(files), 3)
        
        # Test with no encrypted files
        encrypted_files = self.cli.get_files_in_directory(self.temp_dir, encrypted_only=True)
        self.assertEqual(len(encrypted_files), 0)
        
        console.print("[green]✅ Directory analysis test passed[/green]")
    
    def test_cli_encryption(self):
        """Test CLI encryption functionality."""
        console.print("🔐 Testing CLI encryption...")
        
        result = self.cli.encrypt_directory(self.temp_dir, preserve_original=True)
        
        # Verify encryption was performed
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["processed"], 3)
        self.assertEqual(result["successful"], 3)
        self.assertEqual(result["failed"], 0)
        
        console.print("[green]✅ CLI encryption test passed[/green]")
    
    def test_cli_decryption(self):
        """Test CLI decryption functionality."""
        console.print("🔓 Testing CLI decryption...")
        
        # First encrypt files
        self.cli.encrypt_directory(self.temp_dir, preserve_original=True)
        
        # Then decrypt them
        result = self.cli.decrypt_directory(self.temp_dir, preserve_encrypted=True)
        
        # Verify decryption was performed
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["processed"], 3)
        self.assertEqual(result["successful"], 3)
        self.assertEqual(result["failed"], 0)
        
        console.print("[green]✅ CLI decryption test passed[/green]")

class TestPerformance(unittest.TestCase):
    """
    ⚡ Performance Tests
    
    Tests for system performance and optimization.
    """
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.engine = EncryptionEngine()
        
        # Create large test file
        self.large_file = os.path.join(self.temp_dir, "large_test.txt")
        with open(self.large_file, 'w') as f:
            f.write("Large test content\n" * 10000)  # ~200KB file
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_large_file_encryption(self):
        """Test encryption of large files."""
        console.print("📁 Testing large file encryption...")
        
        start_time = time.time()
        result = self.engine.encrypt_file(self.large_file, preserve_original=True)
        end_time = time.time()
        
        # Verify encryption was successful
        self.assertEqual(result["status"], "success")
        
        # Verify reasonable performance (should complete in under 5 seconds)
        duration = end_time - start_time
        self.assertLess(duration, 5.0)
        
        console.print(f"[green]✅ Large file encryption test passed ({duration:.2f}s)[/green]")
    
    def test_memory_usage(self):
        """Test memory usage during operations."""
        console.print("💾 Testing memory usage...")
        
        # This is a basic test - in a real scenario you'd use memory_profiler
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Perform encryption
        result = self.engine.encrypt_file(self.large_file, preserve_original=True)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Verify reasonable memory usage (should not increase by more than 50MB)
        self.assertLess(memory_increase, 50 * 1024 * 1024)  # 50MB
        
        console.print(f"[green]✅ Memory usage test passed (+{memory_increase / 1024 / 1024:.1f}MB)[/green]")

def run_performance_benchmarks():
    """
    🏃‍♀️ Run Performance Benchmarks
    
    Run comprehensive performance benchmarks with beautiful output.
    """
    console.print("\n[bold cyan]🏃‍♀️ Performance Benchmarks[/bold cyan]")
    
    # Create test data
    temp_dir = tempfile.mkdtemp()
    engine = EncryptionEngine()
    
    try:
        # Test different file sizes
        file_sizes = [1024, 10240, 102400, 1048576]  # 1KB, 10KB, 100KB, 1MB
        
        table = Table(title="⚡ Performance Benchmark Results")
        table.add_column("File Size", style="cyan")
        table.add_column("Encryption Time", style="green")
        table.add_column("Decryption Time", style="blue")
        table.add_column("Throughput (MB/s)", style="magenta")
        
        for size in file_sizes:
            # Create test file
            test_file = os.path.join(temp_dir, f"benchmark_{size}.txt")
            with open(test_file, 'w') as f:
                f.write("A" * size)
            
            # Benchmark encryption
            start_time = time.time()
            encrypt_result = engine.encrypt_file(test_file, preserve_original=True)
            encrypt_time = time.time() - start_time
            
            # Benchmark decryption
            start_time = time.time()
            decrypt_result = engine.decrypt_file(encrypt_result["encrypted_path"], preserve_encrypted=True)
            decrypt_time = time.time() - start_time
            
            # Calculate throughput
            throughput = (size / 1024 / 1024) / encrypt_time if encrypt_time > 0 else 0
            
            table.add_row(
                f"{size / 1024:.1f} KB",
                f"{encrypt_time:.3f}s",
                f"{decrypt_time:.3f}s",
                f"{throughput:.1f} MB/s"
            )
        
        console.print(table)
        
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    """
    🧪 Main test runner
    
    Run all tests with beautiful output and comprehensive reporting.
    """
    # Run unit tests
    test_runner = BeautifulTestRunner()
    success = test_runner.run_tests()
    
    # Run performance benchmarks
    run_performance_benchmarks()
    
    # Final status
    if success:
        console.print("\n[bold green]🎉 All tests completed successfully![/bold green]")
        console.print("[green]✨ Your encryption system is working perfectly![/green]")
    else:
        console.print("\n[bold red]❌ Some tests failed. Please review the output above.[/bold red]")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 