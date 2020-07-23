import cv2
import pyaudio
import wave
import threading
import time
import subprocess
import os
import sys


class VideoRecorder():
    """
    VideoRecorder class is used to record video.

    Methods:
        record()
            The function records video while ret is True.
        stop()
            The function stops recording video. 
            All the openCV objects are released.

    """

    def __init__(self, file_name='video'):
        self.open = True
        self.device_index = 0
        self.fps = 6
        self.fourcc = "MJPG"
        self.frameSize = (640, 480)
        self.file_name = file_name + ".avi"
        self.video_cap = cv2.VideoCapture(self.device_index)
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
        self.video_out = cv2.VideoWriter(
            self.file_name,
            self.video_writer,
            self.fps,
            self.frameSize)

    def record(self):
        """
        The function records video while ret is True. 
        Frame is written in the video every 160 ms.
        """

        while(self.open):
            ret, video_frame = self.video_cap.read()
            if(ret):
                try:
                    self.video_out.write(video_frame)
                    time.sleep(0.16)
                except OSError as e:
                    if e.errno == os.errno.ENOSPC:
                        print("No space left on device.")
            else:
                break

    def stop(self):
        """
        The function stops recording video. 
        All the openCV objects are released.
        """
        if self.open:
            print("video stop")
            self.open = False
            self.video_out.release()
            self.video_cap.release()
            cv2.destroyAllWindows()

        else:
            pass

    def main(self):
        """
        The function launches video recording function as a thread.
        """
        video_thread = threading.Thread(target=self.record)
        video_thread.start()
