# EncryptDecrypt Documentation

## Overview

EncryptDecrypt is an advanced file encryption system built with security, performance, and user experience in mind. It provides both graphical and command-line interfaces for encrypting and decrypting files.

## Architecture

### Core Components

- **`src/encryptdecrypt/core/`** - Core encryption engine and algorithms
- **`src/encryptdecrypt/gui/`** - Graphical user interface components
- **`src/encryptdecrypt/cli/`** - Command-line interface components
- **`src/encryptdecrypt/utils/`** - Utility functions and helpers

### Key Features

- **AES-128-CBC Encryption**: Industry-standard symmetric encryption
- **PBKDF2 Key Derivation**: Secure password-based key generation
- **SHA-256 Integrity**: File hash verification for data integrity
- **File Replacement**: Files are replaced (not duplicated) during encryption
- **Batch Processing**: Process multiple files simultaneously
- **Modern UI**: Dark-themed GUI with progress tracking
- **Rich CLI**: Beautiful terminal interface with progress bars

## Security

### Encryption Algorithm
- **Algorithm**: AES-128 in CBC mode with PKCS7 padding
- **Key Derivation**: PBKDF2 with SHA-256 and 100,000 iterations
- **Salt**: 128-bit random salt for each key derivation
- **Integrity**: SHA-256 hash verification

### Key Management
- Keys are stored securely in `key.txt`
- Automatic key generation on first run
- Support for password-based key derivation
- Key rotation capabilities

## Usage

### GUI Mode
```bash
python launcher.py
# Select "GUI" from the menu
```

### CLI Mode
```bash
# Interactive CLI
python -m src.encryptdecrypt interactive

# Direct commands
python -m src.encryptdecrypt encrypt /path/to/files
python -m src.encryptdecrypt decrypt /path/to/files
python -m src.encryptdecrypt status /path/to/check
```

### Launcher
```bash
python launcher.py
# Interactive menu with all options
```

## Development

### Project Structure
```
EncryptDecrypt/
├── src/encryptdecrypt/          # Main package
│   ├── core/                    # Core encryption engine
│   ├── gui/                     # GUI components
│   ├── cli/                     # CLI components
│   ├── utils/                   # Utility functions
│   └── __main__.py             # Entry point
├── tests/                       # Test suite
├── docs/                        # Documentation
├── examples/                    # Example files
├── launcher.py                  # Interactive launcher
├── setup.py                     # Package setup
├── pyproject.toml              # Modern Python packaging
└── requirements.txt            # Dependencies
```

### Running Tests
```bash
pytest tests/ -v
```

### Building Package
```bash
pip install build
python -m build
```

## Configuration

The system uses `config.yaml` for configuration:

```yaml
encryption:
  algorithm: "AES-128-CBC"
  key_derivation: "PBKDF2"
  iterations: 100000
  salt_size: 16

interface:
  theme: "dark"
  language: "en"
  auto_save: true

security:
  preserve_originals: false
  verify_integrity: true
  secure_delete: false
```

## API Reference

### Core Engine

```python
from encryptdecrypt.core.engine import EncryptionEngine

# Initialize engine
engine = EncryptionEngine()

# Encrypt file
result = engine.encrypt_file("file.txt")

# Decrypt file
result = engine.decrypt_file("file.txt")
```

### GUI Interface

```python
from encryptdecrypt.gui.interface import ModernGUI

# Launch GUI
gui = ModernGUI()
gui.run()
```

### CLI Interface

```python
from encryptdecrypt.cli.interface import ProfessionalCLI

# Launch CLI
cli = ProfessionalCLI()
cli.run_interactive()
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 