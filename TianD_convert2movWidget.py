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

class TreeView(QtGui.QTreeView):
    def __init__(self, type, parent=None):
        super(TreeView, self).__init__(parent)
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
            
class HeaderView(QtGui.QHeaderView):

    def __init__(self, parent=None):
        super(HeaderView, self).__init__(QtCore.Qt.Horizontal, parent)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.ctxMenu)

        self.setup()

    @pyqtSlot(bool)
    def printID(self, i):
        print("id")
        if i == False:
            self.hideSection(0)
        else:
            self.showSection(0)

    @pyqtSlot(bool)        
    def printNAME(self, i):
        print("name")
        if i == False:
            self.hideSection(1)
        else:
            self.showSection(1)

    @pyqtSlot(bool)        
    def printUSERNAME(self, i):
        print("username")
        if i == False:
            self.hideSection(2)
        else:
            self.showSection(2)

    def setup(self):

        self.id = QAction("id",self)
        self.id.setCheckable(True)
        self.id.setChecked(True)
        self.connect(self.id, SIGNAL("triggered(bool)"), self, SLOT("printID(bool)"))


        self.name = QAction("name",self)
        self.name.setCheckable(True)
        self.name.setChecked(True)
        self.connect(self.name, SIGNAL("triggered(bool)"), self, SLOT("printNAME(bool)"))


        self.username = QAction("username",self)
        self.username.setCheckable(True)
        self.username.setChecked(True)
        self.connect(self.username, SIGNAL("triggered(bool)"), self, SLOT("printUSERNAME(bool)"))

    def ctxMenu(self, point):
        menu = QMenu(self)
        self.currentSection = self.logicalIndexAt(point)
        menu.addAction(self.id)
        menu.addAction(self.name)
        menu.addAction(self.username)
        menu.exec_(self.mapToGlobal(point))