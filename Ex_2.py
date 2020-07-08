from PyTrackRunnerClass import PyTrackRunner


ptr = PyTrackRunner()
ptr.pytrack_runner(UI_file_name = 'Ex_2_ImageUI',UI = True,pupilTracking= True, blinkDetection=True, 
                eyeTrackingLog = True, eyeTrackingFileName= 'User_2')

