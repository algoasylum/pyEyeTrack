from pyEyeTrack.PyEyeTrackRunnerClass import pyEyeTrack


ptr = pyEyeTrack()
ptr.pyEyeTrack_runner(
    UI=True,
    UI_file_name='Ex_3_SlotsMachine',
    blinkDetection=True,
    eyeTrackingLog=False)
