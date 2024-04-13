from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()

# Save the key to key.txt
with open("key.txt", "wb") as key_file:
    key_file.write(key)

print("Key generated and saved to key.txt.")
