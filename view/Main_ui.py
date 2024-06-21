# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHeaderView, QLabel,
    QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QWidget)
import images.qresources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(783, 665)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(30, 20, 721, 621))
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.West)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget.setElideMode(Qt.TextElideMode.ElideNone)
        self.bomBrowserTab = QWidget()
        self.bomBrowserTab.setObjectName(u"bomBrowserTab")
        self.filterTextInput = QPlainTextEdit(self.bomBrowserTab)
        self.filterTextInput.setObjectName(u"filterTextInput")
        self.filterTextInput.setGeometry(QRect(430, 10, 141, 31))
        self.BOMtreeWidget = QTreeWidget(self.bomBrowserTab)
        self.BOMtreeWidget.headerItem().setText(0, "")
        self.BOMtreeWidget.headerItem().setText(1, "")
        self.BOMtreeWidget.setObjectName(u"BOMtreeWidget")
        self.BOMtreeWidget.setGeometry(QRect(10, 50, 671, 551))
        self.BOMtreeWidget.setAlternatingRowColors(True)
        self.BOMtreeWidget.setHeaderHidden(False)
        self.BOMtreeWidget.setColumnCount(6)
        self.BOMtreeWidget.header().setCascadingSectionResizes(True)
        self.label = QLabel(self.bomBrowserTab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 55, 16))
        self.projectComboBox = QComboBox(self.bomBrowserTab)
        self.projectComboBox.setObjectName(u"projectComboBox")
        self.projectComboBox.setGeometry(QRect(50, 10, 371, 21))
        self.filterClearButton = QPushButton(self.bomBrowserTab)
        self.filterClearButton.setObjectName(u"filterClearButton")
        self.filterClearButton.setGeometry(QRect(590, 10, 75, 24))
        self.tabWidget.addTab(self.bomBrowserTab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.widget = QWidget(self.tab_2)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(90, 110, 120, 80))
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.filterTextInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"filter", None))
        ___qtreewidgetitem = self.BOMtreeWidget.headerItem()
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("MainWindow", u"Filename", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("MainWindow", u"Part Name", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"Qty", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"Part #", None));
        self.label.setText(QCoreApplication.translate("MainWindow", u"Project", None))
        self.filterClearButton.setText(QCoreApplication.translate("MainWindow", u"clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bomBrowserTab), QCoreApplication.translate("MainWindow", u"BOM Browser", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
    # retranslateUi

