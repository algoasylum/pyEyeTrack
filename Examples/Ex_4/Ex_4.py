from PyTrackRunnerClass import pytrack


ptr = pytrack()
ptr.pytrack_runner(
    pupilTracking=True,
    blinkDetection=True,
    video_source=r"#add path of the video input",
    eyeTrackingLog=True,
    eyeTrackingFileName='User_3')
