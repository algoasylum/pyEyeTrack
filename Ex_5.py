from PyTrackRunnerClass import PyTrackRunner


ptr = PyTrackRunner()


#ptr.pytrack_runner(UI_file_name = 'Ex_5_ImageUI_EscExit',flagUI = True,flagPupilTracking = True, 
#                eyeTrackingLog = True, eyeTrackingFileName = 'User_4', 
#                flagAudioRecorder = True, audioName = 'audio4',videoName = 'video4', 
#                flagVideoRecorder = True, flagSyncAudioVideo = True,destinationPath=r'C:\Users\Kanchan\Desktop')


ptr.pytrack_runner(UI_file_name = 'Ex_5_ImageUI_EscExit',UI = True, pupilTracking=True,blinkDetection=True,
                eyeTrackingLog= True)
