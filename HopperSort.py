import os
import shutil
import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import json

local_version = "1.3"
file_extensions = None

def latest_version():
    github_url = 'https://raw.githubusercontent.com/kjutzn/HopperSort/main/offline/latest_version.json'
    response = requests.get(github_url)

    try:
        response.raise_for_status()
        latest_version = response.text.strip().strip('"')

        if local_version == latest_version:
            print("You are using the latest version.")
        else:
            print(f"A new version ({latest_version}) is available. Please update.")
            prompt_update(latest_version)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")

def prompt_update(latest_version):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setText(f"A new version ({latest_version}) is available. Do you want to update?")
    msg_box.setWindowTitle("Update Available")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg_box.setDefaultButton(QMessageBox.StandardButton.Yes)

    ret = msg_box.exec_()

    if ret == QMessageBox.StandardButton.Yes:
        source_directory = QFileDialog.getExistingDirectory(None, "Select the source directory")

        if source_directory:
            FileOrganizerApp().log(f"Manual Input - Source Directory: {source_directory}\n")
            FileOrganizerApp().organize_files_by_extension(source_directory)
            QMessageBox.information(None, "Info", "File organization completed.")
            sys.exit(0)

def update_app():
    import webbrowser
    github_release_url = 'https://github.com/kjutzn/hoppersort/releases'
    webbrowser.open(github_release_url)

def fetch_file_extensions():
    github_url = 'https://raw.githubusercontent.com/kjutzn/HopperSort/main/offline/file_extenions.json'
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
        latest_version()
        source_directory = QFileDialog.getExistingDirectory(self, "Select the source directory")

        if source_directory:
            self.log(f"Manual Input - Source Directory: {source_directory}\n")
            self.organize_files_by_extension(source_directory)
            QMessageBox.information(self, "Info", "File organization completed.")

    def organize_files_on_desktop(self):
        latest_version()
        desktop_path = os.path.expanduser("~/Desktop")
        self.log(f"Organize Files on Desktop - Source Directory: {desktop_path}\n")
        self.organize_files_by_extension(desktop_path)
        QMessageBox.information(self, "Info", "File organization on Desktop completed.")

    def organize_files_in_downloads(self):
        latest_version()
        downloads_path = os.path.expanduser("~/Downloads")
        self.log(f"Organize Files in Downloads - Source Directory: {downloads_path}\n")
        self.organize_files_by_extension(downloads_path)
        QMessageBox.information(self, "Info", "File organization in Downloads completed.")

    def organize_files_in_documents(self):
        latest_version()
        documents_path = os.path.expanduser("~/Documents")
        self.log(f"Organize Files in Documents - Source Directory: {documents_path}\n")
        self.organize_files_by_extension(documents_path)
        QMessageBox.information(self, "Info", "File organization in Documents completed.")

    def organize_files_by_extension(self, source_folder):
        global file_extensions

        if not file_extensions:
            file_extensions = fetch_file_extensions()
            if not file_extensions:
                QMessageBox.warning(self, "Error", "Failed to fetch file extensions. Unable to proceed")
                return

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
        with open("log.txt", "a") as log_file:
            log_file.write(message)

    def resizeEvent(self, event):
        new_font_size = int(event.size().width() / 10)
        self.label_font.setPointSize(new_font_size)
        self.label.setFont(self.label_font)

def main():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
