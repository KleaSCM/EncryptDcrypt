Encrypt/Decrypt: A Python-based Automation Tool
Overview
Encrypt/Decrypt is a Python-based automation tool designed to streamline repetitive tasks such as encrypting/decrypting files, creating protected Excel and Word documents with random data, and processing CSV files into Excel format. The tool leverages Python libraries to provide a comprehensive solution for automating file protection and data generation workflows.

Features
File Encryption/Decryption: Encrypt and decrypt files using the cryptography library.
Excel and Word Document Generation: Create Excel and Word documents with random data and protect them with passwords.
Key Generation: Generate and save encryption keys for secure file encryption and decryption.

Installation



Clone the Repository:

git clone https://github.com/your-username/Encrypt-Decrypt.git
cd Encrypt-Decrypt

Install Dependencies:

pip install -r requirements.txt

Generate Encryption Key:

python generate_key.py

Usage:

Encryption and Decryption
Encrypt Files
Create a files Directory
mkdir files

Place the Files to be Encrypted in the files Directory:

Run the Encryption Script
python encrypt_files.py

Decrypt Files:

Ensure the Encrypted Files are in the files Directory:
Run the Decryption Script
python decrypt_files.py

Create Protected Excel and Word Documents:

Run the Main Script to Generate Documents
python main.py
