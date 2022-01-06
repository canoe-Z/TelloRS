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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGraphicsView, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLayout, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QRadioButton, QScrollBar,
    QSizePolicy, QSlider, QSpacerItem, QStackedWidget,
    QStatusBar, QTextBrowser, QToolBar, QVBoxLayout,
    QWidget)

from ui.ClickJumpSlider import ClickJumpSlider

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1093, 662)
        MainWindow.setFocusPolicy(Qt.StrongFocus)
        self.action_connect = QAction(MainWindow)
        self.action_connect.setObjectName(u"action_connect")
        self.action_takephoto = QAction(MainWindow)
        self.action_takephoto.setObjectName(u"action_takephoto")
        self.action_record = QAction(MainWindow)
        self.action_record.setObjectName(u"action_record")
        self.action_stoprecord = QAction(MainWindow)
        self.action_stoprecord.setObjectName(u"action_stoprecord")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_6 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.listWidget = QListWidget(self.centralwidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMinimumSize(QSize(150, 0))
        self.listWidget.setMaximumSize(QSize(150, 16777215))
        self.listWidget.setStyleSheet(u"QListWidget\n"
"{\n"
"    border:1px solid gray;   /*\u8fb9\u754c\u7ebf:\u5bbd\u5ea6\u3001\u989c\u8272*/\n"
"    /*background:gray;*/    /*\u8868\u683c\u80cc\u666f\u8272*/\n"
"    color:black;        /*\u524d\u666f\u8272\uff1a\u6587\u5b57\u989c\u8272*/\n"
"    /*margin:5px,5px,0px,50px;*/   /*\u4e0a\u3001\u4e0b\u3001\u5de6\u3001\u53f3\uff0c\u95f4\u8ddd*/\n"
"}\n"
"\n"
"QListWidget::item\n"
"{\n"
"    padding-top:48px;\n"
"    padding-bottom:48px;\n"
"}\n"
"\n"
"QListWidget::item:hover\n"
"{\n"
"    show-decoration-selected:5;\n"
"    background:skyblue;\n"
"}\n"
"\n"
"QListWidget::item:selected\n"
"{\n"
"    /*border:0px;*/\n"
"    background:lightgray;\n"
"    padding:0px;\n"
"    margin:0px;\n"
"    color:red;\n"
"}\n"
"\n"
"/*\u4e0a\u6b21\u9009\u62e9\u540e\u4fdd\u7559\u7684\u72b6\u6001\uff0c\u9f20\u6807\u79bb\u5f00\u540e\u663e\u793a*/\n"
"QListWidget::item:selected:!active\n"
"{\n"
"    border-width:0px;\n"
"    background:lightgreen;\n"
"}\n"
"\n"
"\n"
"/*QTableWidget*/\n"
"QTableWidget\n"
"{\n"
"    color"
                        ":green;    /*\u524d\u666f\u8272\uff1a\u6587\u5b57\u989c\u8272*/\n"
"    /*gridline-color:red;   */     /*\u8868\u683c\u4e2d\u7684\u7f51\u683c\u7ebf\u6761\u989c\u8272*/\n"
"    background:white;\n"
"    /*\u8bbe\u7f6e\u4ea4\u66ff\u989c\u8272\uff0c\u9700\u8981\u5728\u51fd\u6570\u5c5e\u6027\u4e2d\u8bbe\u7f6e:tableWidget->setAlternatingRowColors(true)*/\n"
"    /*alternate-background-color:red;   */\n"
"    selection-color:red;    /*\u9f20\u6807\u9009\u4e2d\u65f6\u524d\u666f\u8272\uff1a\u6587\u5b57\u989c\u8272*/\n"
"    selection-background-color:lightgray;   /*\u9f20\u6807\u9009\u4e2d\u65f6\u80cc\u666f\u8272*/\n"
"    border:1px solid gray;  /*\u8fb9\u6846\u7ebf\u7684\u5bbd\u5ea6\u3001\u989c\u8272*/\n"
"    /*border:none;*/    /*\u53bb\u9664\u8fb9\u754c\u7ebf*/\n"
"    /*border-radius:5px;*/\n"
"    /*padding:10px 10px;*/  /*\u8868\u683c\u4e0e\u8fb9\u6846\u7684\u95f4\u8ddd*/\n"
"}\n"
"\n"
"/*\u8bbe\u7f6e\u8868\u5934\u5c5e\u6027*/\n"
"QTableWidget QHeaderView::section\n"
"{\n"
"    background-color:#F0F0F0;  /*lig"
                        "htgray*/\n"
"    /*color:black;*/\n"
"    /*padding-left:4px;*/\n"
"    /*border:3px solid red;*/   /*\u8868\u5934\u8fb9\u6846\u7ebf\u7684\u5bbd\u5ea6\u3001\u989c\u8272*/\n"
"    /*border:1px solid gray;*/\n"
"}")

        self.horizontalLayout_6.addWidget(self.listWidget)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.horizontalLayout_4 = QHBoxLayout(self.page)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.frame = QFrame(self.page)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.label_template = QLabel(self.frame_2)
        self.label_template.setObjectName(u"label_template")
        self.label_template.setMinimumSize(QSize(480, 360))
        self.label_template.setMaximumSize(QSize(480, 360))
        self.label_template.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_template)

        self.verticalSpacer_2 = QSpacerItem(0, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.gb_det = QGroupBox(self.frame_5)
        self.gb_det.setObjectName(u"gb_det")
        self.gb_det.setMinimumSize(QSize(0, 100))
        self.gb_det.setMaximumSize(QSize(16777215, 16777215))
        self.gb_det.setCheckable(True)
        self.gridLayout_2 = QGridLayout(self.gb_det)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_4 = QLabel(self.gb_det)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)

        self.comboBox = QComboBox(self.gb_det)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMaximumSize(QSize(200, 16777215))

        self.gridLayout_2.addWidget(self.comboBox, 0, 1, 1, 1)

        self.label_3 = QLabel(self.gb_det)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.horizontalScrollBar = QScrollBar(self.gb_det)
        self.horizontalScrollBar.setObjectName(u"horizontalScrollBar")
        self.horizontalScrollBar.setMaximumSize(QSize(300, 16777215))
        self.horizontalScrollBar.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.horizontalScrollBar, 1, 1, 1, 1)


        self.horizontalLayout.addWidget(self.gb_det)

        self.gb_cls = QGroupBox(self.frame_5)
        self.gb_cls.setObjectName(u"gb_cls")
        self.gb_cls.setCheckable(True)
        self.gridLayout_3 = QGridLayout(self.gb_cls)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_5 = QLabel(self.gb_cls)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)

        self.label_6 = QLabel(self.gb_cls)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)

        self.comboBox_2 = QComboBox(self.gb_cls)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setMaximumSize(QSize(200, 16777215))

        self.gridLayout_3.addWidget(self.comboBox_2, 0, 1, 1, 1)

        self.label_cls_result = QLabel(self.gb_cls)
        self.label_cls_result.setObjectName(u"label_cls_result")

        self.gridLayout_3.addWidget(self.label_cls_result, 1, 1, 1, 1)


        self.horizontalLayout.addWidget(self.gb_cls)


        self.verticalLayout_2.addWidget(self.frame_5, 0, Qt.AlignBottom)


        self.horizontalLayout_2.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 150))
        self.frame_3.setMaximumSize(QSize(420, 16777215))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, -1, -1)
        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 300))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_12)

        self.label_source = QLabel(self.frame_4)
        self.label_source.setObjectName(u"label_source")
        self.label_source.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_source.sizePolicy().hasHeightForWidth())
        self.label_source.setSizePolicy(sizePolicy)
        self.label_source.setMinimumSize(QSize(350, 350))
        self.label_source.setMaximumSize(QSize(350, 350))
        self.label_source.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_source)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_8)

        self.frame_21 = QFrame(self.frame_4)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setMinimumSize(QSize(0, 100))
        self.verticalLayout_5 = QVBoxLayout(self.frame_21)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.rbtn_move_fixed = QRadioButton(self.frame_21)
        self.rbtn_move_fixed.setObjectName(u"rbtn_move_fixed")
        sizePolicy1 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.rbtn_move_fixed.sizePolicy().hasHeightForWidth())
        self.rbtn_move_fixed.setSizePolicy(sizePolicy1)

        self.verticalLayout_5.addWidget(self.rbtn_move_fixed)

        self.rbtn_move_single = QRadioButton(self.frame_21)
        self.rbtn_move_single.setObjectName(u"rbtn_move_single")
        sizePolicy1.setHeightForWidth(self.rbtn_move_single.sizePolicy().hasHeightForWidth())
        self.rbtn_move_single.setSizePolicy(sizePolicy1)

        self.verticalLayout_5.addWidget(self.rbtn_move_single)

        self.label_2 = QLabel(self.frame_21)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_5.addWidget(self.label_2)

        self.horizontalSlider_2 = ClickJumpSlider(self.frame_21)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)

        self.verticalLayout_5.addWidget(self.horizontalSlider_2)

        self.rbtn_move_rc = QRadioButton(self.frame_21)
        self.rbtn_move_rc.setObjectName(u"rbtn_move_rc")
        sizePolicy1.setHeightForWidth(self.rbtn_move_rc.sizePolicy().hasHeightForWidth())
        self.rbtn_move_rc.setSizePolicy(sizePolicy1)

        self.verticalLayout_5.addWidget(self.rbtn_move_rc)

        self.label_7 = QLabel(self.frame_21)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_5.addWidget(self.label_7)

        self.horizontalSlider_5 = ClickJumpSlider(self.frame_21)
        self.horizontalSlider_5.setObjectName(u"horizontalSlider_5")
        self.horizontalSlider_5.setOrientation(Qt.Horizontal)

        self.verticalLayout_5.addWidget(self.horizontalSlider_5)


        self.verticalLayout_7.addWidget(self.frame_21)


        self.verticalLayout.addWidget(self.frame_4)


        self.horizontalLayout_2.addWidget(self.frame_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_4.addWidget(self.frame)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.horizontalLayout_3 = QHBoxLayout(self.page_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_6 = QSpacerItem(37, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.frame_9 = QFrame(self.page_2)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_9)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer_13)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer_9)

        self.label_template_3 = QLabel(self.frame_9)
        self.label_template_3.setObjectName(u"label_template_3")
        self.label_template_3.setMinimumSize(QSize(400, 400))
        self.label_template_3.setMaximumSize(QSize(16777215, 16777215))
        self.label_template_3.setCursor(QCursor(Qt.CrossCursor))
        self.label_template_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_12.addWidget(self.label_template_3)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer_6)

        self.frame_17 = QFrame(self.frame_9)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setMinimumSize(QSize(0, 100))
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.groupBox_3 = QGroupBox(self.frame_17)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(30, 10, 161, 91))
        self.textBrowser = QTextBrowser(self.groupBox_3)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(20, 20, 121, 61))
        self.groupBox_4 = QGroupBox(self.frame_17)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(260, 10, 161, 91))
        self.textBrowser_2 = QTextBrowser(self.groupBox_4)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        self.textBrowser_2.setGeometry(QRect(20, 20, 121, 61))

        self.verticalLayout_12.addWidget(self.frame_17)


        self.horizontalLayout_3.addWidget(self.frame_9)

        self.frame_11 = QFrame(self.page_2)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 150))
        self.frame_11.setMaximumSize(QSize(420, 16777215))
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_11)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, -1, -1)
        self.verticalSpacer_14 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_14)

        self.frame_12 = QFrame(self.frame_11)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(0, 300))
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_12)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.label_source_3 = QLabel(self.frame_12)
        self.label_source_3.setObjectName(u"label_source_3")
        self.label_source_3.setEnabled(True)
        sizePolicy.setHeightForWidth(self.label_source_3.sizePolicy().hasHeightForWidth())
        self.label_source_3.setSizePolicy(sizePolicy)
        self.label_source_3.setMinimumSize(QSize(300, 250))
        self.label_source_3.setMaximumSize(QSize(350, 290))
        self.label_source_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_14.addWidget(self.label_source_3)

        self.verticalSpacer_4 = QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_4)

        self.frame_13 = QFrame(self.frame_12)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(0, 150))
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.pushButton = QPushButton(self.frame_13)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(40, 60, 111, 41))
        self.pushButton_2 = QPushButton(self.frame_13)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(210, 60, 101, 41))

        self.verticalLayout_14.addWidget(self.frame_13)


        self.verticalLayout_13.addWidget(self.frame_12)


        self.horizontalLayout_3.addWidget(self.frame_11)

        self.horizontalSpacer_8 = QSpacerItem(37, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_8)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.horizontalLayout_7 = QHBoxLayout(self.page_3)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.frame_6 = QFrame(self.page_3)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.label_template_2 = QLabel(self.frame_6)
        self.label_template_2.setObjectName(u"label_template_2")
        self.label_template_2.setMinimumSize(QSize(480, 360))
        self.label_template_2.setMaximumSize(QSize(480, 360))
        self.label_template_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_template_2)

        self.frame_8 = QFrame(self.frame_6)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(0, 150))
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_8)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.radioButton_2 = QRadioButton(self.frame_8)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout_6.addWidget(self.radioButton_2, 0, Qt.AlignHCenter)

        self.groupBox_10 = QGroupBox(self.frame_8)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setMinimumSize(QSize(0, 120))
        self.formLayout_2 = QFormLayout(self.groupBox_10)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.formLayout_2.setRowWrapPolicy(QFormLayout.WrapLongRows)
        self.formLayout_2.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayout_2.setHorizontalSpacing(1)
        self.formLayout_2.setVerticalSpacing(7)
        self.formLayout_2.setContentsMargins(9, -1, -1, 4)
        self.radioButton_4 = QRadioButton(self.groupBox_10)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.radioButton_4)

        self.radioButton_5 = QRadioButton(self.groupBox_10)
        self.radioButton_5.setObjectName(u"radioButton_5")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.radioButton_5)

        self.label_11 = QLabel(self.groupBox_10)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_11)

        self.horizontalSlider_3 = QSlider(self.groupBox_10)
        self.horizontalSlider_3.setObjectName(u"horizontalSlider_3")
        self.horizontalSlider_3.setOrientation(Qt.Horizontal)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.horizontalSlider_3)

        self.radioButton_6 = QRadioButton(self.groupBox_10)
        self.radioButton_6.setObjectName(u"radioButton_6")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.radioButton_6)

        self.label_12 = QLabel(self.groupBox_10)
        self.label_12.setObjectName(u"label_12")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_12)

        self.horizontalSlider_4 = QSlider(self.groupBox_10)
        self.horizontalSlider_4.setObjectName(u"horizontalSlider_4")
        self.horizontalSlider_4.setMinimumSize(QSize(0, 0))
        self.horizontalSlider_4.setOrientation(Qt.Horizontal)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.horizontalSlider_4)


        self.verticalLayout_6.addWidget(self.groupBox_10)


        self.verticalLayout_3.addWidget(self.frame_8)

        self.frame_7 = QFrame(self.frame_6)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)

        self.verticalLayout_3.addWidget(self.frame_7)


        self.horizontalLayout_7.addWidget(self.frame_6, 0, Qt.AlignHCenter)

        self.horizontalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_4 = QVBoxLayout(self.page_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.graphicsView = QGraphicsView(self.page_4)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout_4.addWidget(self.graphicsView)

        self.stackedWidget.addWidget(self.page_4)

        self.horizontalLayout_6.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.action_connect)
        self.toolBar.addAction(self.action_takephoto)
        self.toolBar.addAction(self.action_record)
        self.toolBar.addAction(self.action_stoprecord)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"TelloRS", None))
        self.action_connect.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5", None))
