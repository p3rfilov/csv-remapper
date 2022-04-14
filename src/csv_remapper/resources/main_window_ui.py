# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from csv_remapper.widgets.drag_drop_table import DragDropTable


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(792, 326)
        self.action_edit_templates = QAction(MainWindow)
        self.action_edit_templates.setObjectName(u"action_edit_templates")
        self.action_options = QAction(MainWindow)
        self.action_options.setObjectName(u"action_options")
        self.action_new_input = QAction(MainWindow)
        self.action_new_input.setObjectName(u"action_new_input")
        self.action_new_output = QAction(MainWindow)
        self.action_new_output.setObjectName(u"action_new_output")
        self.action_change_directory = QAction(MainWindow)
        self.action_change_directory.setObjectName(u"action_change_directory")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tbl_items = DragDropTable(self.centralwidget)
        if (self.tbl_items.columnCount() < 1):
            self.tbl_items.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.tbl_items.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.tbl_items.setObjectName(u"tbl_items")
        self.tbl_items.setEnabled(True)
        self.tbl_items.setMouseTracking(False)
        self.tbl_items.setAcceptDrops(True)
        self.tbl_items.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_3.addWidget(self.tbl_items)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btn_browse = QPushButton(self.centralwidget)
        self.btn_browse.setObjectName(u"btn_browse")

        self.horizontalLayout_2.addWidget(self.btn_browse)

        self.btn_remove = QPushButton(self.centralwidget)
        self.btn_remove.setObjectName(u"btn_remove")

        self.horizontalLayout_2.addWidget(self.btn_remove)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_3.addWidget(self.line_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.cbx_template = QComboBox(self.centralwidget)
        self.cbx_template.setObjectName(u"cbx_template")

        self.verticalLayout.addWidget(self.cbx_template)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btn_preview = QPushButton(self.centralwidget)
        self.btn_preview.setObjectName(u"btn_preview")

        self.verticalLayout.addWidget(self.btn_preview)

        self.btn_remap = QPushButton(self.centralwidget)
        self.btn_remap.setObjectName(u"btn_remap")
        self.btn_remap.setMinimumSize(QSize(110, 50))

        self.verticalLayout.addWidget(self.btn_remap)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 792, 21))
        self.menu_edit = QMenu(self.menubar)
        self.menu_edit.setObjectName(u"menu_edit")
        self.menu_new_template = QMenu(self.menu_edit)
        self.menu_new_template.setObjectName(u"menu_new_template")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_edit.menuAction())
        self.menu_edit.addAction(self.menu_new_template.menuAction())
        self.menu_edit.addAction(self.action_edit_templates)
        self.menu_edit.addAction(self.action_change_directory)
        self.menu_new_template.addAction(self.action_new_input)
        self.menu_new_template.addAction(self.action_new_output)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CSV File Remapper", None))
        self.action_edit_templates.setText(QCoreApplication.translate("MainWindow", u"Edit Templates", None))
        self.action_options.setText(QCoreApplication.translate("MainWindow", u"Options", None))
        self.action_new_input.setText(QCoreApplication.translate("MainWindow", u"Input", None))
        self.action_new_output.setText(QCoreApplication.translate("MainWindow", u"Output", None))
        self.action_change_directory.setText(QCoreApplication.translate("MainWindow", u"Change Template Directory...", None))
        ___qtablewidgetitem = self.tbl_items.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Files", None));
#if QT_CONFIG(tooltip)
        self.tbl_items.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.tbl_items.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.label.setText(QCoreApplication.translate("MainWindow", u"TIP: Double-click to Edit / View", None))
        self.btn_browse.setText(QCoreApplication.translate("MainWindow", u"Browse..", None))
        self.btn_remove.setText(QCoreApplication.translate("MainWindow", u" Remove Selected ", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Output Template", None))
        self.btn_preview.setText(QCoreApplication.translate("MainWindow", u"Preview Selected", None))
        self.btn_remap.setText(QCoreApplication.translate("MainWindow", u"Remap All", None))
        self.menu_edit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menu_new_template.setTitle(QCoreApplication.translate("MainWindow", u"New Template...", None))
    # retranslateUi

