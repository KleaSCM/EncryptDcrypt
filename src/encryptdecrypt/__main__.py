"""
Main entry point for the EncryptDecrypt package.

Author: KleaSCM <KleaSCM@gmail.com>
"""

import sys
import logging
from .gui.interface import ModernGUI
from .cli.interface import CLI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """
    Main application entry point.
    
    Launches the appropriate interface based on command line arguments.
    """
    if len(sys.argv) > 1:
        # CLI mode
        cli = CLI()
        
        command = sys.argv[1].lower()
        if command == "gui":
            # Launch GUI from CLI
            gui = ModernGUI()
            gui.run()
        elif command == "encrypt" and len(sys.argv) > 2:
            cli.encrypt_directory(sys.argv[2])
        elif command == "decrypt" and len(sys.argv) > 2:
            cli.decrypt_directory(sys.argv[2])
        elif command == "status" and len(sys.argv) > 2:
            cli.show_directory_status(sys.argv[2])
        elif command == "key":
            cli.generate_new_key()
        elif command == "help":
            cli.print_help()
        elif command == "interactive":
            cli.run_interactive()
        else:
            cli.print_help()
    else:
        # Default to GUI mode
        try:
            gui = ModernGUI()
            gui.run()
        except Exception as e:
            logger.error(f"GUI error: {e}")
            print(f"Error starting GUI: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main() 