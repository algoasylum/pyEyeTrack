from PyTrackRunnerClass import PyTrackRunner


ptr = PyTrackRunner()
ptr.pytrack_runner(UI_file_name = 'User_ImageUI_EscExit',flagUI = True,flagPupilTracking = True, 
                eyeTrackingLog = True, eyeTrackingFileName = 'User_4', 
                flagAudioRecorder = True, audioName = 'audio4',videoName = 'video', 
                flagVideoRecorder = True, flagSyncAudioVideo = True)

