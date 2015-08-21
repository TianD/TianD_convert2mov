#coding:utf-8
'''
Created on 2015年7月30日 下午7:25:38

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

import sys,time
from collections import OrderedDict

sys.dont_write_bytecode = True

from PyQt4 import QtGui, QtCore

from convert2movUI import Ui_toMOVMainWindow

import TianD_convert2movModel
import TianD_convert2movDelegate
import TianD_convert2movWidget
import TianD_loadingUI

class TianD_convert2movUI(QtGui.QMainWindow, Ui_toMOVMainWindow):

    def __init__(self, parent = None):
        super(TianD_convert2movUI, self).__init__(parent)
        self.setupUi(self)
        
        #set window background color
        #self.setStyleSheet("background: #282825;")
        
        #show in status bar
        self.progress = TianD_convert2movWidget.XProgressBar()
        self.text = QtGui.QLabel()
        self.statusbar.addWidget(self.progress)
        self.statusbar.addWidget(self.text)
        self.progress.setHidden(1)
        self.text.setHidden(1)
                
        #tableView receive signal from drop event
        self.connect(self.treeView, QtCore.SIGNAL("dropped"), self.loading)
                    
        #connect clicked signal to refreshDescription command
        self.treeView.clicked.connect(self.refreshDescription)
                
        #run the commads in sub thread
        self.thread = Worker()
        self.upLoadBtn.clicked.connect(self.slotUploadStart)
        self.toMOVBtn.clicked.connect(self.slotConvertStart)
        
        #connect choice label clicked signal to check command
        self.allLabel.clicked.connect(self.checkAll)
        self.noneLabel.clicked.connect(self.checkNone)
        self.greenLabel.clicked.connect(self.checkGreen)
        self.yellowLabel.clicked.connect(self.checkYellow)
        self.redLabel.clicked.connect(self.checkRed)
        
    def loading(self, l):
        self.loadingUI =  TianD_loadingUI.loadingDlg(self)
        self.loadingUI.show()
        self.gth = loadWorker()
        self.gth.start(l)
        self.gth.flagSignal.connect(self.exitLoading)
            
    def exitLoading(self, f):
        if f:
            self.loadingUI.deleteLater()
            source = self.gth.source
            self.gth.exit()
            self.setTreeView(source)
            
    def setTreeView(self, d):        
        
        rootNode = TianD_convert2movModel.Node("Root")
        
        self.analyzePath(d, rootNode)
        headers = [u"镜头分层", u"文件名", u"起始帧", u"结束帧", u"路径", u"版本", u"修改日期", u"是否已经上传", u"选择"]
        
        
        self.contentModel = TianD_convert2movModel.TreeModel(rootNode, self.orderedDic, headers)
        self.treeView.setModel(self.contentModel)
    
        # add comboBox into table view
        self.treeView.setItemDelegateForColumn(5, TianD_convert2movDelegate.ComboBoxDelegate(self.treeView, rootNode))
        
        for r in range(rootNode.childCount()):
            topNode = rootNode.child(r)
            topindex = self.contentModel.index(r, 5, QtCore.QModelIndex())
            for i in range(topNode.childCount()):
                midNode = topNode.child(i)
                midindex = self.contentModel.index(i, 5, topindex)
                for h in range(midNode.childCount()):
                    index = self.contentModel.index(h, 5, midindex)
                    self.treeView.openPersistentEditor(index)
                    
                    
        #treeview expand all children
        self.treeView.expandAll()
        
        #resize column width of treeview
        self.treeView.setColumnWidth(0, 120)
        self.treeView.setColumnWidth(1, 150)
        self.treeView.setColumnWidth(4, 200)
        self.treeView.setColumnWidth(8, 40)
        
    def analyzePath(self, d, root):
        source = d
        
        self.orderedDic = OrderedDict(sorted(source.items(), key = lambda t: t[0]))
        for key, value in self.orderedDic.items():
            topnode = TianD_convert2movModel.Node(key, root)
            for ck, cv in self.orderedDic[key].items():
                midnode = TianD_convert2movModel.Node(ck, topnode)
                for v in cv:
                  tipnode = TianD_convert2movModel.Node(v[:-1], midnode)


    def refreshDescription(self, index):
        node = index.internalPointer()
        row = index.row()
        if not node.childCount():
            parentKey = node.parent().parent().value()
            key = node.parent().value()
            descriptionText = self.orderedDic[parentKey][key][row][-2]
            self.descriptionBrowser.clear()
            self.descriptionBrowser.append(self.headText)
            self.descriptionBrowser.append("<p><big>&nbsp;&nbsp;%s</big></p>" %descriptionText)       
        
    def slotUploadStart(self):
        running = self.thread.isRunning()
        if not running :
            self.thread.btnCmdFlag = 1
            self.thread.progressSignal.connect(self.statusShow)
            self.thread.start(self.getChecked())

    
    def slotConvertStart(self):
        running = self.thread.isRunning()
        if not running :
            self.thread.btnCmdFlag = 0
            self.thread.progressSignal.connect(self.statusShow)
            self.thread.start(self.getChecked())
     
            
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

    
    def checkAll(self):
        print "allLabel is clicked"
        for index in self.contentModel.persistentIndexList():
            row = index.row()
            node = index.internalPointer()
            if not node.childCount():
                parent = index.parent()
                index = self.contentModel.index(row, 8, parent)
                self.contentModel.setData(index, value = QtCore.Qt.Checked, role = QtCore.Qt.CheckStateRole)
                
    def checkNone(self):
        print "noneLabel is clicked"
        for index in self.contentModel.persistentIndexList():
            row = index.row()
            node = index.internalPointer()
            if not node.childCount():
                parent = index.parent()
                index = self.contentModel.index(row, 8, parent)
                self.contentModel.setData(index, value = QtCore.Qt.Unchecked, role = QtCore.Qt.CheckStateRole)
        
    def checkGreen(self):
        print "greenLabel is clicked"
        for index in self.contentModel.persistentIndexList():
            row = index.row()
            node = index.internalPointer()
            if not node.childCount():
                parent = index.parent()
                index = self.contentModel.index(row, 8, parent)
                if self.orderedDic[node.parent().parent().value()][node.parent().value()][row][-1] == "success":
                    self.contentModel.setData(index, value = QtCore.Qt.Checked, role = QtCore.Qt.CheckStateRole)
                else :
                    self.contentModel.setData(index, value = QtCore.Qt.Unchecked, role = QtCore.Qt.CheckStateRole)
        
    def checkYellow(self):
        print "yellowLabel is clicked"
        for index in self.contentModel.persistentIndexList():
            row = index.row()
            node = index.internalPointer()           
            if not node.childCount():
                parent = index.parent()
                index = self.contentModel.index(row, 8, parent)
                if self.orderedDic[node.parent().parent().value()][node.parent().value()][row][-1] == "warning":
                    self.contentModel.setData(index, value = QtCore.Qt.Checked, role = QtCore.Qt.CheckStateRole)
                else :
                    self.contentModel.setData(index, value = QtCore.Qt.Unchecked, role = QtCore.Qt.CheckStateRole)  
                         
    def checkRed(self):
        print "redLabel is clicked"
        for index in self.contentModel.persistentIndexList():
            row = index.row()
            node = index.internalPointer()
            if not node.childCount():
                parent = index.parent()
                index = self.contentModel.index(row, 8, parent)                
                if self.orderedDic[node.parent().parent().value()][node.parent().value()][row][-1] == "error":
                    self.contentModel.setData(index, value = QtCore.Qt.Checked, role = QtCore.Qt.CheckStateRole)
                else :
                    self.contentModel.setData(index, value = QtCore.Qt.Unchecked, role = QtCore.Qt.CheckStateRole)
                    
    def getChecked(self):
        selected = []
        for index in self.contentModel.persistentIndexList():
            row = index.row()
            node = index.internalPointer()
            if not node.childCount():
                if node.value()[-2] == 2:
                    path = node.value()[3] + '\\' + node.value()[0]
                    path in selected or selected.append(path)
        return selected
            
                        
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
 
class loadWorker(QtCore.QThread):
    flagSignal = QtCore.pyqtSignal(int)
    dictSignal = QtCore.pyqtSignal(dict)
    def __init__(self, parent = None):
        super(loadWorker, self).__init__(parent)
    
    def __del__(self):
        self.wait()
    
    def start(self, d):
        super(loadWorker, self).start()
        self.source = {#{镜头号: {分层: [上传名称, 起始帧, 结束帧, 路径, [版本列表], 上传时间, 服务器上是否有, 描述]}}
                        'sc01':{   \
                                "bg_color": [["xxxxx1", 1001, 1010, "z:\\aaa", ["c001","c002","c003"], "2015/8/18", 0, 0, "this is sc01 bg_color1", "success"], \
                                             ["xxxxx2", 1001, 1010, "z:\\ddd", ["c001","c002"], "2015/8/18", 0, 0, "this is sc01 bg_color2", "warning"]], \
                                "occ": [["xxxxx3", 1001, 1010, "z:\\aaa", ["c001","c002"], "2015/8/18", 0, 0, "this is sc01 occ", "success"],]  \
                                }, 
                        'sc02':{"bg_color": [["xxxxx4", 1001, 1011, "z:\\aaa", ["c001","c002","c003"], "2015/8/18", 1, 0, "this is sc02 bg_color", "error"]]},
                        'sc03':{"bg_color": [["xxxxx5", 1001, 1012, "z:\\bbb", ["c001","c002","c003"], "2015/8/18", 0, 0, "this is sc03 bg_color", "error"]]},
                        'sc04':{"bg_color": [["xxxxx6", 1001, 1013, "z:\\aaa", ["c001","c002","c003"], "2015/8/18", 1, 0, "this is sc04 bg_color", "error"]]},
                        'sc05':{"bg_color": [["xxxxx7", 1001, 1011, "z:\\ccc", ["c001"], "2015/8/18", 0, 0, "this is sc05 bg_color", "success"]]},
                        'sc06':{"bg_color": [["xxxxx8", 1001, 1016, "z:\\aaa", ["c001","c002"], "2015/8/18", 0, 0, "this is sc06 bg_color", "warning"]]}
                        }
        
    def run(self):
        self.sleep(1)
        self.flagSignal.emit(1)
        self.dictSignal.emit(self.source)
        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui=TianD_convert2movUI()
    ui.show()
    app.exec_()
