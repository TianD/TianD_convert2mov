#coding:utf-8
'''
Created on 2015年7月31日 上午11:29:01

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''
import random
from PyQt4 import QtGui, QtCore

XPROGRESS_DEFAULT_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}
QProgressBar::chunk {
    background-color: lightblue;
    width: 2px;
    margin: 1px;
}
"""

XPROGRESS_COMPLETED_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}
QProgressBar::chunk {
    background-color: #CD96CD;
    width: 2px;
    margin: 1px;
}
"""

TREEVIEW_STYLE = """
QTreeView{
    border: 2px solid grey;
    border-radius: 5px;    
}
"""

class XProgressBar(QtGui.QProgressBar):
    def __init__(self, parent = None):
        QtGui.QProgressBar.__init__(self, parent)
        self.setStyleSheet(XPROGRESS_DEFAULT_STYLE)
        self.step = 0
        self.setMaximumHeight(15)

    def setValue(self, value):
        QtGui.QProgressBar.setValue(self, value)
        if value == self.maximum():
            self.setStyleSheet(XPROGRESS_COMPLETED_STYLE)
        else :
            self.setStyleSheet(XPROGRESS_DEFAULT_STYLE)

class TreeView(QtGui.QTreeView):
    def __init__(self, type, parent=None):
        super(TreeView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet(TREEVIEW_STYLE)   
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()  

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(QtCore.QString(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            event.ignore()

class Label(QtGui.QLabel):
    clicked = QtCore.pyqtSignal()
    def __init__(self, parent = None, flag = QtCore.Qt.Widget):
        super(Label, self).__init__(parent, flag)
        self.setMouseTracking(True)
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            print "%s" %self.text()
            self.clicked.emit()
            event.accept()
        else :
            event.ignore()
            
    def mouseMoveEvent(self, event):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground, QtGui.QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255), 255))
        self.setPalette(palette)
        