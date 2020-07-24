from pyEyeTrack.PyEyeTrackRunnerClass import pyEyeTrack

ptr = pyEyeTrack()
ptr.pyEyeTrack_runner(
    UI=True,
    UI_file_name='Ex_1_SampleTextUI',
    pupilTracking=True,
    eyeTrackingLog=True,
    eyeTrackingFileName='User_1')
