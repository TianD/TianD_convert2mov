#coding:utf-8
'''
Created on 2015年7月30日 下午7:25:38

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

import sys,time

sys.dont_write_bytecode = True

from PyQt4 import QtGui, QtCore

from convert2movUI import Ui_toMOVMainWindow

import TianD_convert2movTableModel
import TianD_convert2movDelegate
import TianD_convert2movWidget

class TianD_convert2movUI(QtGui.QMainWindow, Ui_toMOVMainWindow):

    def __init__(self, parent = None):
        super(TianD_convert2movUI, self).__init__(parent)
        self.setupUi(self)
        
        #show in status bar
        self.progress = TianD_convert2movWidget.XProgressBar()
        self.text = QtGui.QLabel()
        self.statusbar.addWidget(self.progress)
        self.statusbar.addWidget(self.text)
        self.progress.setHidden(1)
        self.text.setHidden(1)
        
        #tableView receive signal from drop event
        self.connect(self.tableView, QtCore.SIGNAL("dropped"), self.setTableView)
                    
        #connect clicked signal to refreshDescription command
        self.tableView.clicked.connect(self.refreshDescription)
                
        #run the commads in sub thread
        self.thread = Worker()
        self.upLoadBtn.clicked.connect(self.slotUploadStart)
        self.toMOVBtn.clicked.connect(self.slotConvertStart)
        
        
    def setTableView(self, l):
        self.list = [#颜色标记, 文件名, 起始帧, 结束帧, [版本列表], 描述
             ['green', 'a', 1001, 1010, ["c003", "c002", "c001"], "hello this is a"], 
             ['green', 'b', 1001, 1020, ["c003", "c002", "c001"], "hello this is b"], 
             ['green', 'c', 1001, 1030, ["c003", "c002", "c001"], ""], 
             ['green', 'e', 1001, 1040, ["c003", "c002", "c001"], ""], 
             ['green', 'f', 1001, 1050, ["c003", "c002", "c001"], ""], 
             [], 
            ['yellow', 'd', 1001, 1011, ["c003", "c002", "c001"], u"我是C"], 
            ['yellow', 'h', 1001, 1012, ["c003", "c002", "c001"], ""], 
            ['yellow', 'k', 1001, 1013, ["c003", "c002", "c001"], ""], 
            [], 
            ['red', 'g', 1001, 1016, ["c003", "c002", "c001"], ""], 
            ['red', 'i', 1001, 1015, ["c003", "c002", "c001"], ""], 
            ['red', 'j', 1001, 1014, ["c003", "c002", "c001"], ""]
            ]
        headers = [u"名称", u"起始帧", u"结束帧", u"版本"]
        
        self.contentModel = TianD_convert2movTableModel.TableModel(self.list, headers)
        self.tableView.setModel(self.contentModel)
        self.tableView.setShowGrid(0)
        self.headerView = self.tableView.horizontalHeader()
        #let first column stretch
        self.headerView.setResizeMode(0, QtGui.QHeaderView.Stretch)
        #select a whole row
        self.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows)

        # add comboBox into table view
        self.tableView.setItemDelegateForColumn(3, TianD_convert2movDelegate.ComboBoxDelegate(self.tableView, self.list))
        
        row = len(self.list)
        for r in range(row):
            if self.list[r]:
                if self.list[r][4]:
                    index = self.contentModel.index(r, 3, QtCore.QModelIndex())
                    self.tableView.openPersistentEditor(index)
        
    def loadDir(self, l):
        for url in l:
            self.dirModel.setRootPath(url)
            self.treeView.setModel(self.dirModel)
            self.treeView.setRootIndex(self.dirModel.index(url))
        
    
    def refreshDescription(self, index):
        row = index.row()
        if self.list[row]:
            descriptionText = self.list[row][-1]
            self.descriptionBrowser.clear()
            self.descriptionBrowser.append(self.headText)
            self.descriptionBrowser.append("<p><big>&nbsp;&nbsp;%s</big></p>" %descriptionText)
    
    def getSelected(self):
        values = []
        index = self.tableView.selectedIndexes()
        if index:
            for i in index:
                row = i.row()
                value = self.contentModel.index(row, 0, QtCore.QModelIndex()).data().toString()
                if value not in values:
                    values.append(value)
            return values
        
        else :
            values = [s[1] for s in self.list if s]
            return values
       
        
    def slotUploadStart(self):
        running = self.thread.isRunning()
        if not running :
            self.thread.btnCmdFlag = 1
            self.thread.progressSignal.connect(self.statusShow)
            self.thread.start(self.getSelected())

    
    def slotConvertStart(self):
        running = self.thread.isRunning()
        if not running :
            self.thread.btnCmdFlag = 0
            self.thread.progressSignal.connect(self.statusShow)
            self.thread.start(self.getSelected())
     
            
    def closeEvent(self, event):
        super(TianD_convert2movUI, self).closeEvent(event)
        self.thread.exit()
        
    
    def statusShow(self, value, text, flag):
        self.progress.setValue(value)
        self.text.setText(text)
        self.progress.setHidden(flag)
        if flag :
            timer = QtCore.QTimer()
            timer.singleShot(1000, self.hideStatus)

        else :
            self.text.setHidden(0)
            
    def hideStatus(self):
        self.text.setHidden(1)
    
class Worker(QtCore.QThread):
    progressSignal = QtCore.pyqtSignal(int, str, int)
    
    def __init__(self, parent = None):
        super(Worker, self).__init__(parent)
        self.working = True
        self.btnCmdFlag = 1

    def __del__(self):
        self.working = False
        self.wait()
    
    def start(self, list):
        super(Worker, self).start()
        self.working = True
        self.list = list
    
    def run(self):
        while self.working :
            for l in self.list:
                for i in range(100):
                    if self.btnCmdFlag :            #if self.btnCmd == 1 :run upload; if self.btnCmd == 0: run convert
                        print "upload footage %d" %(i+1)
                        self.msleep(100)
                    else :
                        print "convert to mov %d" %(i+1)
                        self.msleep(100) 
                    self.progressSignal.emit(i+1, "running: %s" %l, 0)
            self.working = False
            self.progressSignal.emit(100, "finish!!!", 1)

#         import os
#         import os.path
#         paths = 'Z:/Netrender/renderbus/Kaixuanoutput/20150717'
#         path = os.path.normpath(paths)
#         files = os.listdir(path)
#         convertCmd = 'xcopy {0} {1} /e /y'
#         flag = 0
#         for x in files:
#             path1 = path+'\\'+x
#             path2 = 'E:\\temp\\'
#             os.system(convertCmd.format(path1,path2))
#             self.progressSignal.emit((flag+1.0)/len(files)*100)
#             flag +=1
#         self.working = False
            

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui=TianD_convert2movUI()
    ui.show()
    app.exec_()
