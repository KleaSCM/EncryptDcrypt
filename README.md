# EncryptDcrypt - Advanced File Encryption System

EncryptDcrypt is a robust, modular encryption platform for secure file encryption, batch processing, benchmarking, and analytics. It features a modern, menu-driven CLI, an optional GUI, and comprehensive reporting—all in a single, unified system.

---

## Features

- **Fernet (AES) encryption** with PBKDF2 key derivation and SHA-256 integrity verification
- **Unified CLI** for encryption, decryption, benchmarking, metrics, and file analysis
- **Optional GUI** (CustomTkinter) for users who prefer a graphical workflow
- **Benchmarking and metrics**: Real-time performance measurement, file type analysis, and integrity checks
- **Key management**: Secure, automated key generation and rotation
- **Safe defaults**: Sensitive files, test data, and metrics are excluded from version control

---

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/EncryptDcrypt.git
   cd EncryptDcrypt
   ```
2. **Install dependencies:**
   - CLI only:
     ```bash
     pip install -r requirements.txt
     ```
   - For GUI (optional):
     - On Arch Linux:
       ```bash
       sudo pacman -S python-customtkinter
       ```
     - Or (in a venv):
       ```bash
       pip install customtkinter
       ```
3. **Run the CLI:**
   ```bash
   ./EncryptDcrypt
   # or
   python3 EncryptDcrypt
   ```

---

## Usage

### CLI Menu
- Encrypt/decrypt single files or directories
- Run system tests
- Benchmark with real performance metrics
- View metrics and analytics
- Analyze files (type breakdown, size, largest files)
- Launch GUI (if CustomTkinter is installed)
- Help and usage information

#### Example CLI Session
```
$ ./EncryptDcrypt
1. Encrypt File/Directory
2. Decrypt File/Directory
3. Run System Test
4. Run Benchmark
5. View Metrics
6. View Summary
7. Analyze Files
8. Launch GUI
9. Help
0. Exit
```

### Optional GUI
- Launch from CLI menu (option 8)
- Requires `customtkinter`
- Dark mode, drag-and-drop, real-time progress

---

## File Structure

```
EncryptDcrypt/
├── EncryptDcrypt           # Main CLI launcher (executable)
├── src/
│   └── encryptdecrypt/
│       ├── cli/            # CLI interface code
│       ├── gui/            # GUI interface code (optional)
│       ├── core/           # Encryption engine
│       └── utils/          # Utility functions
├── metrics/                # Benchmark results (ignored by git)
├── Folderwithstuff/        # Test data (ignored by git)
├── key.txt                 # Encryption key (ignored by git)
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

---

## Technical Details

- **Encryption**: Fernet (AES-128, CBC, PKCS7), PBKDF2 (SHA-256, 100k iterations)
- **Key management**: Auto-generated, stored in `key.txt` (never commit this)
- **Benchmarking**: Encrypts/decrypts sample files, measures speed, verifies integrity
- **Metrics**: Saved in `metrics/benchmark_results.json` (ignored by git)
- **File analysis**: Type breakdown, size distribution, largest files
- **Error handling**: All errors are caught and shown with clear messages

---

## Security Considerations

- **Key storage**: `key.txt` is sensitive—keep it safe, never commit
- **Key rotation**: Use the CLI to generate a new key (old files become unreadable)
- **Integrity**: All encryption/decryption is verified with SHA-256
- **Best practices**: Always backup your key, test decryption before deleting originals

---
