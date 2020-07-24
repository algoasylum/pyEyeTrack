import pandas as pd
import time
from math import hypot
from pyEyeTrack.DataHandling import QueueHandling
from pyEyeTrack.EyeTracking.BlinkingClass import Blinking
from pyEyeTrack.EyeTracking.PupilTrackingClass import PupilTracking
from pyEyeTrack.EyeTracking.AbstractEyeTrackingClass import EyeTracking


class PupilBlinking(Blinking, PupilTracking, EyeTracking):

    """
    A subclass of EyeTracking that does blink detection and 
    pupil-tracking.

    Methods:
        functionality(frame)
            Implements pupil tracking and blink detection for a 
            given frame.
        csv_writer(file_name)
            Generates a .csv file with the timestamp,pupil center and 
            blink detection for both eyes.
    """

    def __init__(self, source):
        super().__init__(source)
        # dictionary to store the location of the pupil center, 
        # blink and the corresponding timestamp
        # stores the blink ratio everytime the subject blinks
        self.eye_data_log = {
            "Timestamps": [],
            "Left_Eye_X": [],
            "Left_Eye_Y": [],
            "Right_Eye_X": [],
            "Right_Eye_Y": [],
            "Blink": []}
        # intialized queue to do real-time data transfer
        self.queue_handler = QueueHandling()

    def functionality(self, frame):
        """
        This method overrides the method in the superclass. 
        This method gets the blink ratios for both the eyes and 
        calculates the average blink ratio.

        If the value of the average blink ratio is greater than the 
        BLINK_RATIO_THRESHOLD,we presume that the subject blinked. 
        Here, we set the value of the 'Blink' field in the dictonary 
        to 'False'.We add the data to the dictonary as well as the 
        queue to facilitate real-time data transfer. 
        The values of the pupil centers are set to 0 when the 
        subject is blinking.

        If the blink ratio is less than the BLINK_RATIO_THRESHOLD,
        we calcute the location of the pupil center for both the eyes.
        Once the pupil centers are acquired we append them in eye_data_log
        dictonary along with the timestamp. 
        Here, we set the 'Blink' field in the dictonary to 'False'. 
        We also add this data to the queue for real-time data transfer.

        Finally, we also toggle the close_flag if the string 'Stop' is 
        found in the queue. This can be used by the user to
        stop the application.

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
            timestamp_blinking = time.time()
            self.eye_data_log["Timestamps"].append(timestamp_blinking)
            self.eye_data_log["Left_Eye_X"].append(0)
            self.eye_data_log["Left_Eye_Y"].append(0)
            self.eye_data_log["Right_Eye_X"].append(0)
            self.eye_data_log["Right_Eye_Y"].append(0)
            self.eye_data_log["Blink"].append(True)
            blink_data = (timestamp_blinking, 0, 0, 0, 0, True)
            self.queue_handler.add_data(blink_data)
        else:

            landmarks_coordinates_left_eye = self.detect_eye(
                [36, 37, 38, 39, 40, 41], self.landmarks)
            landmarks_coordinates_right_eye = self.detect_eye(
                [42, 43, 44, 45, 46, 47], self.landmarks)

            pupil_center_left_eye = self.get_pupil_center_coordinates(
                landmarks_coordinates_left_eye, 0, frame)
            pupil_center_right_eye = self.get_pupil_center_coordinates(
                landmarks_coordinates_right_eye, 0, frame)
            timestamp_pupil_centers = time.time()

            self.eye_data_log["Timestamps"].append(timestamp_pupil_centers)
            self.eye_data_log["Left_Eye_X"].append(pupil_center_left_eye[0])
            self.eye_data_log["Left_Eye_Y"].append(pupil_center_left_eye[1])
            self.eye_data_log["Right_Eye_X"].append(pupil_center_right_eye[0])
            self.eye_data_log["Right_Eye_Y"].append(pupil_center_right_eye[1])
            self.eye_data_log["Blink"].append(False)
            pupil_center_data = (
                timestamp_pupil_centers,
                pupil_center_left_eye[0],
                pupil_center_left_eye[1],
                pupil_center_right_eye[0],
                pupil_center_right_eye[1],
                False)
            self.queue_handler.add_data(pupil_center_data)

        if self.queue_handler.search_element('Stop'):
            self.close_flag = True

    def csv_writer(self, file_name):
        """
        Generates a .csv file with the timestamp and pupil centers with 
        the given file name.

        Args:
            file_name (string): name of the .csv file to be generated.
        """
        file_name = file_name + ".csv"
        DF = pd.DataFrame(self.eye_data_log)
        DF.to_csv(file_name)

    def start(self):
        return super().start()
