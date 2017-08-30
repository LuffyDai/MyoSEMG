#！、usr/bin/env.python
#._*_ coding:utf-8 _*_
# myo_emg.py中需要加上import darkstyle.py
# 并且Canvas需要进行改动

import sys, capture, Camera, replay, video_Window
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QStyle
import myo_emg, logging, MyBar
from PyQt5.QtCore import QFile, QTextStream, Qt, QUrl
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

instruction_path = 'C:/input/avi1.avi'
def _logger():
    return logging.getLogger('darkstyle')


def load_darkstyle():
    f = QFile("darkstyle\style.qss")
    if not f.exists():
        _logger().error("Unable to load stylesheet, file not  in resources")
        return ""
    else:
        f.open(QFile.ReadOnly|QFile.Text)
        ts = QTextStream(f)
        stylesheet = ts.readAll()
        return stylesheet


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout = QVBoxLayout()
        w = QMainWindow()

        self.ui = myo_emg.Ui_MainWindow()
        self.ui.setupUi(w)

        self.capture = capture.capture()
        self.guide = self.capture.guide
        self.data = self.capture.Data
        self.replay = replay.replay()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)


        #self.thread = Camera.VideoThread("Video", self.ui, self.capture)
        self.thread2 = Camera.VideoThread("Camera", self.ui, self.capture)
        self.video_window = video_Window.VideoWindow()

        #self.ui.menuCapture.setStyleSheet(load_darkstyle())
        self.ui.actionStop_Capture.setShortcut('space')
        self.ui.actionStart_Capture.setShortcut('ctrl+A')
        self.ui.actionCapture_emg.setCheckable(True)
        self.ui.actionCapture_emg.setChecked(True)
        self.ui.actionCapture_imu.setCheckable(True)
        self.ui.Camera_Button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.ui.Video_Button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))




        self.ui.actionStart_Capture.triggered.connect(lambda: self.guide.start(self, self.ui))#对于有参数的函数需要如此使用
        #self.ui.actionStart_Capture.triggered.connect(self.thread.start_play)
        self.ui.actionStart_Capture.triggered.connect(self.thread2.start_signal.emit)
        self.ui.actionStop_Capture.triggered.connect(lambda: self.guide.stop(self.ui))
        #self.ui.actionStop_Capture.triggered.connect(self.thread.stop_signal.emit)
        self.guide.rest_timer.timeout.connect(lambda: self.guide.rest_event(self.ui))
        self.guide.capture_timer.timeout.connect(lambda: self.guide.capture_event(self.ui))
        self.ui.actionCapture_imu.toggled.connect(self.data.switch_IMU)
        self.ui.actionCapture_emg.toggled.connect(self.data.switch_EMG)
        self.ui.actionMyo.triggered.connect(lambda: self.capture.open_Myo(self.ui))
        self.ui.actionCamera.triggered.connect(lambda: self.thread2.start_camera(self.ui))
        self.ui.actionSave.triggered.connect(lambda: self.capture.save_file(self.guide, self.ui))
        #self.ui.actionSave.triggered.connect(self.thread2.stop_signal.emit)
        self.ui.actionSave_Profile.triggered.connect(lambda: self.replay.create_profile(self.ui, self.capture))
        self.ui.actionLoad_Profile.triggered.connect(lambda: self.replay.load_profile(self))
        self.replay.video_signal.connect(self.video_window.replay_video)

        self.mediaPlayer.setVideoOutput(self.ui.Video)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.ui.Video_Button.clicked.connect(self.play)
        self.ui.Video_slider.sliderMoved.connect(self.setPosition)
        self.ui.actionStart_Capture.triggered.connect(self.start_ins)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.titlebar = MyBar.MyBar(self)
        self.titlebar.pushButtonClose.clicked.connect(self.capture.stop_thread)
        self.layout.addWidget(self.titlebar)
        self.layout.addWidget(w)

        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        #self.layout.addStretch(1)
        self.setMinimumSize(831, 674)

        self.pressing = False
        self.maxNormal = True

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.Video_Button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.ui.Video_Button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.ui.Video_slider.setValue(position)

    def durationChanged(self, duration):
        self.ui.Video_slider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def start_ins(self):
        self.ui.Video.setAspectRatioMode(Qt.IgnoreAspectRatio)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(instruction_path)))
        self.ui.Video_Button.setEnabled(True)
        self.play()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    #w = QMainWindow(parent=None, flags=Qt.FramelessWindowHint)
    mw = MainWindow()
    app.setStyleSheet(load_darkstyle())
    mainFont = app.font()
    mainFont.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(mainFont)
    mw.show()

    sys.exit(app.exec_())
