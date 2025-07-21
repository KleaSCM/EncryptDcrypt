#!/usr/bin/env python3
"""
EncryptDecrypt Launcher
======================

Launcher for the EncryptDecrypt system with mode selection.

Author: KleaSCM <KleaSCM@gmail.com>
"""

import sys
import subprocess
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
import colorlog
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = colorlog.getLogger()
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
))
logger.addHandler(handler)


class Launcher:
    """
    Launcher for EncryptDecrypt System
    
    Provides an interactive menu for launching different components.
    """
    
    def __init__(self):
        """Initialize the professional launcher."""
        self.console = Console()
        self.modes = {
            "gui": {
                "name": "Graphical User Interface",
                "description": "Launch the modern graphical interface",
                "command": None,  # Will be handled specially
                "icon": "🖥️"
            },
            "cli": {
                "name": "Command Line Interface",
                "description": "Launch the interactive CLI",
                "command": "python -m src.encryptdecrypt interactive",
                "icon": "💻"
            },
            "test": {
                "name": "Run Tests",
                "description": "Execute comprehensive test suite",
                "command": "python -m pytest tests/ -v",
                "icon": "🧪"
            },
            "install": {
                "name": "Install Dependencies",
                "description": "Install required packages",
                "command": "pip install -r requirements.txt",
                "icon": "📦"
            },
            "key": {
                "name": "Generate Key",
                "description": "Generate new encryption key",
                "command": "python -m src.encryptdecrypt key",
                "icon": "🔑"
            },
            "status": {
                "name": "System Status",
                "description": "Check system health and dependencies",
                "command": None,  # Will be handled specially
                "icon": "📊"
            },
            "help": {
                "name": "Help & Documentation",
                "description": "Show help information",
                "command": None,  # Will be handled specially
                "icon": "❓"
            }
        }
    
    def print_banner(self):
        """Display the beautiful welcome banner."""
        banner_text = Text()
        banner_text.append("EncryptDecrypt Launcher\n", style="bold blue")
        banner_text.append("Advanced File Encryption System\n", style="cyan")
        banner_text.append("Built by KleaSCM", style="green")
        
        panel = Panel(
            banner_text,
            border_style="blue",
            padding=(1, 2),
            title="Welcome"
        )
        self.console.print(panel)
    
    def print_menu(self):
        """Display the interactive mode selection menu."""
        menu_text = Text()
        menu_text.append("Available Modes:\n\n", style="bold")
        
        for mode, info in self.modes.items():
            menu_text.append(f"{info['icon']} {info['name']}\n", style="blue")
            menu_text.append(f"   {info['description']}\n", style="white")
            menu_text.append(f"   Command: {mode}\n\n", style="dim")
        
        menu_text.append("Select a mode to continue...", style="bold green")
        
        panel = Panel(
            menu_text,
            border_style="blue",
            padding=(1, 2),
            title="Mode Selection"
        )
        self.console.print(panel)
    
    def check_system_health(self):
        """Check system health and dependencies."""
        self.console.print("[bold blue]🔍 System Health Check[/bold blue]")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major >= 3 and python_version.minor >= 8:
            self.console.print(f"[green]✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}[/green]")
        else:
            self.console.print(f"[red]❌ Python {python_version.major}.{python_version.minor}.{python_version.micro} (3.8+ required)[/red]")
        
        # Check virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            self.console.print("[green]✅ Virtual environment active[/green]")
        else:
            self.console.print("[yellow]⚠️  No virtual environment detected[/yellow]")
        
        # Check key file
        if os.path.exists("key.txt"):
            self.console.print("[green]✅ Encryption key found[/green]")
        else:
            self.console.print("[yellow]⚠️  No encryption key found (will be generated)[/yellow]")
        
        # Check source directory
        if os.path.exists("src/encryptdecrypt"):
            self.console.print("[green]✅ Source code found[/green]")
        else:
            self.console.print("[red]❌ Source code not found[/red]")
        
        # Check requirements
        if os.path.exists("requirements.txt"):
            self.console.print("[green]✅ Requirements file found[/green]")
        else:
            self.console.print("[red]❌ Requirements file not found[/red]")
    
    def show_help(self):
        """Display comprehensive help information."""
        help_text = Text()
        help_text.append("EncryptDecrypt System Help\n\n", style="bold blue")
        help_text.append("Quick Start:\n", style="bold")
        help_text.append("1. Select 'Install Dependencies' to set up the environment\n", style="white")
        help_text.append("2. Select 'GUI' for graphical interface or 'CLI' for command line\n", style="white")
        help_text.append("3. Use 'Generate Key' to create a new encryption key\n\n", style="white")
        help_text.append("Features:\n", style="bold")
        help_text.append("• Advanced file encryption with AES-128-CBC\n", style="white")
        help_text.append("• Secure key management with PBKDF2\n", style="white")
        help_text.append("• File integrity verification with SHA-256\n", style="white")
        help_text.append("• Modern GUI with dark theme\n", style="white")
        help_text.append("• Rich CLI with progress tracking\n", style="white")
        help_text.append("• Batch processing capabilities\n\n", style="white")
        help_text.append("Security:\n", style="bold")
        help_text.append("• Files are replaced (not duplicated) during encryption\n", style="white")
        help_text.append("• 100,000 PBKDF2 iterations for key derivation\n", style="white")
        help_text.append("• Secure random key generation\n", style="white")
        help_text.append("• File hash verification for integrity\n", style="white")
        
        panel = Panel(
            help_text,
            border_style="blue",
            padding=(1, 2),
            title="Help & Documentation"
        )
        self.console.print(panel)
    
    def launch_mode(self, mode: str):
        """
        Launch the selected mode.
        
        Args:
            mode (str): Mode to launch
        """
        if mode not in self.modes:
            self.console.print(f"[red]❌ Unknown mode: {mode}[/red]")
            return
        
        mode_info = self.modes[mode]
        self.console.print(f"\n🚀 Launching: {mode_info['name']}")
        
        if mode == "gui":
            # Handle GUI specially - import and run directly
            try:
                print("Launching GUI directly...")
                from src.encryptdecrypt.gui.interface import ModernGUI
                gui = ModernGUI()
                gui.run()
                self.console.print(f"[green]✅ {mode_info['name']} completed successfully![/green]")
            except Exception as e:
                self.console.print(f"[red]❌ Error executing {mode_info['name']}: {str(e)}[/red]")
        elif mode == "status":
            # Handle status specially
            self.check_system_health()
        elif mode == "help":
            # Handle help specially
            self.show_help()
        elif mode_info["command"]:
            try:
                # Execute the command
                print(f"Executing: {mode_info['command']}")
                result = subprocess.run(
                    mode_info["command"].split(),
                    capture_output=False,
                    text=True
                )
                
                if result.returncode == 0:
                    self.console.print(f"[green]✅ {mode_info['name']} completed successfully![/green]")
                else:
                    self.console.print(f"[red]❌ {mode_info['name']} encountered an error.[/red]")
                    
            except FileNotFoundError:
                self.console.print(f"[red]❌ Error: Could not find required files for {mode_info['name']}[/red]")
                self.console.print("[yellow]💡 Try running 'Install Dependencies' first[/yellow]")
            except Exception as e:
                self.console.print(f"[red]❌ Error executing {mode_info['name']}: {str(e)}[/red]")
    
    def run(self):
        """Run the interactive launcher."""
        self.print_banner()
        
        while True:
            try:
                self.print_menu()
                mode = Prompt.ask(
                    "\n[bold blue]Select mode[/bold blue]",
                    choices=list(self.modes.keys()) + ["exit"],
                    default="gui"
                )
                
                if mode == "exit":
                    self.console.print("[green]Goodbye! 👋[/green]")
                    break
                
                self.launch_mode(mode)
                
                # Ask if user wants to continue
                if not Prompt.ask("\n[bold]Continue with another mode?[/bold]", choices=["y", "n"], default="y") == "y":
                    self.console.print("[green]Goodbye! 👋[/green]")
                    break
                    
            except KeyboardInterrupt:
                self.console.print("\n[green]Goodbye! 👋[/green]")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")


def main():
    """Main entry point for the launcher."""
    launcher = Launcher()
    launcher.run()


if __name__ == "__main__":
    main() 