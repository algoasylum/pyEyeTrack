import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import time
from DataHandling import QueueHandling


class Example(QWidget):
    """
    This class is used to display an image on a full screen UI.

    Args:
        QWidget : The QWidget class provides the basic capability to render to the screen, and to handle user input events.
    """

    def __init__(self, path):
        super().__init__()

        self.queue_handler = QueueHandling()

        self.im = QPixmap(path)

        self.label = QLabel()

        self.label.setScaledContents(True)
        self.label.setPixmap(self.im)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 1, 1)
        self.setLayout(self.grid)
        self.showFullScreen()

        self.setWindowTitle("PyQT show image")

        self.blink_count = 0

        # Calls the stopByBlinks function to stop the UI after 2 blinks are
        # detected
        self.stopByBlinks()

        self.queue_handler.add_data('Stop')

    def stopByBlinks(self):
        """
        This function monitors the blink count. It primarily detects if the user has blinked twice.
        The function acceses the queue to detect a blink.
        It increments the blinkcounter every time the queue has a new entry.
        Once the count reaches two, the function returns the control.
        """
        QApplication.processEvents()

        while self.blink_count < 2:

            queue_element = self.queue_handler.get_data()
            if queue_element[5]:
                self.blink_count += 1

        return


def main():
    """
    This function takes path of an image.
    The function displays the image on the PyQt window and closes it when two blinks are detected.
    """
    path = r'wallpaper.jpg'
    app = QApplication(sys.argv)

    ex = Example(path)

    ex.show()

    ex.close()
