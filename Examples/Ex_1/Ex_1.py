from PyTrackRunnerClass import pytrack

ptr = pytrack()
ptr.pytrack_runner(
    UI=True,
    UI_file_name='Ex_1_SampleTextUI',
    pupilTracking=True,
    eyeTrackingLog=True,
    eyeTrackingFileName='User_1')
