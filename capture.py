#！、usr/bin/env.python
#._*_ coding:utf-8 _*_
import myo,capture_guide,myoData,myo_emg,time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class WorkThread(QThread):
    _signal = pyqtSignal()
    def __init__(self,myos,hub,Data,guide):
        super(WorkThread,self).__init__()
        self.myos = myos
        self.hub = hub
        self.Data = Data
        self.guide = guide
        self.flag = 1
        self._signal.connect(self.stop)

    def run(self):#重写
        while self.myos.connected and self.hub.running:
            if self.flag == 1:
                emg = self.myos.emg
                acceleration = self.myos.acceleration
                gyroscope = self.myos.gyroscope
                orientation = self.myos.orientation
                if self.guide.state >= 0 and self.guide.state < 3:#点击Start Capture才开始保存数据
                    if self.Data.IfCapture_EMG:
                        emgdata = myoData.emgData(time.time(),emg,self.guide.state)
                        self.Data.EMGdata.append(emgdata)
                    if self.Data.IfCapture_IMU:
                        imudata = myoData.imuData(time.time(),acceleration,gyroscope,orientation,self.guide.state)
                        self.Data.IMUdata.append(imudata)
                elif self.guide.state == 3:
                    self.exec_()
            else:
                exit(0)


    def stop(self):
        self.flag = 0



class capture():
    #complete_signal = pyqtSignal()

    def __init__(self,spacing = 1000,wait_time = 2.0):
        #myo设备的处理
        self.spacing = spacing
        self.wait_time = wait_time
        self.Data = myoData.myo_Data()#数据类型
        self.guide = capture_guide.capture_guide()#用于指示
        self.myos = None
        self.thread = None
        #self.complete_signal.connect(self.save_file)


    def open_Myo(self,ui = myo_emg.Ui_MainWindow()):
        if not self.myos:
            myo.init()
            self.feed = myo.Feed()
            self.hub = myo.Hub()
            self.hub.run(self.spacing, self.feed)
            self.myos = self.feed.wait_for_single_device(timeout=self.wait_time)
            self.myos.set_stream_emg(myo.StreamEmg.enabled)
            if self.myos.connected:
                ui.listWidget.addItem('Myo is connected!')
            else:
                ui.listWidget.addItem('Myo is not connected!')
            self.thread = WorkThread(self.myos,self.hub,self.Data,self.guide)
            self.thread.start()#数据的capture在另一线程中执行


    def stop_thread(self):
        if self.thread:
            self.thread._signal.emit()
        else:
            pass


    def save_file(self):
        #没有目录创造目录
        date_str = QDateTime.currentDateTime().toString("yyyy-MM-dd-hh-mm-ss")
        rootdir_name = "appdata"
        rootdir = QDir(rootdir_name)
        basedir_name = rootdir_name + "/" + self.guide.dataset_type
        basedir = QDir(basedir_name)
        gesture = str(self.guide.gesture_type)
        if not basedir.exists():
            rootdir.mkdir(self.guide.dataset_type)
        outdir = QDir(basedir_name + "/data")
        if not outdir.exists():
            basedir.mkdir("data")

        if self.Data.IfCapture_EMG:
            emgData = self.Data.EMGdata
            emg_path = basedir_name+"/data/"+"session-emg-"+date_str+"-"+gesture+".txt"
            emgFile = QFile(emg_path)
            if emgFile.open(QIODevice.WriteOnly | QIODevice.Text):
                ts = QTextStream(emgFile)
                for emg in emgData:
                    ts << str(emg.timestamp) << " " << str(emg.emg[0]) << " " << str(emg.state) << "\n"
            emgFile.close()












