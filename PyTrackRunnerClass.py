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


    def dynamic_import(self,module):
        return importlib.import_module(module)

    def pytrack_runner(self, UI_file_name = "User_ImageUI_EscExit", eyeTrackingFileName='EyeTrackLog', video_source = 0, UI = False, 
    pupilTracking = False, blinkDetection = False, eyeTrackingLog=True,
    videoRecorder = False, audioRecorder = False,videoName = 'video', audioName = 'audio', syncAudioVideo = False, destinationPath = '/Output'):
        """
        This function enables the user to run the functionalities of the library simultaneously. 
        Functionalities include running the UI specified by the user, pupil tracking, blink detection, video recording and audio recording.
        The user can set flags to run the combination of these functionalities. The function allows the user to name the output file.

        Args:
            UI_file_name (str, optional): [This parameter takes the file name of the UI]. Defaults to "User_ImageUI_EscExit".
            eyeTrackingFileName (str, optional): [This parameter takes the file name for the CSV]. Defaults to 'EyeTrackLog'.
            video_source (int/str, optional): [This parameter takes either device index or a video file as input]. Defaults to 0.
            UI (bool, optional): [This parameter enables the user to run UI]. Defaults to False.
            pupilTracking (bool, optional): [This parameter enables the user to run pupil tracking]. Defaults to False.
            blinkDetection (bool, optional): [This parameter enables the user to run blink detection]. Defaults to False.
            eyeTrackingLog (bool, optional): [This parameter enables the user to generate a CSV of pupil tracking/ blink detection]. Defaults to True.
            videoRecorder (bool, optional): [This parameter enables the user to record video]. Defaults to False.
            audioRecorder (bool, optional): [This parameter enables the user to record audio]. Defaults to False.
            videoName (str, optional): [This parameter takes the file name for the video]. Defaults to 'video'.
            audioName (str, optional): [This parameter takes the file name for the audio]. Defaults to 'audio'.
            syncAudioVideo (bool, optional): [This parameter enables the user to sync audio and video together]. Defaults to False.
            destinationPath (str, optional): [This parameter enables the user to store their output files at the desired location.] Defaults to Outputs Folder.
        """
        
        startEyeTracking = False
        outputPath = destinationPath

        if os.access(destinationPath,os.W_OK) == False and destinationPath!='/Output':
            print('You may not have write permission.Try changing the destination path.')
            sys.exit()
        
        if os.path.exists(destinationPath) == False and destinationPath!='/Output':
            os.mkdir(destinationPath)
        elif destinationPath == '/Output':
            currentPath = os.getcwd()
            outputPath = currentPath + '/Output'
            if os.path.exists(outputPath) ==False:
                os.mkdir(outputPath)
        
        outputPath = outputPath + '/'

        if pupilTracking or blinkDetection:
            startEyeTracking = True

        if video_source !=0:
            if os.path.exists(video_source) == False:
                print('Please specify correct path for the video source.')
                sys.exit()

        
        if blinkDetection == True and pupilTracking == True:
            
            eyeTracking = PupilBlinking(video_source)
            eyeTrackingThread = threading.Thread(target=eyeTracking.start)
        
        if blinkDetection == True and pupilTracking == False:
            
            eyeTracking = Blinking(video_source)
            eyeTrackingThread = threading.Thread(target=eyeTracking.start)
        
        if pupilTracking == True and blinkDetection == False:
            
            eyeTracking = PupilTracking(video_source)
            eyeTrackingThread = threading.Thread(target=eyeTracking.start) 

        if syncAudioVideo == True:
            audioRecorder = True
            videoRecorder = True
        
        if videoRecorder == True:
            videoOutputPath = outputPath + videoName
            videoRecorder = VideoRecorder(videoOutputPath)
            videoRecorderThread = threading.Thread(target=videoRecorder.main)

        if audioRecorder == True:
            audioOutputPath = outputPath + audioName
            audioRecorder = AudioRecorder(outputPath + audioName) 
            audioRecorderThread = threading.Thread(target=audioRecorder.main)
        
        if UI == True:
            module = self.dynamic_import(UI_file_name)
            if hasattr(module, 'main'):
                uiThread = threading.Thread(target=module.main)
            else:
                print('UI needs a main method. Please Refer documentation for more information.')
                sys.exit()
        
        if UI:
            uiThread.start()
        
        if startEyeTracking == True:
            eyeTrackingThread.start()

        if videoRecorder == True:
            videoRecorderThread.start()

        if audioRecorder == True:
            audioRecorderThread.start()
        
        if UI:
            uiThread.join()

        if startEyeTracking == True:
            eyeTrackingThread.join()
            if eyeTrackingLog == True:
                eyeTrackingOutput = outputPath + eyeTrackingFileName
                eyeTracking.csv_writer(eyeTrackingOutput)
        
        if videoRecorder == True:
            videoRecorderThread.join()
            videoRecorder.stop()

        if audioRecorder == True:
            audioRecorderThread.join()
            audioRecorder.stop()

        if syncAudioVideo==True and audioRecorder==True and videoRecorder==True:

            file_name = audioName+videoName
            avOutputPath = outputPath + file_name
            
            cmd = 'ffmpeg -y -i '+audioOutputPath+'.wav  -r 30 -i '+videoOutputPath+'.avi  -filter:a aresample=async=1 -c:a flac -c:v copy '+avOutputPath+'.mkv'
            subprocess.call(cmd, shell=True)
            