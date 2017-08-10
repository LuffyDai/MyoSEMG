#！、usr/bin/env.python
#._*_ coding:utf-8 _*_
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time,warnings

X_misc = 100 #300ms一帧
Y_max = 100 #暂定最大电压为100
Y_min = -100 #最小电压为-100
MAXCOUNTER = int(X_misc)

class PlotThread(QThread):
    stop_signal = pyqtSignal()
    def __init__(self,Canvas):
        super(PlotThread,self).__init__()
        self.Canvas = Canvas
        self._exit = False
        self.emg_queue = []
        self.emg2_queue = []
        self.emg3_queue = []
        self.emg4_queue = []
        self.time_queue = []
        self.stop_signal.connect(self.stop_thread)

    def run(self):
        counter = 0
        while(True):
            if self._exit:
                exit(0)
            else:
                self.emg_queue.append(self.Canvas.emg_data)
                self.emg2_queue.append(self.Canvas.emg_data2)
                self.emg3_queue.append(self.Canvas.emg_data3)
                self.emg4_queue.append(self.Canvas.emg_data4)

                self.time_queue.append(self.Canvas.time_data)

                self.Canvas.ax = self.Canvas.fig.add_subplot(141)
                self.Canvas.ax.set_ylim(Y_min,Y_max)
                self.Canvas.ax.set_xlim(self.time_queue[0],self.time_queue[-1])
                self.Canvas.ax.plot(self.time_queue,self.emg_queue,'b')
                self.Canvas.ax.axis('off')

                self.Canvas.bx = self.Canvas.fig.add_subplot(142)
                self.Canvas.bx.set_ylim(Y_min, Y_max)
                self.Canvas.bx.set_xlim(self.time_queue[0], self.time_queue[-1])
                self.Canvas.bx.plot(self.time_queue, self.emg2_queue, 'b')
                self.Canvas.bx.axis('off')

                self.Canvas.cx = self.Canvas.fig.add_subplot(143)
                self.Canvas.cx.set_ylim(Y_min, Y_max)
                self.Canvas.cx.set_xlim(self.time_queue[0], self.time_queue[-1])
                self.Canvas.cx.plot(self.time_queue, self.emg3_queue, 'b')
                self.Canvas.cx.axis('off')

                self.Canvas.dx = self.Canvas.fig.add_subplot(144)
                self.Canvas.dx.set_ylim(Y_min, Y_max)
                self.Canvas.dx.set_xlim(self.time_queue[0], self.time_queue[-1])
                self.Canvas.dx.plot(self.time_queue, self.emg4_queue, 'b')
                self.Canvas.dx.axis('off')

                self.Canvas.draw()

                if counter >= MAXCOUNTER:
                    self.time_queue.pop(0)
                    self.emg_queue.pop(0)
                    self.emg2_queue.pop(0)
                    self.emg3_queue.pop(0)
                    self.emg4_queue.pop(0)

                else:
                    counter += 1
            time.sleep(0.001)

    def stop_thread(self):
        self._exit = True



class Canvas(FigureCanvas):

    def __init__(self):
        self.fig = Figure(facecolor=(0, 0, 0))
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.time_data = 0
        self.emg_data = 0
        self.emg_data2 = 0
        self.emg_data3 = 0
        self.emg_data4 = 0
        self.thread = None

    def start(self):

        warnings.filterwarnings('ignore')
        self.thread = PlotThread(self)
        self.thread.start()


    def stop_plot(self):
        if self.thread:
            self.thread.plot_signal.emit()
        else:
            pass

class Canvas2(FigureCanvas):
    def __init__(self):
        self.fig = Figure(facecolor=(0,0,0))
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.time_data = 0
        self.emg_data = 0
        self.emg_data2 = 0
        self.emg_data3 = 0
        self.emg_data4 = 0
        self.thread = None

    def start(self):

        warnings.filterwarnings('ignore')
        self.thread = PlotThread(self)
        self.thread.start()
























