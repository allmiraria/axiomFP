# PyQt5 & Python imports
import sys, os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QProxyStyle, QStyle, QToolTip, QAction, QMainWindow, QApplication, QDesktopWidget, QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QDesktopServices, QTextCursor
# b_alelle_plot imports
from plambases import variables
from widget.widget import BAlellePlot
cwd = os.path.curdir

class MyProxyStyle(QProxyStyle):
    pass
    def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):
        if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
            return 40
        else:
            return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.setFixedSize(variables.window_w, variables.window_h)
        self.window_gui()

    def window_gui(self):
        self.setWindowIcon(QIcon(variables.app_icon))
        self.setWindowTitle('b alelle plot - working beta')
        self.fileMenu()
        self.center_gui()
        self.central_widget = BAlellePlot()
        self.setCentralWidget(self.central_widget)
        self.show()

    def center_gui(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fileMenu(self):
        menubar = self.menuBar()
        font = menubar.font()
        font.setPointSize(variables.font_size)
        menubar.setFont(font)

        # File:
        fileMenu = menubar.addMenu('File')
        font = fileMenu.font()
        font.setPointSize(variables.font_size)
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # File - Exit:
        exitAct = QAction(QIcon(variables.exit_icon), 'Close', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setToolTip('Close application')
        exitAct.triggered.connect(self.exit_app)
        fileMenu.addAction(exitAct)

        # Help:
        fileMenu = menubar.addMenu('Help')
        font = fileMenu.font()
        font.setPointSize(variables.font_size)
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # Help - About:
        aboutAct = QAction(QIcon(variables.about_icon), 'Help', self)
        aboutAct.setShortcut('Ctrl+A')
        aboutAct.setToolTip('About application')
        aboutAct.triggered.connect(self.about_window)
        fileMenu.addAction(aboutAct)

        # Help - Manual:
        helpAct = QAction(QIcon(variables.manual_icon), 'Manual', self)
        helpAct.setShortcut('F1')
        helpAct.setToolTip('How to use application')
        helpAct.triggered.connect(self.manual_window)
        fileMenu.addAction(helpAct)

    # File:
    def exit_app(self):
        mainApplication.quit()

    # Help:
    def about_window(self):
        pass

    def manual_window(self):
        QDesktopServices.openUrl(QUrl(variables.youtube_link))

if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    myStyle = MyProxyStyle('Fusion')
    # The proxy style should be based on an existing style, like 'Windows',
    # 'Motif', 'Plastique', 'Fusion', ...
    mainApplication.setStyle(myStyle)
    mainWindow = MainWindow()
    sys.exit(mainApplication.exec_())
