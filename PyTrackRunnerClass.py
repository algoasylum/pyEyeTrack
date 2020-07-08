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

    def pytrack_runner(self, UI_file_name = "User_ImageUI_EscExit", eyeTrackingFileName='EyeTrackLog', video_source = 0 ,flagUI = False, 
    flagPupilTracking = False, flagBlinkDetection = False,eyeTrackingLog=True, flagPupilTrackingBlinkDetection = False, 
    flagVideoRecorder = False, flagAudioRecorder = False,videoName = 'video',audioName = 'audio', flagSyncAudioVideo = False, destinationPath = '/Output'):
        """
        This function enables the user to run the functionalities of the library simultaneously. 
        Functionalities include running the UI specified by the user, pupil tracking, blink detection, video recording and audio recording.
        The user can set flags to run the combination of these functionalities. The function allows the user to name the output file.

        Args:
            UI_file_name (str, optional): [This parameter takes the file name of the UI]. Defaults to "User_ImageUI_EscExit".
            eyeTrackingFileName (str, optional): [This parameter takes the file name for the CSV]. Defaults to 'EyeTrackLog'.
            video_source (int/str, optional): [This parameter takes either device index or a video file as input]. Defaults to 0.
            flagUI (bool, optional): [This parameter enables the user to run UI]. Defaults to False.
            flagPupilTracking (bool, optional): [This parameter enables the user to run pupil tracking]. Defaults to False.
            flagBlinkDetection (bool, optional): [This parameter enables the user to run blink detection]. Defaults to False.
            eyeTrackingLog (bool, optional): [This parameter enables the user to generate a CSV of pupil tracking/ blink detection]. Defaults to True.
            flagPupilTrackingBlinkDetection (bool, optional): [This parameter enables the user to run pupil tracking and blink detection simultaneously]. Defaults to False.
            flagVideoRecorder (bool, optional): [This parameter enables the user to record video]. Defaults to False.
            flagAudioRecorder (bool, optional): [This parameter enables the user to record audio]. Defaults to False.
            videoName (str, optional): [This parameter takes the file name for the video]. Defaults to 'video'.
            audioName (str, optional): [This parameter takes the file name for the audio]. Defaults to 'audio'.
            flagSyncAudioVideo (bool, optional): [This parameter enables the user to sync audio and video together]. Defaults to False.
            destinationPath (str, optional): [This parameter enables the user to store their output files at the desired location.] Defaults to Outputs Folder.
        """
        
        startEyeTracking = False
        outputPath = destinationPath
        
        if os.path.exists(destinationPath) == False and destinationPath!='/Output':
            os.mkdir(destinationPath)
        elif destinationPath == '/Output':
            currentPath = os.getcwd()
            outputPath = currentPath + '/Output'
            if os.path.exists(outputPath) ==False:
                os.mkdir(outputPath)
        
        outputPath = outputPath + '/'

        if flagPupilTrackingBlinkDetection or flagPupilTracking or flagBlinkDetection:
            startEyeTracking = True

        if video_source !=0:
            if os.path.exists(video_source) == False:
                print('Please specify correct path for the video source.')
                sys.exit()

        
        if flagPupilTrackingBlinkDetection == True:
            
            eyeTracking = PupilBlinking(video_source)
            eyeTrackingThread = threading.Thread(target=eyeTracking.start)
        
        if flagBlinkDetection == True:
            
            eyeTracking = Blinking(video_source)
            eyeTrackingThread = threading.Thread(target=eyeTracking.start)
        
        if flagPupilTracking == True:
            
            eyeTracking = PupilTracking(video_source)
            eyeTrackingThread = threading.Thread(target=eyeTracking.start) 

        if flagSyncAudioVideo == True:

            flagAudioRecorder = True
            flagVideoRecorder = True
        
        if flagVideoRecorder == True:
            videoOutputPath = outputPath + videoName
            videoRecorder = VideoRecorder(videoOutputPath)
            videoRecorderThread = threading.Thread(target=videoRecorder.main)

        if flagAudioRecorder == True:
            audioOutputPath = outputPath + audioName
            audioRecorder = AudioRecorder(outputPath + audioName) 
            audioRecorderThread = threading.Thread(target=audioRecorder.main)
        
        if flagUI == True:
            module = self.dynamic_import(UI_file_name)
            if hasattr(module, 'main'):
                uiThread = threading.Thread(target=module.main)
            else:
                print('UI needs a main method. Please Refer documentation for more information.')
                sys.exit()
        
        if flagUI:
            uiThread.start()
        
        if startEyeTracking == True:
            eyeTrackingThread.start()

        if flagVideoRecorder == True:
            videoRecorderThread.start()

        if flagAudioRecorder == True:
            audioRecorderThread.start()
        
        if flagUI:
            uiThread.join()

        if startEyeTracking == True:
            eyeTrackingThread.join()
            if eyeTrackingLog == True:
                eyeTrackingOutput = outputPath + eyeTrackingFileName
                eyeTracking.csv_writer(eyeTrackingOutput)
        
        if flagVideoRecorder == True:
            videoRecorderThread.join()
            videoRecorder.stop()

        if flagAudioRecorder == True:
            audioRecorderThread.join()
            audioRecorder.stop()

        if flagSyncAudioVideo==True and flagAudioRecorder==True and flagVideoRecorder==True:

            file_name = audioName+videoName
            avOutputPath = outputPath + file_name
            
            cmd = 'ffmpeg -y -i '+audioOutputPath+'.wav  -r 30 -i '+videoOutputPath+'.avi  -filter:a aresample=async=1 -c:a flac -c:v copy '+avOutputPath+'.mkv'
            subprocess.call(cmd, shell=True)
            