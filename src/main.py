from PyQt5 import QtWidgets
from ui import FileNameTranslatorApp

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = FileNameTranslatorApp()
    window.show()
    app.exec_()
