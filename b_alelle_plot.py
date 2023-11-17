# PyQt5 & Python imports
import sys, os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QProxyStyle, QStyle, QToolTip, QAction, QMainWindow, QApplication, QDesktopWidget, QMenu
from PyQt5.QtWidgets import QStatusBar, QProgressBar, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QSizePolicy, QSizePolicy
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import pandas
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

class LoadSTATFileThread(QThread):
    progress_updated = pyqtSignal(int)
    finished_loading = pyqtSignal(pandas.DataFrame)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        df = pandas.read_csv(self.file_path)

        total_rows = len(df)
        step = total_rows // 10
        for i in range(0, total_rows, step):
            self.progress_updated.emit(i)

        self.finished_loading.emit(df)
        MainWindow.statusBar().showMessage('Učitao')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(variables.window_w, variables.window_h)
        self.window_gui()

    def window_gui(self):
        self.setWindowIcon(QIcon(variables.app_icon))
        self.setWindowTitle('b alelle plot - working beta')
        self.fileMenu()
        self.center_gui()

        self.statusBar().showMessage('Ready')
        self.progressBar = QProgressBar()
        #self.progressBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.statusBar().addPermanentWidget(self.progressBar)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()

        

        self.load_button = QPushButton("Load File", self)
        self.load_button.clicked.connect(self.load_file)

        layout.addWidget(self.load_button)
        #layout.addWidget(self.status_bar)

        central_widget.setLayout(layout)

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

    def load_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")

        if file_path:
            self.load_data(file_path)

    def load_data(self, file_path):
        self.worker_thread = LoadSTATFileThread(file_path)
        self.worker_thread.progress_updated.connect(self.update_progress)
        self.worker_thread.finished_loading.connect(self.handle_finished_loading)

        self.progressBar.setValue(0)
        self.worker_thread.start()

    def update_progress(self, value):
        self.progressBar.setValue(value)

    def handle_finished_loading(self, data_frame):
        # Do something with the loaded data, e.g., display it in a table
        print("Data loaded successfully!")
        print(data_frame.head())

        # Clean up the worker thread
        self.worker_thread.quit()
        self.worker_thread.wait()


if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    myStyle = MyProxyStyle('Fusion')
    # The proxy style should be based on an existing style, like 'Windows',
    # 'Motif', 'Plastique', 'Fusion', ...
    mainApplication.setStyle(myStyle)
    mainWindow = MainWindow()
    sys.exit(mainApplication.exec_())
