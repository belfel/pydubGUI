from PyQt6.QtWidgets import (QApplication, QTabWidget, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, 
                            QDockWidget, QMainWindow, QFileDialog, QSpinBox, QDoubleSpinBox ,QCheckBox, QLineEdit)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QSize, Qt, QTimer
from datetime import timedelta
from AudioManager import AudioManager


class Window(QMainWindow):
    #Dodanie konstruktora przyjmującego okno nadrzędne
    def __init__(self, audioManager: AudioManager, parent=None):
        super().__init__(parent)
        self.am = audioManager
        self.setWindowTitle("Pydub GUI")
        self.setFixedSize(QSize(700, 400))
        #self.createMenu()
        self.createTabs()
        self.createDocks()
        

    def createDocks(self):
        slices = Slices(am)
        dock = Dock(am, slices, self.tab_gain, self.tab_cut, self.tab_merge, self.tab_fade, self.tab_export)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, slices)

        
    def createMenu(self):
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("File")
        self.actionExit = QAction('Exit', self)
        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.triggered.connect(self.close)
        self.fileMenu.addAction(self.actionExit)


    def createTabs(self):
        self.main = QWidget()
        self.mainLayout = QHBoxLayout()
        self.tabs = QTabWidget()
        self.tabs2 = QTabWidget()
        
        self.tab_gain = Gain(am)
        self.tab_cut = Cut(am)
        self.tab_merge = Merge(am)
        self.tab_fade = Fade(am)
        self.tab_export = Export(am)
        
        self.tabs.addTab(self.tab_gain, "Gain")        
        self.tabs.addTab(self.tab_cut, "Cut")        
        self.tabs.addTab(self.tab_merge, "Merge")
        self.tabs.addTab(self.tab_fade, "Fade")
        self.tabs2.addTab(self.tab_export, "Export")

        self.mainLayout.addWidget(self.tabs)
        self.mainLayout.addWidget(self.tabs2)
        self.main.setLayout(self.mainLayout)
        
        self.setCentralWidget(self.main)

class Gain(QWidget):
    def __init__(self, audioManager: AudioManager, parent=None):
        super().__init__(parent)
        self.am = audioManager
        layout = QVBoxLayout()
        self.spinBox = QDoubleSpinBox()
        self.statusText = QLabel("Select file first")
        self.label = QLabel("Select time section above, set gain (dB) and press apply.\nGain is additive.")
        self.spinBox.setMinimum(-20)
        self.spinBox.setMaximum(20)
        self.spinBox.setSingleStep(0.25)
        self.button = QPushButton("Apply")
        self.button.clicked.connect(self.apply)
        layout.addWidget(self.label)
        layout.addWidget(self.spinBox)
        layout.addWidget(self.button)
        layout.addWidget(self.statusText, alignment=Qt.AlignmentFlag.AlignBottom)
        self.setLayout(layout)
        self.button.blockSignals(True)
    
    def apply(self):
        self.statusText.setText("Applying...")
        self.statusText.show()
        self.repaint()
        am.applyGain(self.spinBox.value())
        self.spinBox.setValue(0)
        self.setStatusReady()

    def lockButton(self, bool: bool):
        if bool is True:
            self.statusText.setText("Stop playback to apply")
        else:
            self.statusText.setText("Ready")
        self.button.blockSignals(bool)

    def setStatusReady(self):
        self.statusText.setText("Ready")
        self.lockButton(False)

class Cut(QWidget):
    def __init__(self, audioManager: AudioManager, parent=None):
        super().__init__(parent)
        self.am = audioManager
        self.button = QPushButton("Apply")
        self.button.clicked.connect(self.apply)
        self.statusText = QLabel("Select file first")
        self.label = QLabel("Select time interval above and press apply to cut out everything outside the interval.\nCheck reverse to cut out everything inside the interval.")
        self.checkbox = QCheckBox("Reverse")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.button)
        layout.addWidget(self.statusText, alignment=Qt.AlignmentFlag.AlignBottom)

        self.setLayout(layout)
        self.button.blockSignals(True)
    
    def apply(self):
        self.statusText.setText("Applying...")
        self.statusText.show()
        self.repaint()
        am.cut(self.checkbox.isChecked())
        self.setStatusReady()

    def setStatusReady(self):
        self.statusText.setText("Ready")
        self.lockButton(False)

    def lockButton(self, bool: bool):
        if bool is True:
            self.statusText.setText("Stop playback to apply")
        else:
            self.statusText.setText("Ready")
        self.button.blockSignals(bool)

