# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow_bak.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGraphicsView, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QRadioButton, QScrollBar, QSizePolicy,
    QSlider, QSpacerItem, QStackedWidget, QStatusBar,
    QToolBar, QVBoxLayout, QWidget)

from ui.ClickJumpSlider import ClickJumpSlider

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1114, 643)
        MainWindow.setFocusPolicy(Qt.StrongFocus)
        self.action_connect = QAction(MainWindow)
        self.action_connect.setObjectName(u"action_connect")
        self.action_takephoto = QAction(MainWindow)
        self.action_takephoto.setObjectName(u"action_takephoto")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
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

        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.horizontalLayout_4 = QHBoxLayout(self.page)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.frame_2 = QFrame(self.page)
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

        self.verticalLayout_2.addWidget(self.label_template, 0, Qt.AlignVCenter)

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


        self.horizontalLayout.addWidget(self.gb_cls)


        self.verticalLayout_2.addWidget(self.frame_5, 0, Qt.AlignBottom)


        self.horizontalLayout_4.addWidget(self.frame_2)

        self.frame = QFrame(self.page)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 150))
        self.frame.setMaximumSize(QSize(420, 16777215))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, -1, -1)
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 300))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_source = QLabel(self.frame_3)
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

        self.groupBox_2 = QGroupBox(self.frame_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(0, 100))
        self.groupBox_2.setCheckable(True)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.radioButton_2 = QRadioButton(self.groupBox_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout_5.addWidget(self.radioButton_2)

        self.chk_autocap = QCheckBox(self.groupBox_2)
        self.chk_autocap.setObjectName(u"chk_autocap")
        sizePolicy1 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.chk_autocap.sizePolicy().hasHeightForWidth())
        self.chk_autocap.setSizePolicy(sizePolicy1)

        self.verticalLayout_5.addWidget(self.chk_autocap)

        self.radioButton_3 = QRadioButton(self.groupBox_2)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.verticalLayout_5.addWidget(self.radioButton_3)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_5.addWidget(self.label_2)

        self.horizontalSlider_2 = QSlider(self.groupBox_2)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)

        self.verticalLayout_5.addWidget(self.horizontalSlider_2)


        self.verticalLayout_7.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.frame_3)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 100))
        self.groupBox.setCheckable(True)
        self.groupBox.setChecked(False)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout_4.addWidget(self.radioButton)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.frame_4 = QFrame(self.groupBox)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 50))
        self.frame_4.setMaximumSize(QSize(200, 16777215))
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
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


        self.verticalLayout_4.addWidget(self.frame_4)

        self.horizontalSlider = ClickJumpSlider(self.groupBox)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.verticalLayout_4.addWidget(self.horizontalSlider)


        self.verticalLayout_7.addWidget(self.groupBox)


        self.verticalLayout.addWidget(self.frame_3)


        self.horizontalLayout_4.addWidget(self.frame)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.pushButton = QPushButton(self.page_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(410, 220, 75, 24))
        self.pushButton_2 = QPushButton(self.page_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(500, 220, 75, 24))
        self.pushButton_3 = QPushButton(self.page_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(350, 470, 75, 24))
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.graphicsView = QGraphicsView(self.page_4)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(60, 0, 841, 561))
        self.stackedWidget.addWidget(self.page_4)

        self.gridLayout.addWidget(self.stackedWidget, 0, 1, 1, 1)

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

        self.label_source.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u95f4\u9694\u63a7\u5236", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u7eed\u63a7\u5236", None))
        self.chk_autocap.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u62cd\u7167", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"\u95f4\u6b47\u63a7\u5236", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8fde\u7eed\u63a7\u5236", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.rbtn_move_rc.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u7eed\u63a7\u5236", None))
        self.rbtn_move_single.setText(QCoreApplication.translate("MainWindow", u"\u5355\u6b21\u63a7\u5236", None))
        self.rbtn_move_fixed.setText(QCoreApplication.translate("MainWindow", u"\u95f4\u6b47\u63a7\u5236", None))
#if QT_CONFIG(tooltip)
        self.horizontalSlider.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

