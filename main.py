import sys
import os
from PySide6.QtCore import QProcess, QSettings, Qt, QEvent
from PySide6.QtWidgets import *
from PySide6.QtGui import QAction
import qdarkstyle
import logging
from qtawesome import icon
from layout.QTextEditLogger import QTextEditLogger
from backend.vol import vol_backend_v2

os.environ['QT_API'] = 'pyside6'

config = {"imagefile": ""}

res = ""


class LogWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.logTextBox = QTextEditLogger(self)
        self.logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - module: %(module)s - funcName: %(funcName)s\n--> %(message)s\n'))
        logging.getLogger().addHandler(self.logTextBox)
        logging.getLogger().setLevel(logging.DEBUG)

        self.layout = QVBoxLayout()
        message = QLabel("如遇到非预期错误，请提供详细日志")
        self.layout.addWidget(message)
        self.layout.addWidget(self.logTextBox.widget)
        self.setLayout(self.layout)
        self.setMinimumSize(800, 500)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Memory image auto-analyzer")
        self.setMinimumSize(1200, 800)

        # 设置项储存
        # self.settings = QSettings()

        # 设置菜单栏
        self.set_MenuBar()

        # 设置状态栏
        # 独立出来做一个窗体
        self.setStatusBar(QStatusBar(self))

        # 设置变量
        self.process_vol_v2 = None
        self.w = None

        # 设置工具栏
        self.set_ToolBar()

        self.ToolsBTN1 = QPushButton('测试1', self)
        self.ToolsBTN2 = QPushButton('测试2', self)
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.ToolsBTN2)
        self.stack.addWidget(self.ToolsBTN1)
        self.setCentralWidget(self.stack)

    def set_MenuBar(self):
        menu_bar = self.menuBar()
        menu_bar.setContextMenuPolicy(Qt.PreventContextMenu)
        menu_bar_size = menu_bar.font()
        menu_bar_size.setPointSize(9)
        menu_bar.setFont(menu_bar_size)

        # 设置文件菜单栏
        menu_file = menu_bar.addMenu("文件")
        menu_file.setFont(menu_bar_size)
        action_OpenNewFile = QAction(icon("fa5.file"), "打开内存镜像文件", self)
        action_OpenNewFile.setStatusTip("打开内存镜像文件")
        action_OpenNewFile.triggered.connect(self.OpenFile)
        menu_file.addAction(action_OpenNewFile)
        menu_file.addSeparator()
        action_ApplicationQuit = QAction(icon("fa5s.door-open"), "退出", self)
        action_ApplicationQuit.setStatusTip("退出程序")
        action_ApplicationQuit.triggered.connect(self.closeEvent)
        menu_file.addAction(action_ApplicationQuit)

        # 设置帮助菜单栏
        menu_help = menu_bar.addMenu("帮助")
        menu_help.setFont(menu_bar_size)
        action_ShowLog = QAction(icon("ri.newspaper-line"), "显示日志窗口", self)
        action_ShowLog.setStatusTip("显示程序日志")
        action_ShowLog.triggered.connect(self.show_log)
        menu_help.addAction(action_ShowLog)

    def set_ToolBar(self):
        self.toolbar = QToolBar("My main toolbar")
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        button_action = QAction("show log", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.show_log)
        self.toolbar.addAction(button_action)

        button_action = QAction("imageinfo", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.start_process)
        self.toolbar.addAction(button_action)

    def show_log(self):
        print("show log")
        if self.w is None:
            self.w = LogWindow()
        self.w.show()

    def print_res(self):
        print(self.process_vol_v2.res_imagefile)

    # 选取镜像文件
    def OpenFile(self):
        filename = QFileDialog.getOpenFileName(parent=self, caption='Open file', dir='.', filter='*')[0]
        if filename:
            print(filename)
            config["imagefile"] = filename
            logging.info("select image file:" + filename)

    def message(self, s):
        logging.info(s)

    def start_process(self):
        if config["imagefile"] == "":
            logging.warning("未指定文件")
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning!")
            dlg.setText("未选择有效的内存镜像文件!")
            dlg.exec()
            return 0
        if self.process_vol_v2 is None:  # No process running.
            self.message("Executing process")
            self.process_vol_v2 = vol_backend_v2(config["imagefile"], self)
            self.process_vol_v2.finished.connect(self.process_finished)  # Clean up once complete.
            self.process_vol_v2.imageinfo()

    def process_finished(self):
        self.message("Process finished.")
        self.p = None
        print(res)

    def closeEvent(self, event):
        for window in QApplication.topLevelWidgets():
            window.close()


if __name__ == "__main__":

    def app_quit():
        exit(0)

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())