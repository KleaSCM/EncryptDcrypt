"""
EncryptDecrypt - Advanced File Encryption System
===============================================
file encryption system with GUI and CLI interfaces.
Built with security, performance, and user experience in mind.

Author: KleaSCM <KleaSCM@gmail.com>
Version: 2.0.0
"""

__version__ = "2.0.0"
__author__ = "KleaSCM <KleaSCM@gmail.com>"
__description__ = "Advanced File Encryption System"

from .core.engine import EncryptionEngine
from .cli.interface import CLI

# GUI import is optional to avoid dependency issues
try:
    from .gui.interface import ModernGUI
    GUI_AVAILABLE = True
except ImportError:
    ModernGUI = None
    GUI_AVAILABLE = False

__all__ = [
    "EncryptionEngine",
    "CLI",
    "__version__",
    "__author__",
    "__description__"
]

# Add GUI to __all__ only if available
if GUI_AVAILABLE:
    __all__.append("ModernGUI") 