from PyTrackRunnerClass import PyTrackRunner


ptr = PyTrackRunner()
ptr.pytrack_runner(
    UI=True,
    UI_file_name='Ex_5_ImageUI_EscExit',
    pupilTracking=True,
    blinkDetection=True,
    eyeTrackingLog=True,
    eyeTrackingFileName='User_4',
    audioRecorder=True,
    audioName='audio4',
    videoName='video4',
    videoRecorder=True,
    syncAudioVideo=True,
    destinationPath=r'C:\Users\Kanchan\Desktop')
    