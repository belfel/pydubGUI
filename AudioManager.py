from pydub import AudioSegment
import os
from playsound import playsound
import multiprocessing

class AudioManager:
    def __init__(self, parent=None):
        self.mainFile: AudioSegment = None
        self.otherFile: AudioSegment = None
        self.playback = None
        self.mainFileName = ""
        self.mainFileExt = ""
        self.mainFilePath = ""
        self.otherFileName = ""
        self.otherFileExt = ""
        self.tempFileName = "temp.mp3"
        self.tempFilePath = ""
        self.sectionLeft = 0
        self.sectionRight = 0
        self.songSectionMiddle: AudioSegment = None
        self.songSectionLeft: AudioSegment = None
        self.songSectionRight: AudioSegment = None
        
    def openMainFile(self, filepath: str):
        self.mainFilePath = filepath.replace("/", "\\")
        path, self.mainFileExt = os.path.splitext(filepath)
        self.mainFileName = os.path.basename(path)
        self.tempFilePath = self.mainFilePath.replace(self.mainFileName, self.tempFileName)
        self.mainFile = AudioSegment.from_file(filepath, self.mainFileExt[1:])
        self.sectionRight = (int)(self.mainFile.duration_seconds * 1000)
        self.updateSection()
        self.saveTemp()

    def openOtherFile(self, filepath: str):
        otherFilePath = filepath.replace("/", "\\")
        path, self.otherFileExt = os.path.splitext(otherFilePath)
        self.otherFileName = os.path.basename(path)
        self.otherFile = AudioSegment.from_file(filepath, self.otherFileExt[1:])

    def play(self):
        if self.mainFile:
            self.playback = multiprocessing.Process(target=playsound, args=(self.tempFileName,))
            self.playback.daemon = True
            self.playback.start()
                 
    def pause(self):
        if self.playback:
            self.playback.terminate()

    def getMainFileInfo(self):
        filename = self.mainFileName
        durationSeconds = self.mainFile.duration_seconds
        extension = self.mainFileExt
        return filename, durationSeconds, extension

    def getOtherFileInfo(self):
        return self.otherFileName, self.otherFile.duration_seconds, self.otherFileExt

    def applyGain(self, gain):
        if self.mainFile:
            withGain = self.songSectionMiddle.apply_gain(gain)
            self.mainFile = self.songSectionLeft + withGain + self.songSectionRight
            self.saveTemp()

    def cut(self, reverse: bool = False):
        if self.mainFile:
            if reverse:
                self.mainFile = self.songSectionLeft + self.songSectionRight
            else:
                self.mainFile = self.songSectionMiddle
            self.saveTemp()
        
    def merge(self):
        if self.mainFile:
            self.mainFile = self.songSectionMiddle + self.otherFile
            self.saveTemp()

    def repeat(self):
        self.mainFile = self.mainFile + self.mainFile
        self.saveTemp()

    def fade(self, fadeIn=True):
        if self.mainFile:
            duration = (int)(self.songSectionMiddle.duration_seconds * 1000)

            if fadeIn:
                self.mainFile = self.songSectionLeft + self.songSectionMiddle.fade_in(duration) + self.songSectionRight
            else:
                self.mainFile = self.songSectionLeft + self.songSectionMiddle.fade_out(duration) + self.songSectionRight
            self.saveTemp()

    def export(self, path: str, bitrate: int):
        ext = path.split(".")[1]
        pathFixed = path.replace("/", "\\")
        self.mainFile.export(pathFixed, format="mp3", bitrate=(str)(bitrate))

    def saveTemp(self):
        self.mainFile.export(self.tempFileName, format="mp3", bitrate="192k")

    def onSectionChangeLeft(self, amount : int):
        self.sectionLeft = amount * 1000
        self.updateSection()

    def onSectionChangeRight(self, amount : int):
        self.sectionRight = amount * 1000
        self.updateSection()
    
    def updateSection(self):
        self.songSectionLeft = self.mainFile[:self.sectionLeft]
        self.songSectionMiddle = self.mainFile[self.sectionLeft : self.sectionRight]
        self.songSectionRight = self.mainFile[self.sectionRight:]