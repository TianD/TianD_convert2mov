#coding:utf-8
'''
Created on 2015年7月31日 上午11:29:01

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

from PyQt4 import QtGui, QtCore

DEFAULT_STYLE = """
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

COMPLETED_STYLE = """
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
class XProgressBar(QtGui.QProgressBar):
    def __init__(self, parent = None):
        QtGui.QProgressBar.__init__(self, parent)
        self.setStyleSheet(DEFAULT_STYLE)
        self.step = 0
        self.setMaximumHeight(15)

    def setValue(self, value):
        QtGui.QProgressBar.setValue(self, value)
        if value == self.maximum():
            self.setStyleSheet(COMPLETED_STYLE)
        else :
            self.setStyleSheet(DEFAULT_STYLE)

class TableView(QtGui.QTableView):
    def __init__(self, type, parent=None):
        super(TableView, self).__init__(parent)
        self.setAcceptDrops(True)        
        
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