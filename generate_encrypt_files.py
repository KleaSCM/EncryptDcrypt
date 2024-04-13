import os
import random
import string
import openpyxl
import win32com.client as win32

# Function to generate a random string of alphanumeric characters
def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to create an Excel file with random data in each cell and protect it with a password
def create_protected_excel(directory, filename, password):
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Fill cells with random data
    for row in range(1, 101):
        for col in range(1, 101):
            sheet.cell(row=row, column=col).value = generate_random_string(8)

    # Protect the worksheet with a password
    sheet.protection.password = password

    # Save the workbook with the correct extension
    filepath = os.path.join(directory, filename)
    workbook.save(filepath)

    print(f"Excel file '{filename}' created and protected with password.")

# Function to create a Word document with random data in each paragraph and protect it with a password
def create_protected_word(directory, filename, password):
    word = win32.Dispatch("Word.Application")
    doc = word.Documents.Add()

    # Add paragraphs with random data
    for _ in range(100):
        doc.Content.InsertAfter(generate_random_string(50) + "\n")

    # Save and encrypt the document with a password
    filepath = os.path.join(directory, filename)
    doc.SaveAs2(filepath, Password=password, AddToRecentFiles=False)
    doc.Close()

    print(f"Word document '{filename}' created and protected with password.")

    # Quit Word application
    word.Quit()

# Main function
def main():
    # Set the directory for encrypted files
    directory = os.path.join(os.getcwd(), "files")
    if not os.path.exists(directory):
        os.makedirs(directory)

    # World of Warcraft characters
    wow_characters = [
        "file",
        "file1",
        "file2",
        "file3",
        #add more files as needed name them as desired // need to have 20 files, see below v
    ]

    # Generate Excel files and protect them with passwords
    for character in wow_characters:
        password = generate_random_string(20)  # Generate a random password
        create_protected_excel(directory, f"{character}_excel.xlsx", password)

    # Generate Word documents and protect them with passwords
    for character in wow_characters:
        password = generate_random_string(20)  # Generate a random password
        create_protected_word(directory, f"{character}_word.docx", password)

if __name__ == "__main__":
    main()
