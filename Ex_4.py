from PyTrackRunnerClass import PyTrackRunner


ptr = PyTrackRunner()
ptr.pytrack_runner(
    pupilTracking=True,
    video_source=r"C:\Users\Kanchan\Downloads\Text_Reading\data\kanchan2\av.mkv",
    eyeTrackingLog=True,
    eyeTrackingFileName='User_3')
