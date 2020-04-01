import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from guidriver import Ui_MainWindow


class AppWindow(QMainWindow): #main window object
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow() #'loads' layout from guidriver.py
        self.ui.setupUi(self) #setsup UI
        self.show


app = QApplication(sys.argv)
app.setStyle('Fusion') #sets gui style
app.setWindowIcon(QIcon('sit_logo.ico')) #sets app icon

w = AppWindow() #'creates' main window
w.show() #shows main window
sys.exit(app.exec_())
