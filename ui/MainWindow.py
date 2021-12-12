# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_source = QLabel(self.centralwidget)
        self.label_source.setObjectName(u"label_source")
        self.label_source.setGeometry(QRect(70, 40, 361, 391))
        self.btn_connect = QPushButton(self.centralwidget)
        self.btn_connect.setObjectName(u"btn_connect")
        self.btn_connect.setGeometry(QRect(80, 490, 75, 24))
        self.btn_takephoto = QPushButton(self.centralwidget)
        self.btn_takephoto.setObjectName(u"btn_takephoto")
        self.btn_takephoto.setGeometry(QRect(250, 490, 75, 24))
        self.btn_record = QPushButton(self.centralwidget)
        self.btn_record.setObjectName(u"btn_record")
        self.btn_record.setGeometry(QRect(410, 490, 75, 24))
        self.label_template = QLabel(self.centralwidget)
        self.label_template.setObjectName(u"label_template")
        self.label_template.setGeometry(QRect(520, 100, 251, 171))
        self.rbtn_move_single = QRadioButton(self.centralwidget)
        self.rbtn_move_single.setObjectName(u"rbtn_move_single")
        self.rbtn_move_single.setGeometry(QRect(610, 400, 95, 20))
        self.rbtn_move_rc = QRadioButton(self.centralwidget)
        self.rbtn_move_rc.setObjectName(u"rbtn_move_rc")
        self.rbtn_move_rc.setGeometry(QRect(610, 420, 95, 20))
        self.chk_autocap = QCheckBox(self.centralwidget)
        self.chk_autocap.setObjectName(u"chk_autocap")
        self.chk_autocap.setGeometry(QRect(610, 440, 79, 20))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(550, 490, 91, 24))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_source.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.btn_connect.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5Tello", None))
        self.btn_takephoto.setText(QCoreApplication.translate("MainWindow", u"\u62cd\u7167", None))
        self.btn_record.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5f55\u50cf", None))
        self.label_template.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.rbtn_move_single.setText(QCoreApplication.translate("MainWindow", u"\u95f4\u6b47\u63a7\u5236", None))
        self.rbtn_move_rc.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u7eed\u63a7\u5236", None))
        self.chk_autocap.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u62cd\u7167", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u56fe\u50cf\u5339\u914d", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u83dc\u5355", None))
    # retranslateUi

