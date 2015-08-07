#coding:utf-8
'''
Created on 2015年7月31日 下午4:05:02

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''


from PyQt4 import QtGui, QtCore

class TableModel(QtCore.QAbstractTableModel):
    
    def __init__(self, data = [[]], headers = [], parent = None):
        super(TableModel, self).__init__(parent)
        self.__data = data
        self.__red = QtGui.QColor("#FF0000")
        self.__green = QtGui.QColor("#00FF00")
        self.__yellow = QtGui.QColor("#FFFF00")
        self.__white = QtGui.QColor("#FFFFFF")
        self.checks = {}
        self.__headers = headers

    def rowCount(self, parent):
        return len(self.__data)
    
    
    def columnCount(self, parent):
        return len(self.__headers)


    def flags(self, index):
#         return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        row = index.row()
        column = index.column()
        if self.__data[row] :     
            if column == 3:
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
            else :
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else :
            # if current index has no value, it will be cannot be selected
            return QtCore.Qt.NoItemFlags

    def data(self, index, role):
        
        if role == QtCore.Qt.BackgroundRole:
            
            row = index.row()
            column = index.column()
            if self.__data[row] :
                colorStr = self.__data[row][0]
            else :
                colorStr = ''
            if colorStr == 'green' :
                color = self.__green
            elif colorStr == 'red' :
                color = self.__red
            elif colorStr == 'yellow' :
                color = self.__yellow
            else :
                color = self.__white
                    
            brush = QtGui.QBrush(color, style = QtCore.Qt.Dense4Pattern)
            brush.setColor(color)
            
            return brush

              
        if role == QtCore.Qt.DisplayRole:
            
            row = index.row()
            column = index.column()
            if self.__data[row] :
                try:
                    value = self.__data[row][1:][column]
                except:
                    value = ''
            else :
                value = ''
            
            return value
            
                
    def headerData(self, section, orientation, role):
        
        if role == QtCore.Qt.DisplayRole:
            
            if orientation == QtCore.Qt.Horizontal:
                
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return "not implemented"
    