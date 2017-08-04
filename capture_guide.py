#！、usr/bin/env.python
#._*_ coding:utf-8 _*_

from include import Config
from PyQt5.QtCore import QTimer,QTime
from PyQt5.QtGui import QPixmap
import capture,myo_emg
#晕



class capture_guide(object):

    def __init__(self):
        conf = Config.Config().conf
        self.dataset_type = conf["type"]#手势数据集的类别
        self.span = conf["guide_config"]["span"]#一次动作的时间
        self.interval = conf["guide_config"]["interval"]#间隔时间
        self.gesture_type = conf["guide_config"]["gestures"][0]#手势类别，如g12中用1-12表示各个手势
        self.repeat_times = len(conf["guide_config"]["gestures"])#重复手势的次数
        self.capture_timer = QTimer()#capture的计时器
        self.rest_timer = QTimer()#rest的计时器
        self.state = 1 #当前的状态，0表示capture,1表示rest,2表示采集暂停状态，3表示采集结束状态
        self.current_times = 0 #当前的重复次数
        self.RestTime = self.interval/1000
        self.CaptureTime = self.span/1000
        self.spacing = 100


    def start(self,ui = myo_emg.Ui_MainWindow()):#该函数需要与start capture连接起来

        self.rest_timer.start(self.spacing)
        image_path = "D:/MyoSEMG/"+self.dataset_type+"/"+str(self.gesture_type)+".jpg"
        gesture_png = QPixmap(image_path).scaled(ui.gesture_image.geometry().width(),ui.gesture_image.geometry().height())
        ui.gesture_image.setPixmap(gesture_png)
        ui.Timer.setText("{:.1f}".format(self.RestTime))

    def stop(self):#该函数需要与stop capture连接起来
        self.state = 2
        if self.state:
            self.rest_timer.stop()
        else:
            self.capture_timer.stop()

    def rest_event(self,ui = myo_emg.Ui_MainWindow()):

        self.RestTime -= self.spacing/1000
        ui.Timer.setText("{:.1f}".format(self.RestTime))#格式化输出

        if self.RestTime < self.spacing/2000:
            self.rest_timer.stop()
            self.CaptureTime = self.span/1000
            self.capture_timer.start(self.spacing)
            self.state = 0 #进入capture状态
            ui.Timer.setText("{:.1f}".format(self.CaptureTime)) #开始capture阶段

    def capture_event(self,ui = myo_emg.Ui_MainWindow()):
        self.CaptureTime -= self.spacing/1000
        ui.Timer.setText("{:.1f}".format(self.CaptureTime))

        if self.CaptureTime < self.spacing/2000:
            self.capture_timer.stop()
            self.current_times += 1
            if self.current_times < self.repeat_times:
                self.RestTime = self.interval/1000
                self.rest_timer.start(self.spacing)
                self.state = 1#进入休息状态
                ui.Timer.setText("{:.1f}".format(self.RestTime))#再次开始rest阶段
            else:
                self.state = 2#代表采集完全结束