class Merge(QWidget):
    def __init__(self, audioManager: AudioManager, parent=None):
        super().__init__(parent)
        self.am = audioManager
        self.label = QLabel("No other file selected")
        self.crossfade = QSpinBox()
        self.crossfade.setMaximum(99999)
        self.crossfade.setSingleStep(100)
        self.button = QPushButton("Open")
        self.button2 = QPushButton("Apply")
        self.button3 = QPushButton("Repeat")
        self.button.clicked.connect(self.open)
        self.button2.clicked.connect(self.apply)
        self.button3.clicked.connect(self.repeat)
        self.statusText = QLabel("Select file first")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        #layout.addWidget(self.crossfade)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.statusText, alignment=Qt.AlignmentFlag.AlignBottom)

        self.setLayout(layout)
        self.button.blockSignals(True)
        self.button2.blockSignals(True)
        self.button3.blockSignals(True)
    
    def repeat(self):
        self.statusText.setText("Applying...")
        self.statusText.show()
        self.repaint()
        am.repeat()
        self.setStatusReady()

    def apply(self):
        self.statusText.setText("Applying...")
        self.statusText.show()
        self.repaint()
        am.merge()
        self.setStatusReady()

    def open(self):  
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Wybierz plik","", "Audio files (*.wav *.mp3)")
        am.openOtherFile(self.fileName)
        self.name, self.duration, self.ext = am.getOtherFileInfo()
        self.label.setText(self.name + self.ext + " | Duration: " + (str)(timedelta(seconds=self.duration)).split(".")[0])

    def setStatusReady(self):
        self.statusText.setText("Ready")
        self.lockButtons(False)

    def lockButtons(self, bool: bool):
        if bool is True:
            self.statusText.setText("Stop playback to apply")
        else:
            self.statusText.setText("Ready")
        self.button.blockSignals(bool)
        self.button2.blockSignals(bool)
        self.button3.blockSignals(bool)

class Fade(QWidget):
    def __init__(self, audioManager: AudioManager, parent=None):
        super().__init__(parent)
        self.am = audioManager
        self.button = QPushButton("Apply")
        self.button.clicked.connect(self.apply)
        self.statusText = QLabel("Select file first")
        self.label = QLabel("Select time interval above and press apply to apply fade out effect.\nCheck Fade out to apply fade in effect instead.")
        self.checkbox = QCheckBox("Fade in")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.button)
        layout.addWidget(self.statusText, alignment=Qt.AlignmentFlag.AlignBottom)

        self.setLayout(layout)
        self.button.blockSignals(True)
    
    def apply(self):
        self.statusText.setText("Applying...")
        self.statusText.show()
        self.repaint()
        am.fade(self.checkbox.isChecked())
        self.setStatusReady()

    def setStatusReady(self):
        self.statusText.setText("Ready")
        self.lockButton(False)

    def lockButton(self, bool: bool):
        if bool is True:
            self.statusText.setText("Stop playback to apply")
        else:
            self.statusText.setText("Ready")
        self.button.blockSignals(bool)

class Export(QWidget):
    def __init__(self, audioManager: AudioManager, parent=None):
        super().__init__(parent)
        self.am = audioManager
        self.button = QPushButton("Export")
        self.button.clicked.connect(self.apply)
        self.label = QLabel("Bitrate:")
        self.bitrate = QLineEdit("192000")
        self.statusText = QLabel("Select file first")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.bitrate)
        layout.addWidget(self.button)
        layout.addWidget(self.statusText, alignment=Qt.AlignmentFlag.AlignBottom)

        self.setLayout(layout)
        self.button.blockSignals(True)
    
    def apply(self):
        name, _ = QFileDialog.getSaveFileName(self, 'Save File')

        self.statusText.setText("Saving...")
        self.statusText.show()
        self.repaint()
        am.export(name, 192000)
        self.setStatusReady()

    def setStatusReady(self):
        self.statusText.setText("Ready")
        self.lockButton(False)

    def lockButton(self, bool: bool):
        if bool is True:
            self.statusText.setText("Stop playback to export")
        else:
            self.statusText.setText("Ready")
        self.button.blockSignals(bool)

