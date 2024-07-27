import os
from PyQt5 import QtWidgets, QtGui, QtCore
from deep_translator import GoogleTranslator


class RenamingThread(QtCore.QThread):
    progress_updated = QtCore.pyqtSignal(int)
    label_updated = QtCore.pyqtSignal(str)
    renaming_done = QtCore.pyqtSignal(bool)

    def __init__(self, directory, src_lang, dest_lang, include_subfolders):
        super().__init__()
        self.directory = directory
        self.src_lang = src_lang
        self.dest_lang = dest_lang
        self.include_subfolders = include_subfolders
        self.stop_renaming = False

    def run(self):
        translator = GoogleTranslator(
            source=self.src_lang, target=self.dest_lang)
        total_files = sum([len(files) for r, d, files in os.walk(
            self.directory) if self.include_subfolders or r == self.directory])
        self.progress_updated.emit(0)
        progress_value = 0

        for root, _, files in os.walk(self.directory):
            for filename in files:
                if self.stop_renaming:
                    break
                try:
                    file_name, file_extension = os.path.splitext(filename)
                    translated_name_parts = [translator.translate(
                        word) or word for word in file_name.split()]
                    translated_name = ' '.join(translated_name_parts)
                    new_filename = f"{translated_name}{file_extension}"
                    os.rename(os.path.join(root, filename),
                              os.path.join(root, new_filename))
                    print(f'Renamed "{filename}" to "{new_filename}"')
                except Exception as e:
                    print(f'Error renaming "{filename}": {e}')

                progress_value += 1
                percentage = int((progress_value / total_files) * 100)
                self.progress_updated.emit(percentage)
                self.label_updated.emit(f"{percentage}%")

            if self.stop_renaming:
                break

        self.renaming_done.emit(not self.stop_renaming)

    def stop(self):
        self.stop_renaming = True


class FileNameTranslatorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.renaming_thread = None

    def init_ui(self):
        self.setWindowTitle('File Name Translator')
        self.setGeometry(100, 100, 700, 350)

        main_layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        button_layout = QtWidgets.QHBoxLayout()
        progress_layout = QtWidgets.QHBoxLayout()

        self.src_lang_label = QtWidgets.QLabel('Source Language:')
        self.dest_lang_label = QtWidgets.QLabel('Destination Language:')
        self.dir_label = QtWidgets.QLabel('Directory:')
        self.src_lang_combo = QtWidgets.QComboBox()
        self.dest_lang_combo = QtWidgets.QComboBox()
        self.dir_edit = QtWidgets.QLineEdit()
        self.browse_button = QtWidgets.QPushButton('Browse')
        self.include_subfolders_check = QtWidgets.QCheckBox(
            'Include Subfolders')
        self.start_button = QtWidgets.QPushButton('Start Renaming')
        self.stop_button = QtWidgets.QPushButton('Stop Renaming')
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_label = QtWidgets.QLabel('0%')

        languages = ['en', 'fr', 'es', 'de',
                     'it', 'pt', 'nl', 'ru', 'ja', 'zh-cn']
        self.src_lang_combo.addItems(languages)
        self.dest_lang_combo.addItems(languages)

        self.browse_button.clicked.connect(self.browse_directory)
        self.start_button.clicked.connect(self.start_renaming)
        self.stop_button.clicked.connect(self.stop_renaming_process)

        form_layout.addRow(self.src_lang_label, self.src_lang_combo)
        form_layout.addRow(self.dest_lang_label, self.dest_lang_combo)
        form_layout.addRow(self.dir_label, self.dir_edit)
        form_layout.addRow('', self.browse_button)
        form_layout.addRow('', self.include_subfolders_check)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(progress_layout)

        self.setLayout(main_layout)

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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = FileNameTranslatorApp()
    window.show()
    app.exec_()
