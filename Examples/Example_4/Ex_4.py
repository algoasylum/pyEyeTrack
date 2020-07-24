from pyEyeTrack.PyEyeTrackRunnerClass import pyEyeTrack


ptr = pyEyeTrack()
ptr.pyEyeTrack_runner(
    pupilTracking=True,
    blinkDetection=True,
    video_source=r"#add path to the video file",
    eyeTrackingLog=True,
    eyeTrackingFileName='User_3')
