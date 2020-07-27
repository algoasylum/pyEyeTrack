import cv2
import keyboard
from abc import ABC, abstractmethod
import dlib

import sys
import os
import bz2
from functools import partial
from tqdm import tqdm


SHAPE_PREDICTOR_FNAME = 'shape_predictor_68_face_landmarks.dat'
SHAPE_PREDICTOR_BZ2_FNAME = SHAPE_PREDICTOR_FNAME + '.bz2'
SHAPE_PREDICTOR_URL = 'http://dlib.net/files/{}'.format(SHAPE_PREDICTOR_BZ2_FNAME)

def _download_file(url, out_path):
    try:
        from urllib import urlretrieve          # Python 2
    except ImportError:
        from urllib.request import urlretrieve  # Python 3

    def reporthook(t, b=1, bsize=1, tsize=None, last_b=[0]):
        if tsize is not None:
            t.total = tsize
        t.update((b - last_b[0]) * bsize)
        last_b[0] = b
    
    with tqdm(unit='B', unit_scale=True, miniters=1, desc=out_path) as t:
        urlretrieve(url, filename=out_path, reporthook=partial(reporthook, t))

def _bz2_decompress_inplace(path, out_path):
    with open(path, 'rb') as source, open(out_path, 'wb') as dest:
        dest.write(bz2.decompress(source.read()))

def check():
    print("shape_predictor_68_face_landmarks.dat file is needed.")
    print("Press n -if you already have it and place it in the current folder")
    print("Press y -file will start downloading.")

    download_input = input()
    if download_input == 'y':
        script_path = os.path.dirname(os.path.abspath(__file__))

        _download_file(SHAPE_PREDICTOR_URL, SHAPE_PREDICTOR_BZ2_FNAME)
        _bz2_decompress_inplace(SHAPE_PREDICTOR_BZ2_FNAME,
                                    SHAPE_PREDICTOR_FNAME)


check()

class EyeTracking(ABC):

    """
    EyeTracking is an abstract class that is used to implement
    different types of eye-tracking events.
    In this library we have used this class to implement
    blink detection and pupil-tracking.

    Attributes:
        detector: default face detector in dlib
        predictor: used to map the facial landmark on the
        detected face

    Methods:
        csv_writer(file_name)
            an abstract method that is to be used for
            .csv file generation.
        functionality(frame)
            an abstract method used to implement type of eye-tracking.
            e.g. blinking
        start()
            method to start eye-tracking
    """
    file_path = os.path.abspath(SHAPE_PREDICTOR_FNAME)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(file_path)

    def __init__(self, source):

        # acquire the webcam based on device id
        self.cap = cv2.VideoCapture(source)
        self.frame = 0  # frame from the video or live-stream
        self.landmarks = "xx"  # variable to store facial landmarks
        self.close_flag = False  # flag used to close the application

    @abstractmethod
    def csv_writer(self, file_name):
        """
        Implements writer to write the data dictonary to .csv file.

        Args:
            file_name (string): name of the .csv file to be generated.
        """
        pass

    @abstractmethod
    def functionality(self, frame):
        """
        Implement the eye-tracking functionality required.
        Args:
            frame (numpy array): it is the frame in the video or captured by
            the camera
        """
        pass

    def start(self):
        """
        This function reads the input from the video or the live-stream.
        It also processes the frame acquired and detects the facein the frame.
        Then all the facial landmarks are mapped to face detected in the frame.
        The frame and the facial landmarks are thenused by the subclassed to
        implement blink detection or pupil tracking.
        The application terminates if the 'esc' key is pressed or if the
        close_flag is set to 'True'. If the face is not detected for 10 cycles
        of the loop the application will terminate.

        """
        face_not_detected = 0
        while True:

            if keyboard.is_pressed(
                    'esc') or self.close_flag or face_not_detected >= 10:
                break
                
                
            ret, self.frame = self.cap.read()

            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            faces, _, _ = self.detector.run(self.frame, 0, 0)

            if len(faces) == 0:
                print('Face not detected. Find better lighting.')
                face_not_detected += 1
                continue

            face_not_detected = 0

            self.landmarks = self.predictor(self.frame, faces[0])

            self.functionality(self.frame)

        self.cap.release()
