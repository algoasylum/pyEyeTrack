from pyEyeTrack.EyeTracking.AbstractEyeTrackingClass import EyeTracking
import pandas as pd
import time
from math import hypot
from pyEyeTrack.DataHandling import QueueHandling


class Blinking (EyeTracking):

    """
    A subclass of EyeTracking that does blink detection.

    Methods:
        midpoint(point_1, point2)
            Calculates midpoint of two given points.
        get_blink_ratio(eye_points, facial_landmarks)
            Calculates the blink ratio.
        functionality(frame)
            Implements the blink detection for a given frame.
        csv_writer(file_name)
            Generates a .csv file with the timestamp and blink ratio.
    """

    def __init__(self, source):

        super().__init__(source) #constuctor of the superclass- EyeTracking
        self.timestamps = []  #stores timestamps of the blink
        self.blink_ratios = []  #stores the blink ratio
        self.queue_handler = QueueHandling() #queue for real-time data transfer
        self.BLINK_RATIO_THRESHOLD = 5.7 #value of the blink ratio threshold

    def midpoint(self, point_1, point_2):
        """
        This function calculates the midpoint of two dlib.point 
        objects and returns the result as a tuple of integers

        Args:
            point_1 (dlib.point): first point to calculate the midpoint
            point_2 (dlib.point): second point to calculate the midpoint

        Returns:
            (int, int): a tuple containing the x and y coordinates 
            of the midpoint.
        """
        return (int((point_1.x + point_2.x) / 2),
                int((point_1.y + point_2.y) / 2))

    def get_blink_ratio(self, eye_points, facial_landmarks):
        """
        This function calculates the blink ratio for a single eye. 
        blink_ratio is the ratio of the horizontal length of the eye 
        to the vertical length of the eye. 
        The horizontal and vertical lengths are obtained by calculating 
        the Euclidean distance between landmarks of the eye.

        Args:
            eye_points (list): the list of indicies of the facial 
                                landmarks which represent an eye
            facial_landmarks (dlib.full_object_detection): 
                               this object helps get the location of 
                               the eye in the frame.

        Returns:
            float: returns the blink ratio i.e. ratio of the 
                   horizontal length of the eye to the vertical 
                   length of the eye
        """
        corner_left = (
            facial_landmarks.part(eye_points[0]).x, 
            facial_landmarks.part(eye_points[0]).y)
        corner_right = (
            facial_landmarks.part(eye_points[3]).x, 
            facial_landmarks.part(eye_points[3]).y)
        center_top = self.midpoint(
            facial_landmarks.part(eye_points[1]), 
            facial_landmarks.part(eye_points[2]))
        center_bottom = self.midpoint(
            facial_landmarks.part(eye_points[5]), 
            facial_landmarks.part(eye_points[4]))

        horizontal_length = hypot(
            (corner_left[0] - corner_right[0]),
            (corner_left[1] - corner_right[1]))
        vertical_length = hypot(
            (center_top[0] - center_bottom[0]),
            (center_top[1] - center_bottom[1]))

        blink_ratio = horizontal_length / vertical_length
        return blink_ratio

    def functionality(self, frame):
        """
        This method overrides the method in the superclass. 
        This method gets the blink ratios for both the eyes
        and calculates the average blink ratio. If the value of the 
        average blink ratio is greater than the BLINK_RATIO_THRESHOLD
        we presume that the subject blinked. 
        If the subject blinks we add the timestamp of the blink 
        and the value of the blink ratio to the respective lists. 
        We also add True to the queue on blink detection. 
        This queue can be acessed by the user to see if the subject 
        blinked in real-time. 
        Finally, we also toggle the close_flag if the string 'Stop' is found
        in the queue. This can be used by the user to stop the application.

        Args:
            frame (numpy array): it is the frame in the video or 
            captured by the camera
        """

        left_eye_ratio = self.get_blink_ratio(
            [36, 37, 38, 39, 40, 41], self.landmarks)
        right_eye_ratio = self.get_blink_ratio(
            [42, 43, 44, 45, 46, 47], self.landmarks)
        blink_ratio = (left_eye_ratio + right_eye_ratio) / 2

        if blink_ratio > self.BLINK_RATIO_THRESHOLD:
            timestamp = time.time()
            self.queue_handler.add_data(True)
            self.timestamps.append(timestamp)
            self.blink_ratios.append(blink_ratio)
    

        if self.queue_handler.search_element('Stop'):
            self.close_flag = True

    def csv_writer(self, file_name='blink_log'):
        """
        Generates a .csv file with the timestamp and blink ratio 
        with the given file name.

        Args:
            file_name (string): name of the .csv file to be generated.
        """
        file_name = file_name + ".csv"
        df = pd.DataFrame({"Timestamps": self.timestamps,
                           "Blink Ratio": self.blink_ratios})
        df.to_csv(file_name)
