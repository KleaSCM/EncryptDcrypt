import os
from cryptography.fernet import Fernet

# Function to read the encryption key from key.txt
def load_key():
    with open("key.txt", "rb") as key_file:
        return key_file.read()

# Function to decrypt a file
def decrypt_file(file_path, key):
    # Read the encrypted data from the file
    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    # Decrypt the data
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data)

    # Write the decrypted data back to the file
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

# Main function
def main_decrypt():
    # Load the encryption key
    key = load_key()

    # Decrypt all files in the 'files' directory
    directory = os.path.join(os.getcwd(), "files")
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            decrypt_file(filepath, key)

    print("Decryption completed.")

if __name__ == "__main__":
    main_decrypt()
