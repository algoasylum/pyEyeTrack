from EyeTracking.PupilTrackingClass import PupilTracking
from EyeTracking.BlinkingClass import Blinking
from EyeTracking.PupilBlinkingClass import PupilBlinking
from AudioVideoRecording.VideoRecordingClass import VideoRecorder
from AudioVideoRecording.AudioRecordingClass import AudioRecorder
import threading
import importlib
import sys
import subprocess


class PyTrackRunner():

    def __init__(self):
        pass


    def dynamic_import(self,module):
        return importlib.import_module(module)

    def pytrack_runner(self, UI_file_name = "User_ImageUI_EscExit", eyeTrackingFileName='EyeTrackLog', video_source = 0 ,flagUI = False, 
    flagPupilTracking = False, flagBlinkDetection = False,eyeTrackingLog=True, flagPupilTrackingBlinkDetection = False, 
    flagVideoRecorder = False, flagAudioRecorder = False,videoName = 'video',audioName = 'audio', flagSyncAudioVideo = False):
        """[This function enables the user to run the functionalities of the library simultaneously. 
        Functionalities include running the UI specified by the user, pupil tracking, blink detection, video recording and audio recording.
        The user can set flags to run the combination of these functionalities. The function allows the user to name the output file.]

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
        """
        
        startEyeTracking = False

       
        if flagPupilTrackingBlinkDetection or flagPupilTracking or flagBlinkDetection:
            startEyeTracking = True
        
        if flagPupilTrackingBlinkDetection == True:
            
            eyeTracking = PupilBlinking(video_source)
            eyeTrackingThread = threading.Thread(target=eyeTracking.start)
        
        if flagBlinkDetection == True:
            
            eyeTracking = Blinking(video_source)
            eyeTrackingThread = threading.Thread(target=eyeTracking.start)
        
        if flagPupilTracking == True:
            
            eyeTracking = PupilTracking(video_source)
            eyeTrackingThread = threading.Thread(target=eyeTracking.start) 
        
        if flagVideoRecorder == True:
            
            videoRecorder = VideoRecorder(videoName)
            videoRecorderThread = threading.Thread(target=videoRecorder.main)

        if flagAudioRecorder == True:
            
            audioRecorder = AudioRecorder(audioName) 
            audioRecorderThread = threading.Thread(target=audioRecorder.main)
        
        if flagUI == True:
            module = self.dynamic_import(UI_file_name)
            uiThread = threading.Thread(target=module.main)
        
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
                eyeTracking.csv_writer(eyeTrackingFileName)
        
        if flagVideoRecorder == True:
            videoRecorderThread.join()
            videoRecorder.stop()

        if flagAudioRecorder == True:
            audioRecorderThread.join()
            audioRecorder.stop()

        if flagSyncAudioVideo==True and flagAudioRecorder==True and flagVideoRecorder==True:
            file_name = audioName+videoName
            cmd = 'ffmpeg -y -i '+audioName+'.wav  -r 30 -i '+videoName+'.avi  -filter:a aresample=async=1 -c:a flac -c:v copy '+file_name+'.mkv'
            subprocess.call(cmd, shell=True)
