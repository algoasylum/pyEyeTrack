from EyeTracking.PupilTrackingClass import PupilTracking
from EyeTracking.BlinkingClass import Blinking
from EyeTracking.PupilBlinkingClass import PupilBlinking
from AudioVideoRecording.VideoRecordingClass import VideoRecorder
from AudioVideoRecording.AudioRecordingClass import AudioRecorder
import threading
import importlib
import sys
import os
import subprocess


class PyTrackRunner():

    def __init__(self):
        pass

    def dynamic_import(self, module):
        return importlib.import_module(module)

    def pytrack_runner(
            self,
            UI=False,
            UI_file_name="User_ImageUI_EscExit",
            pupilTracking=False,
            blinkDetection=False,
            video_source=0,
            eyeTrackingLog=True,
            eyeTrackingFileName='EyeTrackLog',
            videoRecorder=False,
            videoName='video',
            audioRecorder=False,
            audioName='audio',
            syncAudioVideo=False,
            destinationPath='/Output'):
        """
        This function enables the user to run the functionalities of the 
        library simultaneously.
        Functionalities include running the UI specified by the user, 
        pupil tracking, blink detection, video recording and audio recording.
        The user can set flags to run the combination of these functionalities. 
        The function also allows the user to name the output file.

        Args:
            UI (bool, optional): This parameter enables the user to run UI. 
            Defaults to False.

            UI_file_name (str, optional): This parameter takes the file name 
            of the UI. Defaults to "User_ImageUI_EscExit".

            pupilTracking (bool, optional): This parameter enables the user to 
            run pupil tracking. Defaults to False.

            blinkDetection (bool, optional): This parameter enables the user 
            to run blink detection. Defaults to False.

            video_source (int/str, optional): This parameter takes either 
            device index or a video file as input. Defaults to 0.

            eyeTrackingLog (bool, optional): This parameter enables the user to 
            generate a CSV of pupil tracking/ blink detection. Defaults to True.

            eyeTrackingFileName (str, optional): This parameter takes the file name 
            for the CSV. Defaults to 'EyeTrackLog'.

            videoRecorder (bool, optional): This parameter enables the user to 
            record video. Defaults to False.

            videoName (str, optional): This parameter takes the file name for 
            the video. Defaults to 'video'.

            audioRecorder (bool, optional): This parameter enables the user to 
            record audio. Defaults to False.

            audioName (str, optional): This parameter takes the file name for 
            the audio. Defaults to 'audio'.

            syncAudioVideo (bool, optional): This parameter enables the user to 
            sync audio and video together. Defaults to False.

            destinationPath (str, optional): This parameter enables the user to 
            store their output files at the desired location. Defaults to Outputs Folder.
        """

        startEyeTracking = False
        outputPath = destinationPath

        if os.access(
                destinationPath,
                os.W_OK) == False and destinationPath != '/Output':
            print('You may not have write permission.Try changing the destination path.')
            sys.exit()

        if os.path.exists(
                destinationPath) == False and destinationPath != '/Output':
            os.mkdir(destinationPath)
        elif destinationPath == '/Output':
            currentPath = os.getcwd()
            outputPath = currentPath + '/Output'
            if os.path.exists(outputPath) == False:
                os.mkdir(outputPath)

        outputPath = outputPath + '/'

        if pupilTracking or blinkDetection:
            startEyeTracking = True

        if video_source != 0:
            if os.path.exists(video_source) == False:
                print('Please specify correct path for the video source.')
                sys.exit()

        if blinkDetection and pupilTracking:
            eyeTracking = PupilBlinking(video_source)
            eyeTrackingThread = threading.Thread(target=eyeTracking.start)

        if blinkDetection and pupilTracking == False:
            eyeTracking = Blinking(video_source)
            eyeTrackingThread = threading.Thread(target=eyeTracking.start)

        if pupilTracking and blinkDetection == False:
            eyeTracking = PupilTracking(video_source)
            eyeTrackingThread = threading.Thread(target=eyeTracking.start)

        if syncAudioVideo:
            audioRecorder = True
            videoRecorder = True

        if videoRecorder:
            videoOutputPath = outputPath + videoName
            videoRecorder = VideoRecorder(videoOutputPath)
            videoRecorderThread = threading.Thread(target=videoRecorder.main)

        if audioRecorder:
            audioOutputPath = outputPath + audioName
            audioRecorder = AudioRecorder(outputPath + audioName)
            audioRecorderThread = threading.Thread(target=audioRecorder.main)

        if UI:
            module = self.dynamic_import(UI_file_name)
            if hasattr(module, 'main'):
                uiThread = threading.Thread(target=module.main)
            else:
                print(
                    'UI needs a main method. Please Refer documentation for more information.')
                sys.exit()

        if UI:
            uiThread.start()

        if startEyeTracking:
            eyeTrackingThread.start()

        if videoRecorder:
            videoRecorderThread.start()

        if audioRecorder:
            audioRecorderThread.start()

        if UI:
            uiThread.join()

        if startEyeTracking:
            eyeTrackingThread.join()
            if eyeTrackingLog:
                eyeTrackingOutput = outputPath + eyeTrackingFileName
                eyeTracking.csv_writer(eyeTrackingOutput)

        if videoRecorder:
            videoRecorderThread.join()
            videoRecorder.stop()

        if audioRecorder:
            audioRecorderThread.join()
            audioRecorder.stop()

        if syncAudioVideo and audioRecorder and videoRecorder:

            file_name = audioName + videoName
            avOutputPath = outputPath + file_name
            
            cmd = 'ffmpeg -y -i ' + audioOutputPath + '.wav  -r 30 -i ' + videoOutputPath + \
                '.avi  -filter:a aresample=async=1 -c:a flac -c:v copy ' + avOutputPath + '.mkv'
            subprocess.call(cmd, shell=True)
                                                    
