import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import threading
import time


class Example(QWidget):
    """
    This class is used to display an image on a full screen UI.

    Args:
        QWidget : The QWidget class provides the basic capability to render 
                  to the screen, and to handle user input events.
    """

    def __init__(self, path='wallpaper.jpg'):
        super().__init__()

        self.im = QPixmap(path)

        self.label = QLabel()

        self.label.setScaledContents(True)
        self.label.setPixmap(self.im)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 1, 1)
        self.setLayout(self.grid)
        self.showFullScreen()

        self.setWindowTitle("PyQT show image")

    def keyPressEvent(self, event):
        """
        This function monitors key press events while the program runs.
        On the key press of Escape - the program terminates]
        """

        if event.key() == Qt.Key_Escape:
            self.close()


def main():
    """
    This function takes path of an image.
    The function displays the image on the PyQt window.
    The function closes the window when the code detects the escape 
    key press.
    """
    #path = input('Enter image path: ')
    path = 'wallpaper.jpg'

    app = QApplication(sys.argv)

    ex = Example(path)
    ex.show()

    app.exec_()
