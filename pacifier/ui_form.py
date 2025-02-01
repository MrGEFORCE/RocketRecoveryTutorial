# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QSlider, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(650, 450)
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(12)
        Widget.setFont(font)
        self.verticalLayoutWidget = QWidget(Widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 20, 421, 411))
        self.verticalLayout_orienMainGraph = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_orienMainGraph.setObjectName(u"verticalLayout_orienMainGraph")
        self.verticalLayout_orienMainGraph.setContentsMargins(0, 0, 0, 0)
        self.pushButton_start = QPushButton(Widget)
        self.pushButton_start.setObjectName(u"pushButton_start")
        self.pushButton_start.setGeometry(QRect(460, 20, 80, 30))
        self.pushButton_stop = QPushButton(Widget)
        self.pushButton_stop.setObjectName(u"pushButton_stop")
        self.pushButton_stop.setGeometry(QRect(550, 20, 80, 30))
        self.label_upVec = QLabel(Widget)
        self.label_upVec.setObjectName(u"label_upVec")
        self.label_upVec.setGeometry(QRect(462, 62, 111, 30))
        self.label_height = QLabel(Widget)
        self.label_height.setObjectName(u"label_height")
        self.label_height.setGeometry(QRect(460, 170, 171, 30))
        self.horizontalSlider_height = QSlider(Widget)
        self.horizontalSlider_height.setObjectName(u"horizontalSlider_height")
        self.horizontalSlider_height.setGeometry(QRect(460, 200, 160, 16))
        self.horizontalSlider_height.setValue(20)
        self.horizontalSlider_height.setOrientation(Qt.Horizontal)
        self.label_upVec_value = QLabel(Widget)
        self.label_upVec_value.setObjectName(u"label_upVec_value")
        self.label_upVec_value.setGeometry(QRect(460, 90, 141, 30))
        self.label_height_value = QLabel(Widget)
        self.label_height_value.setObjectName(u"label_height_value")
        self.label_height_value.setGeometry(QRect(460, 220, 161, 30))
        self.label_heading = QLabel(Widget)
        self.label_heading.setObjectName(u"label_heading")
        self.label_heading.setGeometry(QRect(460, 250, 171, 30))
        self.pushButton_stopVessel = QPushButton(Widget)
        self.pushButton_stopVessel.setObjectName(u"pushButton_stopVessel")
        self.pushButton_stopVessel.setGeometry(QRect(460, 400, 151, 30))
        self.label_moveControl = QLabel(Widget)
        self.label_moveControl.setObjectName(u"label_moveControl")
        self.label_moveControl.setGeometry(QRect(470, 330, 131, 30))
        self.label_moveControl.setAlignment(Qt.AlignCenter)
        self.pushButton_forward = QPushButton(Widget)
        self.pushButton_forward.setObjectName(u"pushButton_forward")
        self.pushButton_forward.setGeometry(QRect(460, 360, 71, 30))
        self.pushButton_back = QPushButton(Widget)
        self.pushButton_back.setObjectName(u"pushButton_back")
        self.pushButton_back.setGeometry(QRect(540, 360, 71, 30))
        self.horizontalSlider_heading = QSlider(Widget)
        self.horizontalSlider_heading.setObjectName(u"horizontalSlider_heading")
        self.horizontalSlider_heading.setGeometry(QRect(460, 280, 160, 16))
        self.horizontalSlider_heading.setOrientation(Qt.Horizontal)
        self.label_heading_value = QLabel(Widget)
        self.label_heading_value.setObjectName(u"label_heading_value")
        self.label_heading_value.setGeometry(QRect(460, 300, 161, 30))
        self.label_currentMode = QLabel(Widget)
        self.label_currentMode.setObjectName(u"label_currentMode")
        self.label_currentMode.setGeometry(QRect(460, 130, 161, 30))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.pushButton_start.setText(QCoreApplication.translate("Widget", u"start", None))
        self.pushButton_stop.setText(QCoreApplication.translate("Widget", u"stop", None))
        self.label_upVec.setText(QCoreApplication.translate("Widget", u"up vector", None))
        self.label_height.setText(QCoreApplication.translate("Widget", u"height set (0 - 200)", None))
        self.label_upVec_value.setText(QCoreApplication.translate("Widget", u"[0,0,0]", None))
        self.label_height_value.setText(QCoreApplication.translate("Widget", u"current target:", None))
        self.label_heading.setText(QCoreApplication.translate("Widget", u"heading set (0 - 360)", None))
        self.pushButton_stopVessel.setText(QCoreApplication.translate("Widget", u"stop vessel", None))
        self.label_moveControl.setText(QCoreApplication.translate("Widget", u"move control", None))
        self.pushButton_forward.setText(QCoreApplication.translate("Widget", u"forward", None))
        self.pushButton_back.setText(QCoreApplication.translate("Widget", u"back", None))
        self.label_heading_value.setText(QCoreApplication.translate("Widget", u"current heading:", None))
        self.label_currentMode.setText(QCoreApplication.translate("Widget", u"current mode:", None))
    # retranslateUi

