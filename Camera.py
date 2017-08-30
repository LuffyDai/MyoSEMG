#！、usr/bin/env.python
#._*_ coding:utf-8 _*_

#视频播放、及摄像头

import cv2, time, myo_emg, capture, numpy, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

camera_port = 0


class VideoThread(QThread):

    stop_signal = pyqtSignal()
    start_signal = pyqtSignal()
    image_siganl = pyqtSignal(numpy.ndarray)

    def __init__(self, name, ui=myo_emg.Ui_MainWindow(), cap=capture.capture()):
        super(VideoThread, self).__init__()
        self.flag = True
        self.start_flag = False
        self.support_flag = True
        self.name = name
        self.cap = cap
        self.ui = ui
        self.out = None
        self.stop_signal.connect(self.stop_play)
        self.image_siganl.connect(self.saving_video)
        self.start_signal.connect(self.start_capture)
        self.cap.path_signal.connect(self.save_video)
        if self.name == "Video":
            self.videoLabel = ui.Video
            self.camera = cv2.VideoCapture("instruction.mp4")
            self.fps = self.camera.get(cv2.CAP_PROP_FPS)
        elif self.name == "Camera":
            self.videoLabel = ui.Camera
            self.camera = cv2.VideoCapture(camera_port)

    def start_play(self):
        if self.flag:
            self.start()
        else:
            self.flag = True

    def start_camera(self, ui):
        if self.camera.isOpened():
            ui.listWidget.addItem('Camera has been opened...')
            self.start()
        else:
            ui.listWidget.addItem('No camera dedected...')

    def run(self):

        while True:
            if self.flag:
                ret, image = self.camera.read()
                if image is None:
                    break
                color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                height, width, _ = color_swapped_image.shape

                qt_image = QImage(color_swapped_image.data,
                                  width,
                                  height,
                                  color_swapped_image.strides[0],
                                  QImage.Format_RGB888)
                pixmap = QPixmap(qt_image)
                pixmap = pixmap.scaled(self.videoLabel.geometry().width(), self.videoLabel.geometry().height())
                if self.start_flag and self.support_flag:
                    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
                    self.path = "appdata/" + self.cap.guide.dataset_type + "/data/" + self.cap.date_str + "-" + str(
                        self.cap.guide.gesture_type) + ".avi"
                    self.out = cv2.VideoWriter(self.path, fourcc, 20.0, (640, 480))
                    self.support_flag = False
                if self.name == "Camera" and self.out is not None:
                    self.image_siganl.emit(image)
                self.videoLabel.setPixmap(pixmap)
                if self.name == "Video":
                    time.sleep(1/self.fps)
            else:
                pass

    def stop_play(self):
        self.flag = False

    def start_capture(self):
        self.start_flag = True

    def saving_video(self, image):
        self.out.write(image)

    def save_video(self, path_str):
        if self.out is not None:
            self.out.release()
            os.rename(self.path, path_str+".avi")
            self.ui.listWidget.addItem('Video has been saved...')
        else:
            pass



















