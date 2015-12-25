#coding:utf-8
'''
Created on 2015年7月31日 下午4:05:02

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

import sys
from PyQt4 import QtGui, QtCore

import LOGO_rc

class Node(object):
    
    def __init__(self, value, parent = None):
        self.__value = value
        self.__children = []
        self.__parent = parent
        
        if parent is not None:
            parent.addChild(self)
            
    def addChild(self, child):
        self.__children.append(child)
        
    def value(self):
        return self.__value 
    
    def child(self, row):
        return self.__children[row]
    
    def childCount(self):
        return len(self.__children)
    
    def parent(self):
        return self.__parent

    def row(self):
        if self.__parent is not None:
            return self.__parent.__children.index(self)
        
        
class TreeModel(QtCore.QAbstractItemModel):
    
    def __init__(self, root, source, headers = [], parent = None):
        super(TreeModel, self).__init__(parent)
        self.__rootNode = root
        self.__red = QtGui.QColor("#FF8585")
        self.__green = QtGui.QColor("#85FF85")
        self.__yellow = QtGui.QColor("#FFFF85")
        self.__white = QtGui.QColor("#F0F0F0")
        self.checks = []
        self.__headers = headers
        self.source = source
        self.__checkHeaders = ["All", "None", "Success", "Warning", "Error"]

    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self.__rootNode
        else :
            parentNode = parent.internalPointer()
            
        return parentNode.childCount()
    
    
    def columnCount(self, parent):
        return len(self.__headers)


    def flags(self, index):
        column = index.column()
        node = index.internalPointer()
        if not node.childCount() and (column == 5 or column == 1 or column == 4):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        elif not node.childCount() and column == 8:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable
        else :
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role):
        
        if not index.isValid():
            return None
        
        node = index.internalPointer()
        row = index.column()
        column = index.column()
        
        
        #先获取版本号, 根据不同的版本号获取其他相应的属性的值
        #生成其他几列的值
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if node.childCount():
                if column == 0:
                    return node.value()
            else :
                if column > 0 and column < 7 and column not in [2, 3]:
                    return node.value()[column-1]
                elif column in [2,3]:
                    return node.value()[column-1]
                

        #生成第八列(是否已经上传)的装饰值
        if role == QtCore.Qt.DecorationRole:
            if not node.childCount():
                if node.value()[6] and column == 7 :
                    icon = QtGui.QPixmap(":Warning.png")
                    icon.scaled(icon.size()*0.2)
                    return icon
        
        #生成每个字符的字体和大小
        if role == QtCore.Qt.FontRole:
            
            font = QtGui.QFont("Helvetica [Cronyx]")
            font.setPointSize(12)
            return font
        
        #生成最后一列(选择)的值
        if not node.childCount() and column == 8 and role == QtCore.Qt.CheckStateRole:
            return node.value()[column-1]
        
        #生成每行的背景色
        if role == QtCore.Qt.BackgroundRole:
             
            row = index.row()
            node = index.internalPointer()
            if not node.childCount():
                parent = node.parent()
                topParent = parent.parent()
                colorStr = self.source[topParent.value()][parent.value()][row][-1]
            else :
                colorStr = ''
            if colorStr == 'success' :
                color = self.__green
            elif colorStr == 'error' :
                color = self.__red
            elif colorStr == 'warning' :
                color = self.__yellow
            else :
                color = self.__white
             
            brush = QtGui.QBrush(color, style = QtCore.Qt.SolidPattern)
            brush.setColor(color)
            
             
            return brush

            
    def headerData(self, section, orientation, role):
        
        if role == QtCore.Qt.DisplayRole:
            
            if orientation == QtCore.Qt.Horizontal:
                
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return "not implemented"
                
                
    def parent(self, index):
        
        node = index.internalPointer()
        parentNode = node.parent()

        if parentNode == self.__rootNode:
            return QtCore.QModelIndex()
        
        return self.createIndex(parentNode.row(), 0, parentNode)
    
    def index(self, row, column, parent):
        
        if not parent.isValid():
            parentNode = self.__rootNode
        else :
            parentNode = parent.internalPointer()
        
        childItem = parentNode.child(row)
        
        if childItem:
            return self.createIndex(row, column, childItem)
        else :
            return QtCore.QModelIndex()
       
    def setData(self, index, value, role = QtCore.Qt.DisplayRole):
        
        if index.isValid():
            
            row = index.row()
            column = index.column()
            parent = index.parent()
            node = index.internalPointer()
            
            #修改最后一列(选择)的值
            if column == 8 and role == QtCore.Qt.CheckStateRole:
                if value == QtCore.Qt.Checked:
                    node.value()[column-1] = 2
                else :
                    node.value()[column-1] = 0
                self.dataChanged.emit(index, index)
                return True
            
            #修改第二列(输出名)和第五列(输出路径)的值
            if (column == 1 or column == 4) and role == QtCore.Qt.EditRole:
                node.value()[column-1] = str(value.toString())
                self.dataChanged.emit(index, index)
                return True
            
            #修改第六列(版本号)的值
            if column == 5 and (role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole):
                node.value()[column-1] = str(value.toString())
                self.dataChanged.emit(index, index)
                return True
            
            if column in [2,3] and role == QtCore.Qt.DisplayRole:
                print node.value(), node.value()[column -1]
                node.value()[column -1] = str(value)
                self.dataChanged.emit(index, index)
                return True
    
    @QtCore.pyqtSlot(QtCore.QModelIndex, int)
    def setBroData(self, index, i):
        if index.isValid():
            row = index.row()
            column = index.column()
            parent = index.parent()
            node = index.internalPointer()
            parentNode = parent.internalPointer()
            topparent = parent.parent()
            topNode = topparent.internalPointer()
            
            sfIndex = self.index(row, 2, parent)
            efIndex = self.index(row, 3, parent)
            sfValue = self.source[topNode.value()][parentNode.value()][row][1][i]
            efValue = self.source[topNode.value()][parentNode.value()][row][2][i]
            self.setData(sfIndex, sfValue, QtCore.Qt.DisplayRole)
            self.setData(efIndex, efValue, QtCore.Qt.DisplayRole)