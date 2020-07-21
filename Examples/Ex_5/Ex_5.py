from PyTrackRunnerClass import pytrack


ptr = pytrack()
ptr.pytrack_runner(
    UI=True,
    UI_file_name='Ex_5_ImageUI_EscExit',
    audioRecorder=True,
    audioName='audio4',
    videoName='video4',
    videoRecorder=True,
    syncAudioVideo=True)
    
