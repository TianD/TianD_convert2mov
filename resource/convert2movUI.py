# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Scripts\Eclipse\TianD_convert2mov\resource\convert2movUI.ui'
#
# Created: Fri Aug 14 11:41:34 2015
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
        toMOVMainWindow.resize(1064, 632)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/resource/LOGO.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        toMOVMainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(toMOVMainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget_2 = QtGui.QWidget(self.centralwidget)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.treeView = QtGui.QTreeView(self.widget_2)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.verticalLayout_2.addWidget(self.treeView)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(self.widget_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.label_2 = QtGui.QLabel(self.widget_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.label = QtGui.QLabel(self.widget_2)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.label_5 = QtGui.QLabel(self.widget_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.label_4 = QtGui.QLabel(self.widget_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        self.label_6 = QtGui.QLabel(self.widget_2)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_2.addWidget(self.label_6)
        spacerItem = QtGui.QSpacerItem(360, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addWidget(self.widget_2)
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.descriptionBrowser = QtGui.QTextBrowser(self.widget)
        self.descriptionBrowser.setObjectName(_fromUtf8("descriptionBrowser"))
        self.verticalLayout.addWidget(self.descriptionBrowser)
        self.toMOVBtn = QtGui.QPushButton(self.widget)
        self.toMOVBtn.setObjectName(_fromUtf8("toMOVBtn"))
        self.verticalLayout.addWidget(self.toMOVBtn)
        self.upLoadBtn = QtGui.QPushButton(self.widget)
        self.upLoadBtn.setObjectName(_fromUtf8("upLoadBtn"))
        self.verticalLayout.addWidget(self.upLoadBtn)
        self.horizontalLayout.addWidget(self.widget)
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
        self.label_3.setText(_translate("toMOVMainWindow", "选择：", None))
        self.label_2.setText(_translate("toMOVMainWindow", "全部", None))
        self.label.setText(_translate("toMOVMainWindow", "无", None))
        self.label_5.setText(_translate("toMOVMainWindow", "绿色", None))
        self.label_4.setText(_translate("toMOVMainWindow", "黄色", None))
        self.label_6.setText(_translate("toMOVMainWindow", "红色", None))
        self.toMOVBtn.setText(_translate("toMOVMainWindow", "toMOV", None))
        self.upLoadBtn.setText(_translate("toMOVMainWindow", "upLoad", None))

import LOGO_rc_rc
