#！、usr/bin/env.python
#._*_ coding:utf-8 _*_
import myo,capture_guide,myoData,myo_emg,time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class WorkThread(QThread):
    _signal = pyqtSignal()
    def __init__(self,myos,hub,Data,guide,cap_interval):#cap_interval表示每隔多久采集一次数据，相当于运行一次run里面的循环
        super(WorkThread,self).__init__()
        self.myos = myos
        self.hub = hub
        self.Data = Data
        self.guide = guide
        self.flag = 1
        self.cap_interval = cap_interval
        self._signal.connect(self.stop)


    def run(self):#重写
        while self.myos.connected and self.hub.running:
            if self.flag == 1:
                emg = self.myos.emg
                acceleration = self.myos.acceleration
                gyroscope = self.myos.gyroscope
                orientation = self.myos.orientation
                if self.guide.state >= 0 and self.guide.state < 2:#点击Start Capture才开始保存数据
                    if self.Data.IfCapture_EMG:
                        emgdata = myoData.emgData(time.time(),emg,self.guide.state)
                        self.Data.EMGdata.append(emgdata)
                    if self.Data.IfCapture_IMU:
                        imudata = myoData.imuData(time.time(),acceleration,gyroscope,orientation,self.guide.state)
                        self.Data.IMUdata.append(imudata)
                    time.sleep(self.cap_interval)
                elif self.guide.state == 3 or self.guide.state == 2:
                    self.exec_()
            else:
                exit(0)


    def stop(self):
        self.flag = 0



class capture():

    def __init__(self,spacing = 10000,wait_time = 2.0,cap_interval = 0.001):#默认采集间隔为1ms
        #myo设备的处理
        self.spacing = spacing
        self.wait_time = wait_time
        self.Data = myoData.myo_Data()#数据类型
        self.guide = capture_guide.capture_guide()#用于指示
        self.cap_interval = cap_interval
        self.myos = None
        self.thread = None


    def open_Myo(self,ui = myo_emg.Ui_MainWindow()):
        if not self.myos:
            myo.init()
            self.feed = myo.Feed()
            self.hub = myo.Hub()
            self.hub.run(self.spacing, self.feed)
            self.myos = self.feed.wait_for_single_device(timeout=self.wait_time)
            if not self.myos:
                ui.listWidget.addItem('Myo is not opened...')
            else:
                self.myos.set_stream_emg(myo.StreamEmg.enabled)
                if self.myos.connected:
                    ui.listWidget.addItem('Myo is connected!')
                else:
                    ui.listWidget.addItem('Myo is not connected!')
                self.thread = WorkThread(self.myos,self.hub,self.Data,self.guide,self.cap_interval)
                self.thread.start()#数据的capture在另一线程中执行



    def stop_thread(self):
        if self.thread:
            self.thread._signal.emit()
        else:
            pass


    def save_file(self,guide,ui = myo_emg.Ui_MainWindow()):
        #没有目录创造目录
        if not (guide.state == 2 and guide.state == 3):
            ui.listWidget.addItem('Only save after stop or complete...')
        else:
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
                emg_path = basedir_name+"/data/session-emg-"+date_str+"-"+gesture+".txt"
                emgFile = QFile(emg_path)
                if emgFile.open(QIODevice.WriteOnly | QIODevice.Text):
                    ts = QTextStream(emgFile)
                    for emg in emgData:
                        ts << str(emg.timestamp) << " " << str(emg.emg[0]) << " " << str(emg.emg[1]) << " " \
                        << str(emg.emg[2]) << " " << str(emg.emg[3]) << " " << str(emg.emg[4]) << " " \
                        << str(emg.emg[5]) << " " << str(emg.emg[6]) << " " << str(emg.emg[7]) << " "\
                        <<str(emg.state) << "\n"

                ui.listWidget.addItem('EMGData has been saved...')
                emgFile.close()

            if self.Data.IfCapture_IMU:
                imuData = self.Data.IMUdata
                imu_path = basedir_name + "/data/session-imu-"+date_str+"-"+gesture+".txt"
                imuFile = QFile(imu_path)
                if imuFile.open(QIODevice.WriteOnly | QIODevice.Text):
                    ts = QTextStream(imuFile)
                    for imu in imuData:
                        ts << str(imu.timestamp) << " " \
                        << str(imu.acceleration.x) << " " << str(imu.acceleration.y) << " " << str(imu.acceleration.z) << " " \
                        << str(imu.gyroscope.x) << " " << str(imu.acceleration.y) << " " << str(imu.gyroscope.z) << " "\
                        << str(imu.orientation.x) << " " << str(imu.orientation.y) << " " << str(imu.orientation.z) << " " << str(imu.orientation.w) << " " \
                        << str(imu.state) << "\n"
                ui.listWidget.addItem('IMUdata has been saved...')
                imuFile.close()













