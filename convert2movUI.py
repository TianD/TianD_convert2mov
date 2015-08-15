# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Scripts\Eclipse\TianD_convert2mov\source\convert2movUI.ui'
#
# Created: Fri Jul 31 10:06:16 2015
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui


import TianD_convert2movWidget
import LOGO_rc

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s): 
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_toMOVMainWindow(object):
    
    
    
    def setupUi(self, toMOVMainWindow):
        toMOVMainWindow.setObjectName(_fromUtf8("toMOVMainWindow"))
        toMOVMainWindow.resize(1300, 632)
        self.setWindowIcon(QtGui.QIcon(":LOGO.png"))
        self.centralwidget = QtGui.QWidget(toMOVMainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget_2 = QtGui.QWidget(self.centralwidget)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.treeView = TianD_convert2movWidget.TreeView(self.centralwidget)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.verticalLayout_2.addWidget(self.treeView)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.spacerItem = QtGui.QSpacerItem(600, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(self.spacerItem)
        self.choiceLabel = QtGui.QLabel(self.widget_2)
        self.choiceLabel.setObjectName(_fromUtf8("choiceLabel"))
        self.horizontalLayout_2.addWidget(self.choiceLabel)
        self.allLabel = TianD_convert2movWidget.Label(self.widget_2)
        self.allLabel.setObjectName(_fromUtf8("allLabel"))
        self.horizontalLayout_2.addWidget(self.allLabel)
        self.noneLabel = TianD_convert2movWidget.Label(self.widget_2)
        self.noneLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.noneLabel.setObjectName(_fromUtf8("noneLabel"))
        self.horizontalLayout_2.addWidget(self.noneLabel)
        self.greenLabel = TianD_convert2movWidget.Label(self.widget_2)
        self.greenLabel.setObjectName(_fromUtf8("greenLabel"))
        self.horizontalLayout_2.addWidget(self.greenLabel)
        self.yellowLabel = TianD_convert2movWidget.Label(self.widget_2)
        self.yellowLabel.setObjectName(_fromUtf8("yellowLabel"))
        self.horizontalLayout_2.addWidget(self.yellowLabel)
        self.redLabel = TianD_convert2movWidget.Label(self.widget_2)
        self.redLabel.setObjectName(_fromUtf8("redLabel"))
        self.horizontalLayout_2.addWidget(self.redLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addWidget(self.widget_2)
        self.rightWidget = QtGui.QWidget(self.centralwidget)
        self.rightWidget.setObjectName(_fromUtf8("rightWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.rightWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.descriptionBrowser = QtGui.QTextBrowser(self.rightWidget)
        self.descriptionBrowser.setObjectName(_fromUtf8("descriptionBrowser"))
        self.verticalLayout.addWidget(self.descriptionBrowser)
        self.toMOVBtn = QtGui.QPushButton(self.rightWidget)
        self.toMOVBtn.setObjectName(_fromUtf8("toMOVBtn"))
        self.verticalLayout.addWidget(self.toMOVBtn)
        self.upLoadBtn = QtGui.QPushButton(self.rightWidget)
        self.upLoadBtn.setObjectName(_fromUtf8("upLoadBtn"))
        self.verticalLayout.addWidget(self.upLoadBtn)
        #
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.addWidget(self.widget_2)
        self.splitter.addWidget(self.rightWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalLayout.addWidget(self.splitter)
        self.splitter.setStretchFactor(0, 1)
        #
        self.headText = "<b><big>Description:</big></b>"
        self.descriptionBrowser.append(self.headText)
        #
        toMOVMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(toMOVMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1064, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        toMOVMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(toMOVMainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        toMOVMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(toMOVMainWindow)
        QtCore.QMetaObject.connectSlotsByName(toMOVMainWindow)

    def retranslateUi(self, toMOVMainWindow):
        toMOVMainWindow.setWindowTitle(_translate("toMOVMainWindow", "批量图片序列转MOV", None))
        self.choiceLabel.setText(_translate("toMOVMainWindow", "选择：", None))
        self.allLabel.setText(_translate("toMOVMainWindow", "全部", None))
        self.noneLabel.setText(_translate("toMOVMainWindow", "无", None))
        self.greenLabel.setText(_translate("toMOVMainWindow", "绿色", None))
        self.yellowLabel.setText(_translate("toMOVMainWindow", "黄色", None))
        self.redLabel.setText(_translate("toMOVMainWindow", "红色", None))
        self.toMOVBtn.setText(_translate("toMOVMainWindow", "toMOV", None))
        self.upLoadBtn.setText(_translate("toMOVMainWindow", "upLoad", None))