class Slices(QDockWidget):
    def __init__(self, audioManager: AudioManager, parent=None):
        super().__init__(parent)
        self.am = audioManager
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.dockWidget = QWidget()
        self.layout = QHBoxLayout()
        self.isSongSelected = False
        
        self.initFields()

        self.dockWidget.setLayout(self.layout)
        self.setWidget(self.dockWidget)
    
    def initFields(self):
        self.fieldLH = QSpinBox()
        self.fieldLH.valueChanged.connect(self.onSectionChangedLeft)
        self.fieldLH.setMaximum(23)
        self.fieldLM = QSpinBox()
        self.fieldLM.valueChanged.connect(self.onSectionChangedLeft)
        self.fieldLM.setMaximum(59)
        self.fieldLS = QSpinBox()
        self.fieldLS.valueChanged.connect(self.onSectionChangedLeft)
        self.fieldLS.setMaximum(59)

        self.fieldRH = QSpinBox()
        self.fieldRH.valueChanged.connect(self.onSectionChangedRight)
        self.fieldRH.setMaximum(23)
        self.fieldRM = QSpinBox()
        self.fieldRM.valueChanged.connect(self.onSectionChangedRight)
        self.fieldRM.setMaximum(59)
        self.fieldRS = QSpinBox()
        self.fieldRS.valueChanged.connect(self.onSectionChangedRight)
        self.fieldRS.setMaximum(59)

        self.labelLH = QLabel("From: (hh:mm:ss)")
        self.labelLM = QLabel(":")
        self.labelLS = QLabel(":")
        self.labelRH = QLabel("To: (hh:mm:ss)")
        self.labelRM = QLabel(":")
        self.labelRS = QLabel(":")

        self.layout.addWidget(self.labelLH, alignment=Qt.AlignmentFlag.AlignLeft, stretch=0)
        self.layout.addWidget(self.fieldLH)
        self.layout.addWidget(self.labelLM, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.fieldLM)
        self.layout.addWidget(self.labelLS, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.fieldLS)
        self.layout.addWidget(self.labelRH, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.fieldRH)
        self.layout.addWidget(self.labelRM, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.fieldRM)
        self.layout.addWidget(self.labelRS, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.fieldRS)
        self.layout.addWidget(QWidget(None), stretch=1)
    
    def setDuration(self, durationSeconds):
        self.durationH, minutes = divmod(durationSeconds, 3600)
        self.durationM, self.durationS = divmod(minutes, 60)

        self.fieldLH.setMaximum(self.durationH)
        self.fieldRH.setMaximum(self.durationH)
        self.fieldRH.setValue(self.durationH)
        self.fieldLH.setValue(0)
        self.fieldRM.setMaximum(self.durationM)
        self.fieldRM.setValue(self.durationM)
        self.fieldLM.setValue(0)
        self.fieldRS.setMaximum(self.durationS)
        self.fieldRS.setValue(self.durationS)
        self.fieldLS.setValue(0)
    
    def onSectionChangedLeft(self):
        if self.isSongSelected:
            self.onSectionChanged()
            am.onSectionChangeLeft(self.fieldLH.value() * 3600 + self.fieldLM.value() * 60 + self.fieldLS.value())

    def onSectionChangedRight(self):
        if self.isSongSelected:
            self.onSectionChanged()
            am.onSectionChangeRight(self.fieldRH.value() * 3600 + self.fieldRM.value() * 60 + self.fieldRS.value())

    def onSectionChanged(self):
        if self.fieldLH.value() == self.durationH:
            self.fieldLM.setMaximum(self.durationM)
        else:
            self.fieldLM.setMaximum(59)

        if self.fieldRH.value() == self.durationH:
            self.fieldRM.setMaximum(self.durationM)
        else:
            self.fieldRM.setMaximum(59)

        if self.fieldLM.value() == self.durationM:
            self.fieldLS.setMaximum(self.durationS)
        else:
            self.fieldLS.setMaximum(59)

        if self.fieldRM.value() == self.durationM:
            self.fieldRS.setMaximum(self.durationS)
        else:
            self.fieldRS.setMaximum(59)

    def songSelected(self):
        self.isSongSelected = True

