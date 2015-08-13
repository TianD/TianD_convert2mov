#coding:utf-8
'''
Created on 2015年7月31日 下午4:05:02

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

import sys
from PyQt4 import QtGui, QtCore

class Node(object):
    
    def __init__(self, value, parent = None):
        self._value = value
        self._children = []
        self._parent = parent
        
        if parent is not None:
            parent.addChild(self)
            
    def addChild(self, child):
        self._children.append(child)
        
    def value(self):
        return self._value 
    
    def child(self, row):
        return self._children[row]
    
    def childCount(self):
        return len(self._children)   
    
    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)
        
    def log(self, tabLevel = -1):
        output = ""
        tabLevel +=1
        
        for i in range(tabLevel):
            output +='|\t'
            
        output += "|------" + self._name + "\n"
        
        for child in self._children:
            output += child.log(tabLevel)
            
        tabLevel -= 1
        #output += "\n"
        
        return output

    def __repr__(self):
        return self.log()
        
        
class TreeModel(QtCore.QAbstractItemModel):
    
    def __init__(self, root, source, headers = [], parent = None):
        super(TreeModel, self).__init__(parent)
        self._rootNode = root
        #self._data = data
        self._red = QtGui.QColor("#FF0000")
        self._green = QtGui.QColor("#00FF00")
        self._yellow = QtGui.QColor("#FFFF00")
        self._white = QtGui.QColor("#FFFFFF")
        self.checks = []
        self._headers = headers
        self.source = source

    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else :
            parentNode = parent.internalPointer()
            
        return parentNode.childCount()
    
    
    def columnCount(self, parent):
        return len(self._headers)


    def flags(self, index):
#         return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        column = index.column()
        node = index.internalPointer()
        if column == 5:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        elif not node.childCount() and column == 7:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable
        else :
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role):
        
        if not index.isValid():
            return None
        
        node = index.internalPointer()
        column = index.column()
        
        if role == QtCore.Qt.DisplayRole:
            if node.childCount():
                if column == 0:
                    return node.value()
            else :
                if column > 0 and column < 6:
                    return node.value()[column-1]
        
        if role == QtCore.Qt.FontRole:
            
            font = QtGui.QFont("Helvetica [Cronyx]")
            font.setPointSize(12)
            return font
        
        if not node.childCount() and column == 7 and role == QtCore.Qt.CheckStateRole:
            if node in self.checks:
                return QtCore.Qt.Checked
            else :
                return QtCore.Qt.Unchecked
        
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
                color = self._green
            elif colorStr == 'error' :
                color = self._red
            elif colorStr == 'warning' :
                color = self._yellow
            else :
                color = self._white
                     
            brush = QtGui.QBrush(color, style = QtCore.Qt.Dense4Pattern)
            brush.setColor(color)
             
            return brush
       
    def headerData(self, section, orientation, role):
        
        if role == QtCore.Qt.DisplayRole:
            
            if orientation == QtCore.Qt.Horizontal:
                
                if section < len(self._headers):
                    return self._headers[section]
                else:
                    return "not implemented"
                
    def parent(self, index):
        
        node = index.internalPointer()
        parentNode = node.parent()

        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        
        return self.createIndex(parentNode.row(), 0, parentNode)
    
    def index(self, row, column, parent):
        
        if not parent.isValid():
            parentNode = self._rootNode
        else :
            parentNode = parent.internalPointer()
        
        childItem = parentNode.child(row)
        
        if childItem:
            return self.createIndex(row, column, childItem)
        else :
            return QtCore.QModelIndex()
       
    def setData(self, index, value, role = QtCore.Qt.DisplayRole):
        
        if index.isValid():
            
            column = index.column()
            node = index.internalPointer()
            if column == 7 and role == QtCore.Qt.CheckStateRole:
                if value == QtCore.Qt.Checked:
                    self.checks.append(node)
                    return False
                else :
                    if node in self.checks :
                        self.checks.remove(node)
                        return False
            
        
              
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    
    rootNode = Node("Root")
    scName0 = Node("sc0", rootNode)
    scName1 = Node("sc1", rootNode)  
    path0 = Node(["name0", "start","end", "path0", scName0.row()], scName0)
    aa = Node(["name3", "start","end", "path0", path0.row()], path0)
    path1 = Node(["name1", "start","end", "path1", scName0.row()], scName0)
    bb = Node(["name4", "start","end", "path0", path1.row()], path1)
    path2 = Node(["name2", "start","end", "path2", scName1.row()], scName1)
    cc = Node(["name5", "start","end", "path0", path2.row()], path2)
    
    model = TreeModel(rootNode, ["name","path", "start","end", "row"])
    view = QtGui.QTreeView()
    view.setModel(model)
    view.show()
    
    sys.exit(app.exec_())