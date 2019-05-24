import os, sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setGeometry(0,0, 500,650)
        self.setWindowTitle("Debreate")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(500,650)
        self.setMinimumSize(500,650)
        self.center()

        # --- Menu --- #
        open = QAction("Exit", self)
        save = QAction("Save", self)
        build = QAction("Build", self)
        exit = QAction("Quit", self)

        menu_bar = QMenuBar()
        file = menu_bar.addMenu("&File")
        help = menu_bar.addMenu("&Help")

        file.addAction(open)
        file.addAction(save)
        file.addAction(build)
        file.addAction(exit)

        tab_widget = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()

        p1_vertical = QVBoxLayout(tab1)
        p2_vertical = QVBoxLayout(tab2)

        tab_widget.addTab(tab1, "Main")
        tab_widget.addTab(tab2, "Description")

        button1 = QPushButton("button1")
        p1_vertical.addWidget(button1)

        vbox = QVBoxLayout()
        vbox.addWidget(menu_bar)
        vbox.addWidget(tab_widget)

        self.setLayout(vbox)


    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)


app = QApplication(sys.argv)
frame = MainWindow()
frame.show()
sys.exit(app.exec_())