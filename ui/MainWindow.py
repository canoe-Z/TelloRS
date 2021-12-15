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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QRadioButton, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(40, 510, 325, 26))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_connect = QPushButton(self.layoutWidget)
        self.btn_connect.setObjectName(u"btn_connect")

        self.horizontalLayout.addWidget(self.btn_connect, 0, Qt.AlignBottom)

        self.btn_takephoto = QPushButton(self.layoutWidget)
        self.btn_takephoto.setObjectName(u"btn_takephoto")

        self.horizontalLayout.addWidget(self.btn_takephoto, 0, Qt.AlignBottom)

        self.btn_record = QPushButton(self.layoutWidget)
        self.btn_record.setObjectName(u"btn_record")

        self.horizontalLayout.addWidget(self.btn_record, 0, Qt.AlignBottom)

        self.pushButton = QPushButton(self.layoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton, 0, Qt.AlignBottom)

        self.layoutWidget1 = QWidget(self.centralwidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(690, 440, 73, 100))
        self.verticalLayout = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.rbtn_move_fixed = QRadioButton(self.layoutWidget1)
        self.rbtn_move_fixed.setObjectName(u"rbtn_move_fixed")

        self.verticalLayout.addWidget(self.rbtn_move_fixed, 0, Qt.AlignRight)

        self.rbtn_move_single = QRadioButton(self.layoutWidget1)
        self.rbtn_move_single.setObjectName(u"rbtn_move_single")

        self.verticalLayout.addWidget(self.rbtn_move_single, 0, Qt.AlignRight)

        self.rbtn_move_rc = QRadioButton(self.layoutWidget1)
        self.rbtn_move_rc.setObjectName(u"rbtn_move_rc")

        self.verticalLayout.addWidget(self.rbtn_move_rc, 0, Qt.AlignRight)

        self.chk_autocap = QCheckBox(self.layoutWidget1)
        self.chk_autocap.setObjectName(u"chk_autocap")

        self.verticalLayout.addWidget(self.chk_autocap, 0, Qt.AlignRight)

        self.label_source = QLabel(self.centralwidget)
        self.label_source.setObjectName(u"label_source")
        self.label_source.setEnabled(True)
        self.label_source.setGeometry(QRect(20, 10, 421, 441))
        self.label_template = QLabel(self.centralwidget)
        self.label_template.setObjectName(u"label_template")
        self.label_template.setGeometry(QRect(460, 120, 331, 191))
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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"TelloRS", None))
        self.btn_connect.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5Tello", None))
        self.btn_takephoto.setText(QCoreApplication.translate("MainWindow", u"\u62cd\u7167", None))
        self.btn_record.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5f55\u50cf", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u56fe\u50cf\u5339\u914d", None))
        self.rbtn_move_fixed.setText(QCoreApplication.translate("MainWindow", u"\u95f4\u6b47\u63a7\u5236", None))
        self.rbtn_move_single.setText(QCoreApplication.translate("MainWindow", u"\u5355\u6b21\u63a7\u5236", None))
        self.rbtn_move_rc.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u7eed\u63a7\u5236", None))
        self.chk_autocap.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u62cd\u7167", None))
        self.label_source.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_template.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u83dc\u5355", None))
    # retranslateUi

