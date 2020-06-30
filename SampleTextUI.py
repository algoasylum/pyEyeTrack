import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QTextCursor
import time,csv
import pandas as pd


class MainWindow(QMainWindow):

    def __init__(self, path, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.path = path
        self.setWindowTitle("Text UI")
        self.showFullScreen()
        self.i = 0
        self.editor = QTextEdit()  
        f = self.editor.font()
        f.setPointSize(27) # sets the size to 27
        self.editor.setFont(f)
        self.setCentralWidget(self.editor)
        self.cursor = QTextCursor(self.editor.document())
        self.cursor.setPosition(0)
        self.editor.setTextCursor(self.cursor)
        with open('ts_line.csv','w') as file:
            self.fieldnames = ('Start_Time','End_Time','video_Time')
            self.writer = csv.DictWriter(file,fieldnames = self.fieldnames)
            self.writer.writeheader()
            start = time.time()
            self.writer.writerow({'video_Time':start})
        

    def openfile(self,i):
        """[This function opens and reads the file specified by the path. 
        It returns each line of the file when called.]

        Args:
            i ([integer]): ['i' specifies the line number]

        Returns:
            [an element of the list 'data']: [It returns the specified line from the file.]
        """
        file = open(self.path,"r")
        with file:
            text = file.read()
        data = text.splitlines()
        return data[i]
           
    def keyPressEvent(self,event):
        """[This function monitors key press events while the program runs. 
        On the key press of Escape - the program terminates.

        On the key press of Ctrl - a new line appears on the display. 
        The timestamp at the time of key press is added to a csv. 
        This timestamp denotes the start time of the user reading the line.

        On the key press of shift - The timestamp at the time of key press is added to csv. 
        This timestamp denotes the end time of the user reading the line.]
        Args:
            event ([key press]): [Detects key presses]
        """

        if event.key() == Qt.Key_Escape:
            self.close()
        
        if event.key()==Qt.Key_Shift:
            ts_end = time.time()
            with open('ts_line.csv','a') as file:
                writer = csv.DictWriter(file,fieldnames = self.fieldnames)
                writer.writerow({'End_Time':ts_end})
            self.i = self.i+1
        
        if event.key() == Qt.Key_Control:
            data = self.openfile(self.i)
            ts_start = time.time()
            with open('ts_line.csv','a') as file:
                writer = csv.DictWriter(file,fieldnames = self.fieldnames)
                writer.writerow({'Start_Time':ts_start})
            
            if self.i%8 ==0:
                self.cursor.setPosition(0)
                self.editor.setTextCursor(self.cursor)
                self.editor.setText(data)
                self.editor.append("")
            else:
                self.editor.append(data)
                self.editor.append("")

            
        
def main():
    """[This function takes the path of a text file and displays and it on a PyQt window.]
    """
    path = "SampleFile.txt"
    app = QApplication(sys.argv)

    window = MainWindow(path)
    window.show()
    app.exec_()

