from pyEyeTrack.PyEyeTrackRunnerClass import pyEyeTrack


ptr = pyEyeTrack()
ptr.pyEyeTrack_runner(
    UI=True,
    UI_file_name='Ex_5_ImageUI_EscExit',
    audioRecorder=True,
    audioName='audio5',
    videoName='video5',
    videoRecorder=True)
    
