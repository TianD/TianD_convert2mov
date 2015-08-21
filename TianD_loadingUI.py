#coding:utf-8
'''
Created on 2015年8月19日 上午9:55:11

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''
import sys
import time
from PyQt4 import QtCore, QtGui
import LOGO_rc
 
class loadingDlg(QtGui.QDialog):
    def __init__(self,parent=None):
        super(loadingDlg, self).__init__(parent)
        self.label = QtGui.QLabel('Red', self)
        self.setFixedSize(95,95)
        self.setWindowFlags(QtCore.Qt.Dialog|QtCore.Qt.CustomizeWindowHint|QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)             #set dialog transparent
        self.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0,0,0,0)
        self.label.setContentsMargins(0,0,0,0)
         
        self.movie = QtGui.QMovie(":circle-progress-bars.gif")
        self.label.setMovie(self.movie)
        self.movie.start()
           
    def __del__(self):
        del self.label
        del self.movie
 
if __name__ == '__main__':
      
    app = QtGui.QApplication(sys.argv)
    mw = loadingDlg()
    mw.show()
    sys.exit(app.exec_())