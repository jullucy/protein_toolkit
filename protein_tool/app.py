from PySide6.QtWidgets import QMainWindow, QApplication, QMenuBar
from PySide6.QtGui import QAction  # QAction is in QtGui, not QtWidgets
from PySide6.QtGui import QIcon
from .main_window import MainWindow

def run():
    app = QApplication([])
    app.setApplicationName("Protein Tool")
    app.setOrganizationName("Julia Łucyn")
    win = MainWindow()
    win.show()
    return app.exec()
