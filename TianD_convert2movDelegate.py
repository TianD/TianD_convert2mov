#coding:utf-8
'''
Created on 2015年7月30日 下午7:25:38

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

from PyQt4 import QtCore, QtGui
               
        
class ComboBoxDelegate(QtGui.QStyledItemDelegate):
    
    def __init__(self, parent, data):
        super(ComboBoxDelegate, self).__init__(parent)
        self.parent = parent
        self.__data = data 
    
    def createEditor(self, parent, option, index):
        row = index.row()
        column = index.column()
        if self.__data[row]:
            editor = QtGui.QComboBox(parent)
            editor.addItems(self.__data[row][1:][column])
            return editor
        
    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        editor.setCurrentIndex(editor.findText(value[0]))
        
    def setModelData(self, editor, model, index):
        value = editor.currentIndex()
        model.setData(index, editor.itemData( value, QtCore.Qt.DisplayRole ) )

        
        
