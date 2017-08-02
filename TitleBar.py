#！、usr/bin/env.python
#._*_ coding:utf-8 _*_
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QFile,QTextStream
import myo

class  TitleBar(myo.Ui_MainWindow):
    def __init__(self,parent=None):
        myo.Ui_MainWindow.__init__(self,parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        f = QFile("D:\MyoSEMG\BorderlessWindow.css")
        if not f.exists():
            self.statusBar().showMessage("Unable to load stylesheet, file not found in resources")
        else:
            f.open(QFile.ReadOnly | QFile.Text)
            ts = QTextStream(f)
            stylesheet = ts.readAll()
        self.setStyleSheet(stylesheet)
        title_bar = QtWidgets.QWidget()
        title_bar.pushButtonMinimize =  QtWidgets.QToolButton()
        title_bar.pushButtonMinimize.setIcon(QtGui.QIcon('Icons/Minimize.png'))
        title_bar.pushButtonMaxmize = QtWidgets.QToolButton()
        title_bar.pushButtonMaxmize.setIcon(QtGui.QIcon('Icons/Maxmize.png'))
        title_bar.pushButtonClose = QtWidgets.QToolButton()
        title_bar.pushButtonClose.setIcon(QtGui.QIcon('Icons/Close.png'))
        title_bar.pushButtonMinimize.setMinimumHeight(10)
        title_bar.pushButtonClose.setMinimumHeight(10)
        title_bar.pushButtonMaxmize.setMinimumHeight(10)
        label = QtWidgets.QLabel(self)
        label.setText("MyoSEMG")
        title_bar.setWindowTitle("MyoSEMG")
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(title_bar.pushButtonMinimize)
        hbox.addWidget(title_bar.pushButtonMaxmize)
        hbox.addWidget(title_bar.pushButtonClose)
        hbox.insertStretch(1,500)
        hbox.setSpacing(0)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)
        self.maxNormal = False
        title_bar.pushButtonClose.clicked().connect(self.close)
        title_bar.pushButtonMinimize.clicked.connect(self.showSmall)
        title_bar.pushButtonMaxmize.clicked.connect(self.showMaxRestore)



    def showSmall(self):
        self.showMinimized()

    def showMaxRestore(self):
        if(self.maxNormal):
            self.showNormal()
            self.maxNormal = False
            self.pushButtonMaxmize.setIcon(QtGui.QIcon('Icons/Maxmize.png'))
        else:
            self.showMaximized()
            self.maxNormal = True
            self.pushButtonMaxmize.setIcon(QtGui.QIcon('Icons/Restore.png'))


