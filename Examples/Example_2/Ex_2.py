from pyEyeTrack.PyEyeTrackRunnerClass import pyEyeTrack

ptr = pyEyeTrack()
ptr.pyEyeTrack_runner(
    UI=True,
    UI_file_name='Ex_2_ImageUI',
    blinkDetection=True,
    eyeTrackingLog=True,
    eyeTrackingFileName='User_2')
