import sys, os, datetime
from time import sleep
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QGroupBox, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox, QWidget, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtCore, QtGui
from plambases import variables

class Worker(QtCore.QObject):
    progressed = QtCore.pyqtSignal(int)
    messaged = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()

    def run(self):
        for i in range(1, 11):
            self.progressed.emit(int(i*10))
            self.messaged.emit(str(i))
            sleep(0.5)

        self.finished.emit()


class BAlellePlot(QWidget):
    def __init__(self):
        super().__init__()
        self.__thread = QtCore.QThread()
        self.window_gui()
        self.status_update(message=variables.welcome_message)


    def window_gui(self):
        font = self.font()
        font.setPointSize(variables.font_size)
        self.setFont(font)
        self.setFixedSize(variables.window_w, variables.window_h)
        self.grid = QGridLayout()
        self.grid.addWidget(self.data_input_groupbox(), 0, 0, 1, 1)
        self.grid.addWidget(self.data_options_groupbox(), 1, 0, 1, 1)
        self.grid.addWidget(self.status_update_groupbox(), 0, 1, 2, 1)
        #self.grid.addWidget(self.buttons_groupbox(), 2, 1, 1, 1)
        self.setLayout(self.grid)
        self.show()

    def data_input_groupbox(self):
        self.data_groupbox = QGroupBox('Data files:')
        self.font = self.data_groupbox.font()
        self.font.setPointSize(variables.font_size)
        self.data_groupbox.setFont(self.font)

        self.snp_stat_gp = QGroupBox()
        self.btn_snp_stat_browse = QPushButton('Browse for SNP Statistics file')
        self.btn_snp_stat_browse.clicked.connect(self.browse_snp_stat)
        self.snp_file_stat_text = QLabel()
        self.snp_file_stat_text.setWordWrap(True)
        self.snp_file_stat_text.setText('No SNP Statistics file selected.')
        
        self.snp_stat_gp.layout = QGridLayout()
        self.snp_stat_gp.layout.addWidget(self.btn_snp_stat_browse)
        self.snp_stat_gp.layout.addWidget(self.snp_file_stat_text)
        self.snp_stat_gp.setLayout(self.snp_stat_gp.layout)

        self.snp_cc_gp = QGroupBox()
        self.btn_snp_cc_browse = QPushButton('Browse for SNP Call Contrasts Position file')
        self.btn_snp_cc_browse.clicked.connect(self.browse_snp_cc)
        self.snp_file_cc_text = QLabel()
        self.snp_file_cc_text.setWordWrap(True)
        self.snp_file_cc_text.setText('No SNP Call Contrasts Position file selected.')
        
        self.snp_cc_gp.layout = QGridLayout()
        self.snp_cc_gp.layout.addWidget(self.btn_snp_cc_browse)
        self.snp_cc_gp.layout.addWidget(self.snp_file_cc_text)
        self.snp_cc_gp.setLayout(self.snp_cc_gp.layout)


        self.data_groupbox.layout = QGridLayout()
        self.data_groupbox.layout.addWidget(self.snp_stat_gp, 0, 0, 1, 1)
        self.data_groupbox.layout.addWidget(self.snp_cc_gp, 0, 1, 1, 1)
        self.data_groupbox.setLayout(self.data_groupbox.layout)
        return self.data_groupbox
    
    def browse_snp_stat(self):
        self.snp_stat_file_path, _ = QFileDialog.getOpenFileName(self, 'Select SNP Statistics file', os.path.curdir, '*.txt')
        with open(self.snp_stat_file_path) as f:
            lines = f.readlines()
        tabs, letabs = [], []
        for line in lines:
            lineContains = line.split('\t')
            lineLength = len(lineContains)
            if lineLength < 3:
                letabs.append(line)
            else:
                tabs.append(lineContains)
        if len(letabs) != 0:
            self.status_update(message='Selected file not supported. Not a tab delimited txt file.')
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText('Selected file not supported. Not a tab delimited txt file.')
            self.msg.setWindowTitle('File not supported')
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            msg_selected_snp_stat = 'Selected SNP Statistics file: ' + self.snp_stat_file_path
            self.status_update(message=msg_selected_snp_stat)
            self.snp_file_stat_text.setText(self.snp_stat_file_path)

    def browse_snp_cc(self):
        self.snp_cc_file_path, _ = QFileDialog.getOpenFileName(self, 'Select SNP Call Contrasts Positions file', os.path.curdir, '*.txt')
        # prvo provjeri ima li file name, ako nema nista
        with open(self.snp_cc_file_path) as f:
            lines = f.readlines()
        tabs, letabs = [], []
        for line in lines:
            lineContains = line.split('\t')
            lineLength = len(lineContains)
            if lineLength < 3:
                letabs.append(line)
            else:
                tabs.append(lineContains)
        if len(letabs) != 0:
            self.status_update(message='Selected file not supported. Not a tab delimited txt file.')
            self.msg = QMessageBox()
            self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText('Selected file not supported. Not a tab delimited txt file.')
            self.msg.setWindowTitle('File not supported')
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.msg.close)
            self.msg.show()
        else:
            msg_selected_snp_cc = 'Selected SNP Call Contrasts Positions file: ' + self.snp_cc_file_path
            self.status_update(message=msg_selected_snp_cc)
            self.snp_file_cc_text.setText(self.snp_cc_file_path)

    def data_options_groupbox(self):
        self.data_options_groupbox = QGroupBox('Data options:')
        self.font = self.data_options_groupbox.font()
        self.font.setPointSize(variables.font_size)
        self.data_options_groupbox.setFont(self.font)

        self.snp_stat_gp = QGroupBox()
        self.btn_snp_stat_browse = QPushButton('Browse for SNP Statistics file')
        self.btn_snp_stat_browse.clicked.connect(self.browse_snp_stat)
        self.snp_file_stat_text = QLabel()
        self.snp_file_stat_text.setWordWrap(True)
        self.snp_file_stat_text.setText('No SNP Statistics file selected.')
        
        self.snp_stat_gp.layout = QGridLayout()
        self.snp_stat_gp.layout.addWidget(self.btn_snp_stat_browse)
        self.snp_stat_gp.layout.addWidget(self.snp_file_stat_text)
        self.snp_stat_gp.setLayout(self.snp_stat_gp.layout)

        self.snp_cc_gp = QGroupBox()
        self.btn_snp_cc_browse = QPushButton('Browse for SNP Call Contrasts Position file')
        self.btn_snp_cc_browse.clicked.connect(self.browse_snp_cc)
        self.snp_file_cc_text = QLabel()
        self.snp_file_cc_text.setWordWrap(True)
        self.snp_file_cc_text.setText('No SNP Call Contrasts Position file selected.')
        
        self.snp_cc_gp.layout = QGridLayout()
        self.snp_cc_gp.layout.addWidget(self.btn_snp_cc_browse)
        self.snp_cc_gp.layout.addWidget(self.snp_file_cc_text)
        self.snp_cc_gp.setLayout(self.snp_cc_gp.layout)


        self.data_options_groupbox.layout = QGridLayout()
        self.data_options_groupbox.layout.addWidget(self.snp_stat_gp, 0, 0, 1, 1)
        self.data_options_groupbox.layout.addWidget(self.snp_cc_gp, 0, 1, 1, 1)
        self.data_options_groupbox.setLayout(self.data_options_groupbox.layout)
        return self.data_options_groupbox
    
        
    def status_update_groupbox(self):
        self.info_groupbox = QGroupBox('Status update window:')
        self.info_groupbox.setFixedWidth(variables.status_w)
        self.font = self.info_groupbox.font()
        self.font.setPointSize(variables.font_size_update)
        self.info_groupbox.setFont(self.font)
        self.status_window = QTextEdit()
        self.info_groupbox.layout = QGridLayout()
        self.info_groupbox.layout.addWidget(self.status_window)
        self.info_groupbox.setLayout(self.info_groupbox.layout)
        return self.info_groupbox
    
    def cursor_updater(self):
        cursor = self.status_window.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.status_window.setTextCursor(cursor)

    def status_update(self, message):
        ct = datetime.datetime.now().strftime('%H:%M:%S')
        self.status_window.append(ct + ' : ' + message)
        self.cursor_updater()

    
    def buttons_groupbox(self):
        self.btn_groupbox = QGroupBox()
        self.btn_save = QPushButton('add_eto_method_btn_save')
        self.btn_save.clicked.connect(self.status_update)
        self.btn_cancel = QPushButton('add_eto_method_btn_close')
        self.btn_cancel.clicked.connect(self.close)
        self.btn_groupbox.layout = QHBoxLayout()
        self.btn_groupbox.layout.addWidget(self.btn_save)
        self.btn_groupbox.layout.addWidget(self.btn_cancel)
        self.btn_groupbox.setLayout(self.btn_groupbox.layout)
        return self.btn_groupbox
            
if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    mainWindow = BAlellePlot()
    sys.exit(mainApplication.exec_())