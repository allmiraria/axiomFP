import sys, os, json
cwd = os.path.curdir
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QHBoxLayout, QGridLayout, QGroupBox, QLabel, QPushButton
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QMessageBox, QWidget, QApplication, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui

class AddETOMethod(QWidget):
    def __init__(self):
        super(AddETOMethod, self).__init__()
        self.window_gui()

    def window_gui(self):
        font = self.font()
        font.setPointSize(14)
        self.setFont(font)
        self.setWindowTitle('add_eto_method_window_title')
        #self.setWindowIcon(QIcon(css.parameters_basic_icon))
        self.grid = QGridLayout()
        self.grid.addWidget(self.left_groupbox(), 0, 0, 1, 1)
        self.grid.addWidget(self.down_groupbox(), 1, 0, 1, 2)
        self.setLayout(self.grid)
        self.show()
        
    def left_groupbox(self):
        self.method_info_groupbox = QGroupBox('add_eto_method_info_caption')
        
        self.text_method_description = QLabel('add_eto_method_info_description')
        self.method_description = QTextEdit()
        
        self.method_info_groupbox.layout = QGridLayout()
        self.method_info_groupbox.layout.addWidget(self.text_method_description, 4, 0, 1, 1)
        self.method_info_groupbox.layout.addWidget(self.method_description, 5, 0, 1, 1)
        
        self.method_info_groupbox.setLayout(self.method_info_groupbox.layout)
        return self.method_info_groupbox  
    
    def down_groupbox(self):
        self.btn_groupbox = QGroupBox()
        self.btn_save = QPushButton('add_eto_method_btn_save')
        self.btn_save.clicked.connect(self.add_method)
        self.btn_cancel = QPushButton('add_eto_method_btn_close')
        self.btn_cancel.clicked.connect(self.close)
        self.btn_groupbox.layout = QHBoxLayout()
        self.btn_groupbox.layout.addWidget(self.btn_save)
        self.btn_groupbox.layout.addWidget(self.btn_cancel)
        self.btn_groupbox.setLayout(self.btn_groupbox.layout)
        return self.btn_groupbox
    
    def move_cursor(self):
        cursor = self.method_description.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.method_description.setTextCursor(cursor)

    def add_method(self):
        self.method_description.append('huehue')
        self.move_cursor()
            
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = AddETOMethod()
    sys.exit(mainApplication.exec_())