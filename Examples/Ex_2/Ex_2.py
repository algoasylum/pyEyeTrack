from PyTrackRunnerClass import PyTrackRunner


ptr = PyTrackRunner()
ptr.pytrack_runner(
    UI=True,
    UI_file_name='Ex_2_ImageUI',
    blinkDetection=True,
    eyeTrackingLog=True,
    eyeTrackingFileName='User_2')
