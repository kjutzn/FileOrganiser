import os
import shutil
import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QVBoxLayout, QWidget, \
    QLabel
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QFont
from offline import dictionary
import json
import pyi_splash


def fetch_file_extensions():
    github_url = 'https://raw.githubusercontent.com/yourusername/yourrepository/master/file_extensions.json'
    response = requests.get(github_url)

    try:
        response.raise_for_status()

        file_extensions = response.json()

        if isinstance(file_extensions, dict):
            return file_extensions
        else:
            print("GitHub response is not a valid dictionary")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON decoding error occurred: {json_err}")

    return dictionary.file_extensions                    #to do: add local last fetched

file_extensions = fetch_file_extensions()


def create_log_file():
    current_datetime = QDateTime.currentDateTime()
    log_filename = f"logs/log_{current_datetime.toString('yyyy-MM-dd_hh-mm-ss')}.txt"
    log_file = open(log_filename, "w")
    return log_file, log_filename

class FileOrganizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.log_file, self.log_filename = create_log_file()
        self.log(f"Debug log  {self.log_filename}\n")

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
            self.log(f"Manual Input - Source Directory: {source_directory}\n")
            self.organize_files_by_extension(source_directory)
            QMessageBox.information(self, "Info", "File organization completed.")

    def organize_files_on_desktop(self):
        desktop_path = os.path.expanduser("~/Desktop")
        self.log(f"Organize Files on Desktop - Source Directory: {desktop_path}\n")
        self.organize_files_by_extension(desktop_path)
        QMessageBox.information(self, "Info", "File organization on Desktop completed.")

    def organize_files_in_downloads(self):
        downloads_path = os.path.expanduser("~/Downloads")
        self.log(f"Organize Files in Downloads - Source Directory: {downloads_path}\n")
        self.organize_files_by_extension(downloads_path)
        QMessageBox.information(self, "Info", "File organization in Downloads completed.")

    def organize_files_in_documents(self):
        documents_path = os.path.expanduser("~/Documents")
        self.log(f"Organize Files in Documents - Source Directory: {documents_path}\n")
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
            self.log(f"Moved {source_file} to {destination_file}\n")

    def log(self, message):
        with open(self.log_filename, "a") as log_file:
            log_file.write(message)

    def resizeEvent(self, event):
        new_font_size = int(event.size().width() / 10)
        self.label_font.setPointSize(new_font_size)
        self.label.setFont(self.label_font)

def main():
    pyi_splash.close()
    if not os.path.exists("logs"):
        os.makedirs("logs")

    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
