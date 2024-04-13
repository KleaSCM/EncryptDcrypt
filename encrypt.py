import os
from cryptography.fernet import Fernet

# Function to read the encryption key from key.txt
def load_key():
    with open("key.txt", "rb") as key_file:
        return key_file.read()

# Function to encrypt a file
def encrypt_file(file_path, key):
    # Read the file content
    with open(file_path, "rb") as file:
        data = file.read()

    # Encrypt the data
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data)

    # Write the encrypted data back to the file
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

# Main function
def main_encrypt():
    # Load the encryption key
    key = load_key()

    # Encrypt all files in the 'files' directory
    directory = os.path.join(os.getcwd(), "files")
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            encrypt_file(filepath, key)

    print("Encryption completed.")

if __name__ == "__main__":
    main_encrypt()
