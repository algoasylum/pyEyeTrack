from pyEyeTrack.PyEyeTrackRunnerClass import pyEyeTrack


ptr = pyEyeTrack()
ptr.pyEyeTrack_runner(
    pupilTracking=True,
    blinkDetection=True,
    video_source=r"#add path of the video input",
    eyeTrackingLog=True,
    eyeTrackingFileName='User_3')
