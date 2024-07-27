import os
from PyQt5 import QtCore
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
                    translated_name = translator.translate(file_name)
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
