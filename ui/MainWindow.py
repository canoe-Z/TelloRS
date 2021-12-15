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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_source = QLabel(self.frame_2)
        self.label_source.setObjectName(u"label_source")
        self.label_source.setEnabled(True)
        self.label_source.setMinimumSize(QSize(400, 400))

        self.verticalLayout_2.addWidget(self.label_source)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_connect = QPushButton(self.frame_2)
        self.btn_connect.setObjectName(u"btn_connect")

        self.horizontalLayout_2.addWidget(self.btn_connect)

        self.btn_record = QPushButton(self.frame_2)
        self.btn_record.setObjectName(u"btn_record")

        self.horizontalLayout_2.addWidget(self.btn_record)

        self.btn_takephoto = QPushButton(self.frame_2)
        self.btn_takephoto.setObjectName(u"btn_takephoto")

        self.horizontalLayout_2.addWidget(self.btn_takephoto)

        self.pushButton = QPushButton(self.frame_2)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addWidget(self.frame_2)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 150))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label_template = QLabel(self.frame)
        self.label_template.setObjectName(u"label_template")
        self.label_template.setMinimumSize(QSize(350, 200))
        self.label_template.setMaximumSize(QSize(16777215, 300))

        self.verticalLayout.addWidget(self.label_template)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 10))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(50, 0))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.rbtn_move_rc = QRadioButton(self.frame_4)
        self.rbtn_move_rc.setObjectName(u"rbtn_move_rc")

        self.verticalLayout_3.addWidget(self.rbtn_move_rc)

        self.rbtn_move_single = QRadioButton(self.frame_4)
        self.rbtn_move_single.setObjectName(u"rbtn_move_single")
        self.rbtn_move_single.setMinimumSize(QSize(0, 0))
        self.rbtn_move_single.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_3.addWidget(self.rbtn_move_single)

        self.rbtn_move_fixed = QRadioButton(self.frame_4)
        self.rbtn_move_fixed.setObjectName(u"rbtn_move_fixed")

        self.verticalLayout_3.addWidget(self.rbtn_move_fixed)

        self.chk_autocap = QCheckBox(self.frame_4)
        self.chk_autocap.setObjectName(u"chk_autocap")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chk_autocap.sizePolicy().hasHeightForWidth())
        self.chk_autocap.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.chk_autocap)


        self.horizontalLayout_3.addWidget(self.frame_4)


        self.verticalLayout.addWidget(self.frame_3)


        self.horizontalLayout.addWidget(self.frame)

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
        self.label_source.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.btn_connect.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5Tello", None))
        self.btn_record.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5f55\u50cf", None))
        self.btn_takephoto.setText(QCoreApplication.translate("MainWindow", u"\u62cd\u7167", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u52a0\u8f7d\u56fe\u50cf\u5339\u914d", None))
        self.label_template.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.rbtn_move_rc.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u7eed\u63a7\u5236", None))
        self.rbtn_move_single.setText(QCoreApplication.translate("MainWindow", u"\u5355\u6b21\u63a7\u5236", None))
        self.rbtn_move_fixed.setText(QCoreApplication.translate("MainWindow", u"\u95f4\u6b47\u63a7\u5236", None))
        self.chk_autocap.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u62cd\u7167", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u83dc\u5355", None))
    # retranslateUi