#if QT_CONFIG(tooltip)
        self.action_connect.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:16pt; font-weight:700;\">\u8fde\u63a5</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.action_takephoto.setText(QCoreApplication.translate("MainWindow", u"\u62cd\u7167", None))
        self.action_record.setText(QCoreApplication.translate("MainWindow", u"\u5f55\u50cf", None))
        self.action_stoprecord.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62\u5f55\u50cf", None))
#if QT_CONFIG(tooltip)
        self.action_stoprecord.setToolTip(QCoreApplication.translate("MainWindow", u"\u505c\u6b62\u5f55\u50cf", None))
#endif // QT_CONFIG(tooltip)

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u9065\u63a7\u5bfc\u822a", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u5de1\u68c0", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u76ee\u6807\u8ddf\u8e2a", None));
        ___qlistwidgetitem3 = self.listWidget.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u79bb\u7ebf\u68c0\u6d4b", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.label_template.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.gb_det.setTitle(QCoreApplication.translate("MainWindow", u"\u5b9e\u65f6\u68c0\u6d4b", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u68c0\u6d4b\u5668", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"NanoDet", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"YOLOv5", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"\u6a21\u677f\u5339\u914d", None))

        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u9608\u503c", None))
        self.gb_cls.setTitle(QCoreApplication.translate("MainWindow", u"\u5b9e\u65f6\u573a\u666f\u5206\u7c7b", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u5206\u7c7b\u5668", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u5206\u7c7b\u7ed3\u679c", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"ResNet18", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"YOLOv5", None))

        self.label_cls_result.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_source.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.rbtn_move_fixed.setText(QCoreApplication.translate("MainWindow", u"\u95f4\u9694\u63a7\u5236", None))
        self.rbtn_move_single.setText(QCoreApplication.translate("MainWindow", u"\u5355\u6b65\u63a7\u5236", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6b65\u957f", None))
        self.rbtn_move_rc.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u7eed\u63a7\u5236", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u901f", None))
        self.label_template_3.setText(QCoreApplication.translate("MainWindow", u"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"1111111111111111111111111111111"
                        "11111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"111111111111111111111111111111111111111111111111111111111111111111\n"
"11111111111111111111111111111111111111111111111111111111111111"
                        "1111\n"
"", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\uff1f\uff1f\uff1f\u68c0\u6d4b\u6570\u91cf", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\uff1f\uff1f\uff1f\u68c0\u6d4b\u6570\u91cf", None))
        self.label_source_3.setText(QCoreApplication.translate("MainWindow", u"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222"
                        "222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"222222222222222222222222222222222222222222222222\n"
"", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_template_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u6355\u6349\u76ee\u6807", None))
        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", u"\u95f4\u9694\u63a7\u5236", None))
        self.radioButton_5.setText(QCoreApplication.translate("MainWindow", u"\u5355\u6b65\u63a7\u5236", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u6b65\u957f", None))
        self.radioButton_6.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u7eed\u63a7\u5236", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u8f6c\u901f", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

