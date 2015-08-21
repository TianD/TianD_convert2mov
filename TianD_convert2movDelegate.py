#coding:utf-8
'''
Created on 2015年7月30日 下午7:25:38

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

from PyQt4 import QtCore, QtGui
               
        
class ComboBoxDelegate(QtGui.QStyledItemDelegate):
    
    def __init__(self, parent, root):
        super(ComboBoxDelegate, self).__init__(parent)
        self.parent = parent
        self.__root = root
      
    def createEditor(self, parent, option, index):
        node = index.internalPointer()
        row = index.row()
        column = index.column()
        if self.__root.childCount(): 
            if not node.childCount():
                childNode = self.__root.child(row)
                editor = QtGui.QComboBox(parent)
                editor.addItems(node.value()[column-1])
                return editor
        
    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        editor.setCurrentIndex(editor.findText(value[0]))
        
    def setModelData(self, editor, model, index):
        value = editor.currentIndex()
        model.setData(index, editor.itemData( value, QtCore.Qt.DisplayRole ) )