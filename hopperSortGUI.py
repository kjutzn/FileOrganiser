import os
import shutil
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox

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
class FileOrganizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HopperSort")
        self.setGeometry(100, 100, 400, 200)

        self.manual_button = QPushButton("Manual Input", self)
        self.manual_button.setGeometry(50, 50, 150, 50)
        self.manual_button.clicked.connect(self.manual_input)

        self.automatic_button = QPushButton("Automatic (Use Script Location)", self)
        self.automatic_button.setGeometry(200, 50, 150, 50)
        self.automatic_button.clicked.connect(self.automatic_input)

    def manual_input(self):
        source_directory = QFileDialog.getExistingDirectory(self, "Select the source directory")
        if source_directory:
            self.organize_files_by_extension(source_directory)
            QMessageBox.information(self, "Info", "File organization completed.")

    def automatic_input(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.organize_files_by_extension(script_directory)
        QMessageBox.information(self, "Info", "File organization completed.")

    def organize_files_by_extension(self, source_folder):
        for filename in os.listdir(source_folder):
            source_file = os.path.join(source_folder, filename)

            if os.path.isdir(source_file) or filename == '.DS_Store':
                continue

            file_extension = filename.split('.')[-1]

            if file_extension in file_extensions:
                destination_folder = os.path.join(source_folder, file_extensions[file_extension])
            else:
                destination_folder = os.path.join(source_folder, file_extension)

            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            destination_file = os.path.join(destination_folder, filename)
            shutil.move(source_file, destination_file)

def main():
    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
