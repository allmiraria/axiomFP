from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QProxyStyle, QStyle, QToolTip
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QDesktopWidget, QMenu
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QDesktopServices
from widgets.image_widget import AddETOMethod
from variables import css, var
import sys
import os
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
        #self.setWindowState(QtCore.Qt.WindowMaximized)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint)
        self.window_gui()

    def window_gui(self):
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon(css.srclet_icon))
        self.setWindowTitle('huehue')
        self.fileMenu()
        self.center_gui()
        self.central_widget = AddETOMethod()
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
        font.setPointSize(12)
        menubar.setFont(font)

        # File:
        fileMenu = menubar.addMenu('file')
        font = fileMenu.font()
        font.setPointSize(12)
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # File - Settings:
        settingsAct = QAction(QIcon(css.settings_icon),
                              'settings', self)
        settingsAct.setShortcut('Ctrl+S')
        settingsAct.setToolTip('settings_tooltip')
        settingsAct.triggered.connect(self.settings_window)
        fileMenu.addAction(settingsAct)

        fileMenu.addSeparator()

        # File - Exit:
        exitAct = QAction(QIcon(css.exit_icon),
                          'exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setToolTip('exit_tooltip')
        exitAct.triggered.connect(self.exit_srclet)
        fileMenu.addAction(exitAct)

        # Project:
        fileMenu = menubar.addMenu('menu_project')
        font = fileMenu.font()
        font.setPointSize(12)
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # Project - New project:
        newProjectAct = QAction(
            QIcon((css.new_project_icon)), 'menu_project_new_project', self)
        newProjectAct.setShortcut('Ctrl+N')
        newProjectAct.setToolTip('menu_project_new_project_tooltip')
        newProjectAct.triggered.connect(self.new_project_window)
        fileMenu.addAction(newProjectAct)

        # Project - Open existing project:
        openProjectAct = QAction(
            QIcon((css.open_project_icon)), 'menu_project_open_project', self)
        openProjectAct.setShortcut('Ctrl+O')
        openProjectAct.setToolTip('menu_project_open_project_tooltip')
        openProjectAct.triggered.connect(self.open_project_window)
        fileMenu.addAction(openProjectAct)

        # Customize:
        fileMenu = menubar.addMenu('menu_customize')
        font = fileMenu.font()
        font.setPointSize(12)
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # Customize - Parameters:
        parameters_menu = QMenu('menu_customize_parameters', self)
        parameters_menu.setIcon(QIcon(css.parameters_icon))
        font = parameters_menu.font()
        font.setPointSize(12)
        parameters_menu.setFont(font)
        parameters_menu.setToolTipsVisible(True)

        parametersAct = QAction(QIcon(css.parameters_basic_icon), 'menu_customize_basic_parameters', self)
        parametersAct.setShortcut('Ctrl+B')
        parametersAct.setToolTip('menu_customize_basic_parameters_tooltip')
        parametersAct.triggered.connect(self.basic_parameters_window)
        parameters_menu.addAction(parametersAct)

        complexParametersAct = QAction(QIcon(
            css.parameters_complex_icon), 'enu_customize_changable_parameters', self)
        complexParametersAct.setShortcut('Ctrl+R')
        complexParametersAct.setToolTip('menu_customize_changable_parameters_tooltip')
        complexParametersAct.triggered.connect(self.changable_parameters_window)
        parameters_menu.addAction(complexParametersAct)

        fileMenu.addMenu(parameters_menu)

        # Customize - Methods:
        methods_menu = QMenu('menu_customize_methods', self)
        methods_menu.setIcon(QIcon(css.methods_icon))
        font = methods_menu.font()
        font.setPointSize(12)
        methods_menu.setFont(font)
        methods_menu.setToolTipsVisible(True)

        etoAct = QAction(QIcon(css.methods_eto_icon), 'menu_customize_methods_eto', self)
        etoAct.triggered.connect(self.eto_methods_window)
        etoAct.setShortcut('Ctrl+E')
        etoAct.setToolTip('menu_customize_methods_eto_tooltip')
        methods_menu.addAction(etoAct)

        wbAct = QAction(QIcon(css.methods_wb_icon), 'menu_customize_methods_wb', self)
        wbAct.triggered.connect(self.wb_methods_window)
        wbAct.setShortcut('Ctrl+W')
        wbAct.setToolTip('menu_customize_methods_wb_tooltip')
        methods_menu.addAction(wbAct)

        otherAct = QAction(QIcon(css.methods_others_icon), 'menu_customize_methods_others', self)
        otherAct.triggered.connect(self.other_methods_window)
        otherAct.setShortcut('Ctrl+T')
        otherAct.setToolTip('menu_customize_methods_others_tooltip')
        methods_menu.addAction(otherAct)

        fileMenu.addMenu(methods_menu)

        # Help:
        fileMenu = menubar.addMenu('menu_help')
        font = fileMenu.font()
        font.setPointSize(12)
        fileMenu.setFont(font)
        fileMenu.setToolTipsVisible(True)

        # Help - About:
        aboutAct = QAction(QIcon(css.about_icon), 'menu_help_about', self)
        aboutAct.setShortcut('Ctrl+A')
        aboutAct.setToolTip('menu_help_about_tooltip')
        aboutAct.triggered.connect(self.about_window)
        fileMenu.addAction(aboutAct)

        # Help - Manual:
        helpAct = QAction(QIcon(css.manual_icon), 'menu_help_manual', self)
        helpAct.setShortcut('F1')
        helpAct.setToolTip('menu_help_manual_tooltip')
        helpAct.triggered.connect(self.manual_window)
        fileMenu.addAction(helpAct)

    # File:
    def settings_window(self):
        pass

    def exit_srclet(self):
        mainApplication.quit()
        # self.close()

        # self.window_basic_parameters.close()

    # Project:
    def new_project_window(self):
        pass

    def open_project_window(self):
        pass

    # Customize:
    def basic_parameters_window(self):
        pass

    def changable_parameters_window(self):
        pass

    def eto_methods_window(self):
        pass
        # self.window = ETOMethodsWindow(self.language)

    def wb_methods_window(self):
        pass

    def other_methods_window(self):
        pass

    # Help:
    def about_window(self):
        pass

    def manual_window(self):
        # self.window = ManualWindow(self.language)
        QDesktopServices.openUrl(QUrl(
            'https://www.youtube.com/watch?v=ECTLzJow1Wo&list=PLBO2iP5zSYD7CbGOXEnMsUoWSkyxRsXTd'))


if __name__ == '__main__':
    mainApplication = QApplication(sys.argv)
    myStyle = MyProxyStyle('Plastique')
    # The proxy style should be based on an existing style, like 'Windows',
    # 'Motif', 'Plastique', 'Fusion', ...
    mainApplication.setStyle(myStyle)
    mainWindow = MainWindow()
    sys.exit(mainApplication.exec_())
