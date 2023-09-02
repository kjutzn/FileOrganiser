import os
import shutil

file_extensions = {
    'pdf'  : 'PDFs',
    'png'  : 'Images',
    'jpg'  : 'Images',
    'jpeg' : 'Images',
    'gif'  : 'Images',
    'doc'  : 'Documents',
    'docx' : 'Documents',
    'txt'  : 'Documents',
    'zip'  : 'Archives',
    'rar'  : 'Archives',
    'exe'  : 'Programs',
    'mp3'  : 'Music',
    'wav'  : 'Music',
    'mp4'  : 'Videos',
    'avi'  : 'Videos',
    'flv'  : 'Videos',
    'pkg'  : 'Mac Installers',
    'dmg'  : 'macOS Disk Images',
    'deb'  : 'Debian Software Packages / iOS tweak',
    'm4a'  : 'MPEG-4 Audio Files',
    'tipa' : 'TrollStore Application',
    'ipa'  : 'iOS App',
    '7zip' : 'Archives'
}

def rename_directory(old_name, new_name):

    os.rename(old_name, new_name)
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def organize_files_by_extension(source_folder):

    for filename in os.listdir(source_folder):
        source_file = os.path.join(source_folder, filename)

        if os.path.isdir(source_file) or filename == '.DS_Store':
            continue

        file_extension = filename.split('.')[-1]

        if file_extension in file_extensions:
            destination_folder = os.path.join(source_folder, file_extensions[file_extension])
        else:
            destination_folder = os.path.join(source_folder, file_extension)

        # Create the destination folder if it doesn't exist
        create_directory(destination_folder)

        # Move the file to the destination folder
        destination_file = os.path.join(destination_folder, filename)
        shutil.move(source_file, destination_file)


if __name__ == "__main__":
    source_directory = input("Enter path of source folder: ")

    if os.path.exists(source_directory):
        organize_files_by_extension(source_directory)
        print("Finished! Thank you for using this script.")
    else:
        print("Source Folder not found!")
