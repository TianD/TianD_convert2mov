#coding:utf-8
'''
Created on 2015年7月30日 下午7:25:38

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

import sys,time
from collections import OrderedDict
from functools import partial

sys.dont_write_bytecode = True

from PyQt4 import QtGui, QtCore

from convert2movUI import Ui_toMOVMainWindow

import TianD_convert2movModel
import TianD_convert2movDelegate
import TianD_convert2movWidget
import TianD_loadingUI


###
# design control style by qss
TEXTBROWSER_STYLE = """
QTextBrowser{
    border: 2px solid grey;
    border-radius: 5px;

}
"""
BUTTON_STYLE = """
QPushButton{
    border: 2px solid grey;
    border-radius: 5px;
}
QPushButton:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #dadbde, stop: 1 #f6f7fa);
}
"""
HEADERVIEW_STYLE = """
QHeaderView::section {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 grey, stop: 0.5 #505050,
                                      stop: 0.6 #434343, stop:1 grey);
    color: white;
    padding-left: 4px;
    border: 1px solid grey;
}
"""
###

class TianD_convert2movUI(QtGui.QMainWindow, Ui_toMOVMainWindow):

    def __init__(self, parent = None):
        super(TianD_convert2movUI, self).__init__(parent)
        self.setupUi(self)
        
        # set window background color
        self.setStyleSheet("background: #F0F0F0;")
        # set widget styleSheet
        self.descriptionBrowser.setStyleSheet(TEXTBROWSER_STYLE)
        self.reorderBtn.setStyleSheet(BUTTON_STYLE)
        self.runBtn.setStyleSheet(BUTTON_STYLE)
        
        # run the commads in sub thread
        self.thread = Worker()
        
        # show progress and text in status bar
        self.progress = TianD_convert2movWidget.XProgressBar()
        self.text = QtGui.QLabel()
        self.statusbar.addWidget(self.progress)
        self.statusbar.addWidget(self.text)
        self.progress.setHidden(1)
        self.text.setHidden(1)
                
        # treeView receive signal from drop event
        self.connect(self.treeView, QtCore.SIGNAL("dropped"), self.loading)
        
        # connect clicked signal to refreshDescription command
        self.treeView.clicked.connect(self.refreshDescription)
                
        # connect clicked signal to slotRunStart command
        self.runBtn.clicked.connect(self.slotRunStart)
        
        # connect choice label clicked signal to check command
#         self.allLabel.clicked.connect(self.checkAll)
#         self.noneLabel.clicked.connect(self.checkNone)
#         self.greenLabel.clicked.connect(self.checkGreen)
#         self.yellowLabel.clicked.connect(self.checkYellow)
#         self.redLabel.clicked.connect(self.checkRed)
        self.allLabel.clicked.connect(partial(self.checkByColor, "All"))
        self.noneLabel.clicked.connect(partial(self.checkByColor, "None"))
        self.greenLabel.clicked.connect(partial(self.checkByColor, "Green"))
        self.yellowLabel.clicked.connect(partial(self.checkByColor, "Yellow"))
        self.redLabel.clicked.connect(partial(self.checkByColor, "Red"))
        
        # set radioButton default value and connect checked signal to display command
        self.toMovRadioBtn.setChecked(1)
        self.buttongroup.buttonClicked.connect(self.displayTreeView)
        
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
    
    def displayTreeView(self, index):
        
        print index
        
    def setTreeView(self, d):        
        
        rootNode = TianD_convert2movModel.Node("Root")
        
        self.analyzePath(d, rootNode)
        headers = [u"素材名", u"输出名", u"起始帧", u"结束帧", u"输出路径", u"版本", u"修改日期", u"是否已经上传", u"选择"]
        
        
        self.contentModel = TianD_convert2movModel.TreeModel(rootNode, self.orderedDic, headers)
        self.treeView.setModel(self.contentModel)
        self.headerView = self.treeView.header()
        self.headerView.setStyleSheet(HEADERVIEW_STYLE)
    
        # add comboBox into table view
        delegate = TianD_convert2movDelegate.ComboBoxDelegate(self.treeView, rootNode)
        self.treeView.setItemDelegateForColumn(5, delegate)
        delegate.indexSignal.connect(self.contentModel.setBroData)
        
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
    
    def slotRunStart(self):
        mode = self.buttongroup.checkedId()
        running = self.thread.isRunning()
        print self.getChecked()
        if not running :
            if mode == -2:
                self.thread.btnCmdFlag = 0
            elif mode == -3:
                self.thread.btnCmdFlag = 1
            else :
                print "nothing is selected"
                return False
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

    def checkByColor(self, color = "Green"):
        #根据颜色背景勾选不同的item
        for index in self.contentModel.persistentIndexList():
            row = index.row()
            node = index.internalPointer()
            if not node.childCount():
                parent = index.parent()
                index = self.contentModel.index(row, 8, parent)
                if color == "All":
                    self.contentModel.setData(index, value = QtCore.Qt.Checked, role = QtCore.Qt.CheckStateRole)
                elif color == "Green":
                    if self.orderedDic[node.parent().parent().value()][node.parent().value()][row][-1] == "success":
                        self.contentModel.setData(index, value = QtCore.Qt.Checked, role = QtCore.Qt.CheckStateRole)
                    else :
                        self.contentModel.setData(index, value = QtCore.Qt.Unchecked, role = QtCore.Qt.CheckStateRole)
                elif color == "Yellow":
                    if self.orderedDic[node.parent().parent().value()][node.parent().value()][row][-1] == "warning":
                        self.contentModel.setData(index, value = QtCore.Qt.Checked, role = QtCore.Qt.CheckStateRole)
                    else :
                        self.contentModel.setData(index, value = QtCore.Qt.Unchecked, role = QtCore.Qt.CheckStateRole)
                elif color == "Red":
                    if self.orderedDic[node.parent().parent().value()][node.parent().value()][row][-1] == "error":
                        self.contentModel.setData(index, value = QtCore.Qt.Checked, role = QtCore.Qt.CheckStateRole)
                    else :
                        self.contentModel.setData(index, value = QtCore.Qt.Unchecked, role = QtCore.Qt.CheckStateRole)
                else:
                    self.contentModel.setData(index, value = QtCore.Qt.Unchecked, role = QtCore.Qt.CheckStateRole)
        
    def getChecked(self):
        #获取界面上所选择的项目,返回一个字典
        #现在那个版本号返回的还是个列表,还没有修改
        selected = dict()
        for index in self.contentModel.persistentIndexList():
            row = index.row()
            column = index.column()
            node = index.internalPointer()
            if not node.childCount():
                if node.value()[-2] == 2:
                    parent = index.parent()
                    parentNode = parent.internalPointer()
                    topparent = parent.parent()
                    topparentNode = topparent.internalPointer()
                    selected.setdefault(topparentNode.value(), dict()).setdefault(parentNode.value(), list())
                    if node.value() not in selected[topparentNode.value()][parentNode.value()]: 
                        selected[topparentNode.value()][parentNode.value()].append(node.value())
        return selected

#     def checkAll(self):
#         #勾选全部
#         print "allLabel is clicked"
#         for index in self.contentModel.persistentIndexList():
#             row = index.row()
#             node = index.internalPointer()
#             if not node.childCount():
#                 parent = index.parent()
#                 index = self.contentModel.index(row, 8, parent)
#                 self.contentModel.setData(index, value = QtCore.Qt.Checked, role = QtCore.Qt.CheckStateRole)
#                 
#     def checkNone(self):
#         #取消勾选
#         print "noneLabel is clicked"
#         for index in self.contentModel.persistentIndexList():
#             row = index.row()
#             node = index.internalPointer()
#             if not node.childCount():
#                 parent = index.parent()
#                 index = self.contentModel.index(row, 8, parent)
#                 self.contentModel.setData(index, value = QtCore.Qt.Unchecked, role = QtCore.Qt.CheckStateRole)
#        
#     def checkGreen(self):
#         #勾选绿色背景
#         print "greenLabel is clicked"
#         for index in self.contentModel.persistentIndexList():
#             row = index.row()
#             node = index.internalPointer()
#             if not node.childCount():
#                 parent = index.parent()
#                 index = self.contentModel.index(row, 8, parent)
#                 if self.orderedDic[node.parent().parent().value()][node.parent().value()][row][-1] == "success":
#                     self.contentModel.setData(index, value = QtCore.Qt.Checked, role = QtCore.Qt.CheckStateRole)
#                 else :
#                     self.contentModel.setData(index, value = QtCore.Qt.Unchecked, role = QtCore.Qt.CheckStateRole)
#         
#     def checkYellow(self):
#         #勾选黄色背景
#         print "yellowLabel is clicked"
#         for index in self.contentModel.persistentIndexList():
#             row = index.row()
#             node = index.internalPointer()           
#             if not node.childCount():
#                 parent = index.parent()
#                 index = self.contentModel.index(row, 8, parent)
#                 if self.orderedDic[node.parent().parent().value()][node.parent().value()][row][-1] == "warning":
#                     self.contentModel.setData(index, value = QtCore.Qt.Checked, role = QtCore.Qt.CheckStateRole)
#                 else :
#                     self.contentModel.setData(index, value = QtCore.Qt.Unchecked, role = QtCore.Qt.CheckStateRole)  
#                          
#     def checkRed(self):
#         #勾选红色背景
#         print "redLabel is clicked"
#         for index in self.contentModel.persistentIndexList():
#             row = index.row()
#             node = index.internalPointer()
#             if not node.childCount():
#                 parent = index.parent()
#                 index = self.contentModel.index(row, 8, parent)                
#                 if self.orderedDic[node.parent().parent().value()][node.parent().value()][row][-1] == "error":
#                     self.contentModel.setData(index, value = QtCore.Qt.Checked, role = QtCore.Qt.CheckStateRole)
#                 else :
#                     self.contentModel.setData(index, value = QtCore.Qt.Unchecked, role = QtCore.Qt.CheckStateRole)
        

# 该进程用于输出
class Worker(QtCore.QThread):
    progressSignal = QtCore.pyqtSignal(int, str, int)
    
    def __init__(self, parent = None):
        super(Worker, self).__init__(parent)
        self.working = True
        self.btnCmdFlag = 1

    def __del__(self):
        self.working = False
        self.wait()
    
    def start(self, dic):
        super(Worker, self).start()
        self.working = True
        self.dic = dic
    
    def run(self):
        while self.working :
            for l in self.dic:
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
 
# 该进程接收提供的数据, 
class loadWorker(QtCore.QThread):
    flagSignal = QtCore.pyqtSignal(int)
    dictSignal = QtCore.pyqtSignal(dict)
    def __init__(self, parent = None):
        super(loadWorker, self).__init__(parent)
    
    def __del__(self):
        self.wait()
    
    def start(self, d):
        super(loadWorker, self).start()
        self.source = {#{镜头号: {分层:      [上传名称,  起始帧,             结束帧,           输出路径,  [版本列表],             上传时间,     服务器上是否有, 选择标记, 描述,                     正确性标记, 素材路径]}}
                        'sc01':{   \
                                "bg_color": [["xxxxx1", [1001,1002,1003], [1010,1011,1012], "z:\\aaa", ["c001","c002","c003"], "2015/8/18", 0,              0,      u"这是 sc01 bg_color1",    "success"], \
                                             ["xxxxx2", [1002,1003],      [1020,1021],      "z:\\ddd", ["c001","c002"],        "2015/8/18", 0,              0,      "this is sc01 bg_color2", "warning"]], \
                                "occ":      [["xxxxx3", [1003,1004],      [1030,1031],      "z:\\aaa", ["c001","c002"],        "2015/8/18", 0,              0,      "this is sc01 occ",       "success"],]  \
                                }, 
                        'sc02':{"bg_color": [["xxxxx4", [1004,1005,1006], [1040,1041,1042], "z:\\aaa", ["c001","c002","c003"], "2015/8/18", 1,              0,      "this is sc02 bg_color",  "error"]]},
                        'sc03':{"bg_color": [["xxxxx5", [1005,1006,1007], [1050,1051,1052], "z:\\bbb", ["c001","c002","c003"], "2015/8/18", 0,              0,      "this is sc03 bg_color",  "error"]]},
                        'sc04':{"bg_color": [["xxxxx6", [1006,1007,1008], [1060,1061,1062], "z:\\aaa", ["c001","c002","c003"], "2015/8/18", 1,              0,      "this is sc04 bg_color",  "error"]]},
                        'sc05':{"bg_color": [["xxxxx7", [1007],           [1070],           "z:\\ccc", ["c001"],               "2015/8/18", 0,              0,      "this is sc05 bg_color",  "success"]]},
                        'sc06':{"bg_color": [["xxxxx8", [1008,1009],      [1080,1081],      "z:\\aaa", ["c001","c002"],        "2015/8/18", 0,              0,      "this is sc06 bg_color",  "warning"]]}
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
