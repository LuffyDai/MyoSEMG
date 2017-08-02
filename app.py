#！、usr/bin/env.python
#._*_ coding:utf-8 _*_

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow,QVBoxLayout
import myo_emg,logging,MyBar
from PyQt5.QtCore import QFile,QTextStream,Qt
from PyQt5.QtGui import  QFont

def _logger():
    return logging.getLogger('darkstyle')

def load_darkstyle():
    f = QFile("D:\MyoSEMG\darkstyle\style.qss")
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
        super(MainWindow,self).__init__()
        self.layout = QVBoxLayout()
        w = QMainWindow()
        self.ui = myo_emg.Ui_MainWindow()
        self.ui.setupUi(w)
        self.layout.addWidget(MyBar.MyBar(self))
        self.layout.addWidget(w)

        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addStretch(-1)
        self.setMinimumSize(800,600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        self.maxNormal = True



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
