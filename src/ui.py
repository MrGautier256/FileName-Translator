from PyQt5 import QtWidgets, QtCore
from renaming_thread import RenamingThread


class FileNameTranslatorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.renaming_thread = None

    def init_ui(self):
        self.setWindowTitle('File Name Translator')
        self.setGeometry(100, 100, 800, 400)

        # Set main layout
        main_layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        button_layout = QtWidgets.QHBoxLayout()
        progress_layout = QtWidgets.QHBoxLayout()

        # Define widgets
        self.src_lang_label = QtWidgets.QLabel('Source Language:')
        self.dest_lang_label = QtWidgets.QLabel('Destination Language:')
        self.dir_label = QtWidgets.QLabel('Directory:')
        self.src_lang_combo = QtWidgets.QComboBox()
        self.dest_lang_combo = QtWidgets.QComboBox()
        self.dir_edit = QtWidgets.QLineEdit()
        self.browse_button = QtWidgets.QPushButton('Browse')
        self.include_subfolders_check = QtWidgets.QCheckBox(
            'Include Subfolders')
        self.start_button = QtWidgets.QPushButton('Start')
        self.stop_button = QtWidgets.QPushButton('Stop')
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_label = QtWidgets.QLabel('0%')

        # Set language options
        languages = ['en', 'fr', 'es', 'de',
                     'it', 'pt', 'nl', 'ru', 'ja', 'zh-cn']
        self.src_lang_combo.addItems(languages)
        self.dest_lang_combo.addItems(languages)

        # Connect buttons to functions
        self.browse_button.clicked.connect(self.browse_directory)
        self.start_button.clicked.connect(self.start_renaming)
        self.stop_button.clicked.connect(self.stop_renaming_process)

        # Add widgets to form layout
        form_layout.addRow(self.src_lang_label, self.src_lang_combo)
        form_layout.addRow(self.dest_lang_label, self.dest_lang_combo)
        form_layout.addRow(self.dir_label, self.dir_edit)
        form_layout.addRow('', self.browse_button)
        form_layout.addRow('', self.include_subfolders_check)
        form_layout.setSpacing(20)  # Add spacing between form rows

        # Add buttons to button layout
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.setSpacing(20)  # Add spacing between buttons

        # Add progress bar and label to progress layout
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)

        # Add all layouts to main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(progress_layout)
        # Add margins to main layout
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Set main layout to the widget
        self.setLayout(main_layout)

        # Apply styles
        self.apply_styles()

    def apply_styles(self):
        # Set stylesheet for the application
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                font-size: 14px;
                background-color: #2b2b2b;
                color: #d3d3d3;
            }
            QLabel {
                color: #d3d3d3;
            }
            QLineEdit, QComboBox {
                border: 1px solid #555;
                border-radius: 4px;
                padding: 8px;  /* Increased padding for better spacing */
                background-color: #3b3b3b;
                color: #d3d3d3;
            }
            QPushButton {
                background-color: #555;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #777;
            }
            QProgressBar {
                height: 40px;  /* Further increased height for the progress bar */
                border: 1px solid #777;
                border-radius: 5px;
                text-align: center;  /* Centered text within progress bar */
                color: transparent;  /* Hide the text within the progress bar */
                background-color: #3b3b3b;
            }
            QProgressBar::chunk {
                background-color: #5a9;
                width: 20px;
                margin: 1px;
            }
            QCheckBox {
                color: #d3d3d3;
            }
        """)

    def browse_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory")
        if directory:
            self.dir_edit.setText(directory)

    def start_renaming(self):
        if not self.dir_edit.text():
            QtWidgets.QMessageBox.warning(
                self, "Warning", "Please select a directory.")
            return

        self.renaming_thread = RenamingThread(
            self.dir_edit.text(),
            self.src_lang_combo.currentText(),
            self.dest_lang_combo.currentText(),
            self.include_subfolders_check.isChecked()
        )
        self.renaming_thread.progress_updated.connect(self.set_progress)
        self.renaming_thread.label_updated.connect(self.set_label)
        self.renaming_thread.renaming_done.connect(self.renaming_completed)
        self.renaming_thread.start()

    def stop_renaming_process(self):
        if self.renaming_thread:
            self.renaming_thread.stop()
            QtWidgets.QMessageBox.information(
                self, "Stopped", "File renaming has been stopped.")
            self.progress_bar.setValue(0)
            self.progress_label.setText("0%")

    @QtCore.pyqtSlot(int)
    def set_progress(self, value):
        self.progress_bar.setValue(value)

    @QtCore.pyqtSlot(str)
    def set_label(self, text):
        self.progress_label.setText(text)

    @QtCore.pyqtSlot(bool)
    def renaming_completed(self, completed):
        if completed:
            QtWidgets.QMessageBox.information(
                self, "Done", "File renaming is complete!")
        self.progress_bar.setValue(0)
        self.progress_label.setText("0%")

    def closeEvent(self, event):
        if self.renaming_thread and self.renaming_thread.isRunning():
            self.renaming_thread.stop()
        event.accept()
