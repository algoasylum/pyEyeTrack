from pyEyeTrack.EyeTracking.AbstractEyeTrackingClass import EyeTracking
import numpy as np
import pandas as pd
import cv2
import time
from pyEyeTrack.DataHandling import QueueHandling


class PupilTracking(EyeTracking):
    """
    A subclass of EyeTracking that does pupil tracking 
    i.e. this class will give the pupil centers for both the eyes.

    Methods:
        detect_eye(eye_points,facial_landmarks)
            Returns the location of the eye in the frame.
        get_connected_components(thresholded_pupil_region)
            Calculates the pupil center.
        get_approximate_pupil_rectangle(eye_landmarks_coordinates,frame)
            Returns the part of the frame with only the pupil
        get_pupil_center_coordinates(eye_landmarks_coordinates,threshold,
        frame)
            Returns pupil center for a single eye.
        functionality(frame)
            Implements pupil tracking for a given frame.
        csv_writer(file_name)
            Generates a .csv file with the timestamp and pupil center 
            for both eyes.

    """

    def __init__(self, source):
        super().__init__(source)
        self.eye_data_log = {"Timestamps": [], "Left_Eye_X": [], "Left_Eye_Y": []  
                             , "Right_Eye_X": [], "Right_Eye_Y": []}
        # dictionary to store the location of the pupil center and 
        # the corresponding timestamp
        self.queue_handler = QueueHandling()
        # intialized queue to do real-time data transfer

    def detect_eye(self, eye_points, facial_landmarks):
        """
        This function returns a numpy array of the x, y coordinates of the 
        landmarks that define the eye in the frame.

        Args:
            eye_points (list): the list of indicies of the facial landmarks 
            which represent an eye 
            facial_landmarks (dlib.full_object_detection): this object helps 
            get the location of the eye in the frame

        Returns:
            numpy array: the array of points that define the location of the 
            eye in the frame.
        """

        eye_landmarks_coordinates = np.array(
            [(facial_landmarks.part(eye_points[0]).x,
              facial_landmarks.part(eye_points[0]).y),
             (facial_landmarks.part(eye_points[1]).x,
              facial_landmarks.part(eye_points[1]).y),
             (facial_landmarks.part(eye_points[2]).x,
              facial_landmarks.part(eye_points[2]).y),
             (facial_landmarks.part(eye_points[3]).x,
              facial_landmarks.part(eye_points[3]).y),
             (facial_landmarks.part(eye_points[4]).x,
              facial_landmarks.part(eye_points[4]).y),
             (facial_landmarks.part(eye_points[5]).x,
              facial_landmarks.part(eye_points[5]).y)],
            np.int32)
        return eye_landmarks_coordinates

    def get_connected_components(self, thresholded_pupil_region):
        """
        This function returns the pupil ceter of the eye. 
        The input parameter is the thresholded pupil region.
        The pupil center is the centroid of the connected component
        with the largest area. Since we already have the approximate
        pupil area, we assume that the connected component with the 
        largest area to be the the pupil.

        Args:
            thresholded_pupil_region (numpy array): the approximate 
            pupil area after filtering and thresholding is applied.

        Returns:
            (float, float): a tuple with the x, y coordinate of the 
            pupil center.
        """

        _, _, stats, centroids = cv2.connectedComponentsWithStats(
            thresholded_pupil_region, 4)

        area = []
        index = 0
        for stat in stats:
            area.append((stat[4], index))
            index = index + 1

        maximum_area = max(area)
        index_of_maximum_area = maximum_area[1]

        pupil_center = centroids[index_of_maximum_area]

        return pupil_center

    def get_approximate_pupil_rectangle(
            self, eye_landmarks_coordinates, frame):
        """
        In this function we first find the minimum and maximum for 
        x coordinate of the location the eye and similarly for the y coordinate.
        Here we have altered the values such that after cropping the area would 
        give us only the region inside the eye. This is the approximately
        the region where the pupil lies.

        Args:
            eye_landmarks_coordinates (numpy array): array of the x,y 
            coordinates of the location the eye
            frame (numpy array): it is the frame in the video or captured 
            by the camera

        Returns:
            numpy array: the area of the eye cropped tightly
        """

        eye_landmark_min_x = np.min(eye_landmarks_coordinates[:, 0]) + 10
        eye_landmark_max_x = np.max(eye_landmarks_coordinates[:, 0]) - 10
        eye_landmark_min_y = np.min(eye_landmarks_coordinates[:, 1]) + 1
        eye_landmark_max_y = np.max(eye_landmarks_coordinates[:, 1]) - 1
        approximate_pupil_region = frame[eye_landmark_min_y: eye_landmark_max_y,
                                         eye_landmark_min_x: eye_landmark_max_x]

        return approximate_pupil_region

    def get_pupil_center_coordinates(
            self,
            eye_landmarks_coordinates,
            threshold,
            frame):
        """
        This function returns the pupil center for a single eye. First we acquire 
        the approximate region of the frame in which the pupil lies.
        Then we perform thresholding on this cropped part of the frame. 
        We then send this proceesed part to the get_connected_components function
        which returns the pupil center.

        Args:
            eye_landmarks_coordinates (numpy array): array of the x,y coordinates 
            of the location the eye
            threshold (int): the value that should be used for thresholding
            frame (numpy array): it is the frame in the video or captured by the camera

        Returns:
            (float, float): a tuple containing x and y coordinates of the pupil center.
        """

        approximate_pupil_region = self.get_approximate_pupil_rectangle(
            eye_landmarks_coordinates, frame)

        median_blur_filter = cv2.medianBlur(approximate_pupil_region, 5)
        _, thresholded_pupil_region = cv2.threshold(
            median_blur_filter, threshold, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        return self.get_connected_components(thresholded_pupil_region)

    def functionality(self, frame):
        """
        This method overrides the method in the superclass. 
        This method gets the pupil center for both the eyes in the frame.
        Once the pupil centers are acquired we append them in eye_data_log 
        dictonary along with the timestamp.
        We also add this data to the queue for real-time data transfer. 
        Finally, we also toggle the close_flag if the string 'Stop' is found
        in the queue. This can be used by the user to stop the application.

        Args:
            frame (numpy array): it is the frame in the video or captured 
            by the camera
        """

        landmarks_coordinates_left_eye = self.detect_eye(
            [36, 37, 38, 39, 40, 41], self.landmarks)
        landmarks_coordinates_right_eye = self.detect_eye(
            [42, 43, 44, 45, 46, 47], self.landmarks)

        pupil_center_left_eye = self.get_pupil_center_coordinates(
            landmarks_coordinates_left_eye, 0, frame)
        pupil_center_right_eye = self.get_pupil_center_coordinates(
            landmarks_coordinates_right_eye, 0, frame)

        timestamp = time.time()
        self.eye_data_log["Timestamps"].append(timestamp)
        self.eye_data_log["Left_Eye_X"].append(pupil_center_left_eye[0])
        self.eye_data_log["Left_Eye_Y"].append(pupil_center_left_eye[1])
        self.eye_data_log["Right_Eye_X"].append(pupil_center_right_eye[0])
        self.eye_data_log["Right_Eye_Y"].append(pupil_center_right_eye[1])
        pupil_center_data = (
            timestamp,
            pupil_center_left_eye[0],
            pupil_center_left_eye[1],
            pupil_center_right_eye[0],
            pupil_center_right_eye[1])
        self.queue_handler.add_data(pupil_center_data)

        if self.queue_handler.search_element('Stop'):
            self.close_flag = True

    def csv_writer(self, file_name):
        """
        Generates a .csv file with the timestamp and pupil centers with the 
        given file name.

        Args:
            file_name (string): name of the .csv file to be generated.
        """
        file_name = file_name + ".csv"
        DF = pd.DataFrame(self.eye_data_log)
        DF.to_csv(file_name)
