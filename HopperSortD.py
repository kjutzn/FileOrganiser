import os
import shutil
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

file_extensions = {
    'pdf': 'PDFs',
    'png': 'Images',
    'jpg': 'Images',
    'jpeg': 'Images',
    'gif': 'Images',
    'doc': 'Documents',
    'docx': 'Documents',
    'txt': 'Documents',
    'zip': 'Archives',
    'rar': 'Archives',
    'exe': 'Programs',
    'mp3': 'Music',
    'wav': 'Music',
    'mp4': 'Videos',
    'avi': 'Videos',
    'flv': 'Videos',
    'dmg': 'macOS Disk Images',
    'deb': 'Debian Software Packages / iOS tweak',
    'm4a': 'MPEG-4 Audio Files',
    'tipa': 'TrollStore Application',
    'ipa': 'iOS App',
    '7zip': 'Archives',
    'pkg': 'Package file',
    'tar.gz': 'Tarball compressed file',
    'bin': 'Binary disc image',
    'iso': 'ISO disk image',
    'toast': 'Toast disk image',
    'vcd': 'Virtual CD',
    'csv': 'Comma separated value file',
    'dat': 'Data file',
    'db': 'Database file',
    'log': 'Log files',
    'mdb': 'Microsoft Access database file',
    'sav': 'Save files',
    'sql': 'SQL database file',
    'tar': 'Linux-Unix Tarball File Archive',
    'xml': 'XML file',
    'apk': 'Android package file',
    'bat': 'Batch File',
    'py': 'Python files',
    'fnt': 'Fonts',
    'fon': 'Fonts',
    'otf': 'Fonts',
    'ttf': 'Fonts',
    'bmp': 'Images',
    'ico': 'Icons',
    'webp': 'Images'
}

class FileOrganizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hopper Sort")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        self.label_font = QFont()
        self.label_font.setPointSize(100)
        self.label_font.setBold(True)
        self.label_font.setFamily("Sedgwick Ave Display")

        self.label = QLabel("Hopper Sort", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(self.label_font)
        layout.addWidget(self.label)

        self.manual_button = QPushButton("Manual Path", self)
        font = QFont(self.manual_button.font())
        font.setPointSize(font.pointSize() + 2)
        self.manual_button.setFont(font)
        layout.addWidget(self.manual_button)

        # Add buttons for desktop, downloads, and documents
        self.desktop_button = QPushButton("Desktop", self)
        self.downloads_button = QPushButton("Downloads", self)
        self.documents_button = QPushButton("Documents", self)

        layout.addWidget(self.desktop_button)
        layout.addWidget(self.downloads_button)
        layout.addWidget(self.documents_button)

        central_widget.setLayout(layout)

        self.manual_button.clicked.connect(self.manual_input)
        self.desktop_button.clicked.connect(self.organize_files_on_desktop)
        self.downloads_button.clicked.connect(self.organize_files_in_downloads)
        self.documents_button.clicked.connect(self.organize_files_in_documents)

    def manual_input(self):
        source_directory = QFileDialog.getExistingDirectory(self, "Select the source directory")
        if source_directory:
            self.organize_files_by_extension(source_directory)
            QMessageBox.information(self, "Info", "File organization completed.")

    def organize_files_on_desktop(self):
        desktop_path = os.path.expanduser("~/Desktop")
        self.organize_files_by_extension(desktop_path)
        QMessageBox.information(self, "Info", "File organization on Desktop completed.")

    def organize_files_in_downloads(self):
        downloads_path = os.path.expanduser("~/Downloads")
        self.organize_files_by_extension(downloads_path)
        QMessageBox.information(self, "Info", "File organization in Downloads completed.")

    def organize_files_in_documents(self):
        documents_path = os.path.expanduser("~/Documents")
        self.organize_files_by_extension(documents_path)
        QMessageBox.information(self, "Info", "File organization in Documents completed.")

    def organize_files_by_extension(self, source_folder):
        for filename in os.listdir(source_folder):
            source_file = os.path.join(source_folder, filename)

            if os.path.isdir(source_file) or filename == '.DS_Store':
                continue

            file_extension = filename.split('.')[-1]

            if file_extension in file_extensions:
                destination_folder_name = file_extensions[file_extension]
            else:
                destination_folder_name = file_extension

            destination_folder = os.path.join(source_folder, destination_folder_name)

            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            destination_file = os.path.join(destination_folder, filename)
            shutil.move(source_file, destination_file)

    def resizeEvent(self, event):
        new_font_size = int(event.size().width() / 10)
        self.label_font.setPointSize(new_font_size)
        self.label.setFont(self.label_font)

def main():
    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