class Dock(QDockWidget):
    def __init__(self, audioManager: AudioManager, slices: Slices, gain: Gain, cut: Cut, merge: Merge, fade: Fade, export: Export, parent=None):
        super().__init__(parent)
        self.am = audioManager
        self.gain = gain
        self.slices = slices
        self.cut = cut
        self.merge = merge
        self.fade = fade
        self.export = export
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.setTitleBarWidget(QWidget(None))
        self.dockWidget = QWidget()
        self.layout = QHBoxLayout()
        buttonOpen = QPushButton("Open file")
        buttonOpen.clicked.connect(self.open)
        self.textFilename = QLabel("No file opened")
        self.textDuration = QLabel("0:00:00/0:00:00")
        self.buttonPlay = QPushButton("Play")
        self.buttonPlay.clicked.connect(self.play)
        self.buttonPlay.blockSignals(True)
        self.layout.addWidget(buttonOpen)
        self.layout.addWidget(self.textFilename)
        self.layout.addWidget(self.textDuration, alignment=Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.buttonPlay)
        self.dockWidget.setLayout(self.layout)
        self.setWidget(self.dockWidget)
        self.isPlaying = False
        self.playbackTime = "0:00:00"
        self.playbackTimeMs = 0
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.playbackCounterUp)
        self.cut.button.clicked.connect(self.updateInfo)
        self.merge.button2.clicked.connect(self.updateInfo)
        self.merge.button3.clicked.connect(self.updateInfo)
        
    def playbackCounterUp(self):
        self.playbackTimeMs += 100
        self.playbackTime = (str)(timedelta(milliseconds=self.playbackTimeMs)).split(".")[0]
        self.playbackCounterUpdate()
        if self.playbackTimeMs > self.fileDuration * 1000:
            self.stop()

    def playbackCounterReset(self):
        self.playbackTimeMs = 0
        self.playbackTime = (str)(timedelta(milliseconds=self.playbackTimeMs)).split(".")[0]
        self.playbackCounterUpdate()

    def playbackCounterUpdate(self):
        duration = self.textDuration.text().split("/")[1]
        self.textDuration.setText(self.playbackTime + "/" + duration)

    def open(self):
        if (self.isPlaying):
            self.stop()
        
        fileName, _ = QFileDialog.getOpenFileName(self, "Wybierz plik","", "Audio files (*.wav *.mp3)")
        if fileName:
            am.openMainFile(fileName)
            self.updateInfo()
            self.buttonPlay.blockSignals(False)
            self.updateStatus()
            self.slices.songSelected()

    def updateInfo(self):
        name, duration, ext = am.getMainFileInfo()
        self.fileDuration = duration
        durationText = (str)(timedelta(seconds=duration)).split(".")[0]
        self.textFilename.setText(name + ext)
        self.textDuration.setText(self.playbackTime + "/" + durationText)
        self.slices.setDuration((int)(duration))
        
    def play(self):
        self.buttonPlay.setText("Stop")
        self.buttonPlay.clicked.disconnect(self.play)
        self.buttonPlay.clicked.connect(self.stop)
        self.isPlaying = True
        self.lockButtons(True)
        self.timer.start()
        am.play()

    def stop(self):
        am.pause()
        self.timer.stop()
        self.playbackCounterReset()
        self.isPlaying = False
        self.buttonPlay.setText("Play")
        self.buttonPlay.clicked.disconnect(self.stop)
        self.buttonPlay.clicked.connect(self.play)
        self.lockButtons(False)
    
    def updateStatus(self):
        self.gain.setStatusReady()
        self.cut.setStatusReady()
        self.merge.setStatusReady()
        self.fade.setStatusReady()
        self.export.setStatusReady()

    def lockButtons(self, bool: bool):
        self.gain.lockButton(bool)
        self.cut.lockButton(bool)
        self.merge.lockButtons(bool)
        self.fade.lockButton(bool)
        self.export.lockButton(bool)


if __name__ == '__main__':
    am = AudioManager()
    app = QApplication([])
    win = Window(am)
    win.show()
    app.exec()