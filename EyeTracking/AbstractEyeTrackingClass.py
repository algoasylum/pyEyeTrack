import cv2
import keyboard
from abc import ABC, abstractmethod
import dlib


class EyeTracking(ABC):

    """
    EyeTracking is an abstract class that is used to implement different types of eye-tracking events.
    In this library we have used this class to implement blink detection and pupil-tracking.

    Attributes:
        detector: default face detector in dlib
        predictor: used to map the facial landmark on the face detected

    Methods:
        csv_writer(file_name)
            an abstract method that is to be used for .csv file generation.
        functionality(frame)
            an abstract method used to implement type of eye-tracking. e.g. blinking
        start()
            method to start eye-tracking
    """

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(r"EyeTracking\shape_predictor_68_face_landmarks.dat")

    def __init__(self,source):

        self.cap = cv2.VideoCapture(source)                           #load the video or acquire the webcam based on device id
        self.frame = 0                                                #frame from the video or live-stream intialed to 0
        self.landmarks = "xx"                                         #variable to store facial landmarks
        self.close_flag = False                                       #flag used to close the application initialsed to Flase

    @abstractmethod
    def csv_writer(self, file_name):
        """
        Implements writer to write the data dictonary to .csv file.

        Args:
            file_name (string): name of the .csv file to be generated.
        """
        pass

    @abstractmethod
    def functionality(self,frame):
        """
        Implement the eye-tracking functionality required. 
        Args:
            frame (numpy array): it is the frame in the video or captured by the camera
        """
        pass

    def start(self):
        """
        This function reads the input from the video or the live-stream. It also processes the frame acquired and detects the face 
        in the frame. Then all the facial landmarks are mapped to face detected in the frame. The frame and the facial landmarks are then
        used by the subclassed to implement blink detection or pupil tracking. The application terminates if the 'esc' key is pressed or
        if the close_flag is set to 'True' . 

        """
        while True:            
            ret, self.frame = self.cap.read()

            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break 

            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            faces,_,_ = self.detector.run(self.frame,0)

            if len(faces)==0:
                print('Face not detected. Find better lighting.')
                break

            self.landmarks = self.predictor(self.frame, faces[0])

            self.functionality(self.frame)   

            if keyboard.is_pressed('esc') or self.close_flag ==True:
                break

        self.cap.release()





