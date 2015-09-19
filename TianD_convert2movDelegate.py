#coding:utf-8
'''
Created on 2015年7月30日 下午7:25:38

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''

from PyQt4 import QtCore, QtGui

import LOGO_rc

COMBOBOX_STYLE = """
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;

    border-left-color: darkgray;
    border-left-style: solid; /* just a single line */
    border-top-right-radius: 3px; /* same radius as the QComboBox */
    border-bottom-right-radius: 3px;
}
QComboBox {
    border: 0px solid gray;
    min-width: 6em;
    background-color: #"""
    
COMBOBOX_CLICK_STYLE = """
QComboBox::down-arrow {
    image: url(:arrow_down.png);
}
"""


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
                color = index.data(QtCore.Qt.BackgroundRole).toPyObject().color().rgb()
                colorStr = "%x" %color
                COMPLETE_COMBOBOX_STYLE = COMBOBOX_STYLE + colorStr[2:] + ";\n}"
                editor = QtGui.QComboBox(parent)
                editor.setStyleSheet(COMPLETE_COMBOBOX_STYLE)
                editor.addItems(node.value()[column-1])
                return editor
        
    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        editor.setCurrentIndex(editor.findText(value[0]))
        
    def setModelData(self, editor, model, index):
        value = editor.currentIndex()
        model.setData(index, editor.itemData( value, QtCore.Qt.DisplayRole ) )