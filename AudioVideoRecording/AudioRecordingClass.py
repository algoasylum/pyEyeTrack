import cv2
import pyaudio
import wave
import threading
import time
import subprocess
import os,shutil
import sys,re



class AudioRecorder():

    def __init__(self,file_name = 'audio'):
        self.open = True
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.file_name = file_name+".wav"
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,channels=self.channels,rate=self.rate,input=True,frames_per_buffer=self.frames_per_buffer)
        self.audioframes = []

    def record(self):
        """[The function records audio until the open flag is set to false. 
        The frames read by the stream are appended into audio frames.]
        """
        self.stream.start_stream()
        while(self.open ==True):
            data = self.stream.read(self.frames_per_buffer)  
            self.audioframes.append(data)
            if self.open==False:
                break
        

    def stop(self):
        """[The function stops recording audio, thereby also stopping the thread. 
        Audio frames are written into a .wav file. The stream is stopped and closed. ]
        """
        if self.open==True:
            print("Audio Stop")
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            
            waveFile = wave.open (self.file_name,'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audioframes))
            waveFile.close()
        
        else:
            pass
    
    def main(self):
        """[The function launches audio recording function as a thread.]
        """
        audio_thread = threading.Thread(target=self.record,)
        audio_thread.start()
    
   




