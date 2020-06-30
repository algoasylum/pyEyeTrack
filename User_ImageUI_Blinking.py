import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import time
from datahandling import QueueHandling

class Example(QWidget):

    def __init__(self,path):
        super().__init__()

        self.q = QueueHandling()
    
        self.im = QPixmap(path)
       
        self.label = QLabel()
        
        self.label.setScaledContents(True)
        self.label.setPixmap(self.im)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label,1,1)
        self.setLayout(self.grid)
        self.showFullScreen()
        
        self.setWindowTitle("PyQT show image")
        
        self.blinkcounts = 0


        self.stopByBlinks()
        
        self.q.add_data('Stop')
        

    
    def stopByBlinks(self):
        """[This function monitors the blink count. It primarily detects if the user has blinked twice. 
        The function acceses the queue that has the timestamp of the blink. 
        It increments the blinkcounter every time the queue has a new entry. 
        Once the count reaches two, the function returns the control.]
        """
        QApplication.processEvents()
        while self.blinkcounts<2:
            if self.q.get_data():
                self.blinkcounts+=1
        return 

        

def main():
    """[This function takes path of an image. 
    The function displays the image on the PyQt window and closes it when two blinks are detected.]
    """
    path = r'wallpaper.jpg'
    app = QApplication(sys.argv)
    
    ex = Example(path)
    
    ex.show()
 
    ex.close()



