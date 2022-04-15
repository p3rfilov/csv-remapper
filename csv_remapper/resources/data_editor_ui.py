# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_editor_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DataEditor(object):
    def setupUi(self, DataEditor):
        if not DataEditor.objectName():
            DataEditor.setObjectName(u"DataEditor")
        DataEditor.setWindowModality(Qt.ApplicationModal)
        DataEditor.resize(1218, 471)
        self.verticalLayout = QVBoxLayout(DataEditor)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.grp_name = QGroupBox(DataEditor)
        self.grp_name.setObjectName(u"grp_name")
        self.grp_name.setAutoFillBackground(False)
        self.grp_name.setStyleSheet(u"QGroupBox#grp_name{border: 1px solid grey; margin-top: 7px}\n"
"QGroupBox::title { subcontrol-origin: margin; left: 7px; padding: 0px 3px 0px 3px;}")
        self.grp_name.setFlat(False)
        self.grp_name.setCheckable(False)
        self.verticalLayout_3 = QVBoxLayout(self.grp_name)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tbl_data = QTableView(self.grp_name)
        self.tbl_data.setObjectName(u"tbl_data")
        self.tbl_data.setAlternatingRowColors(True)
        self.tbl_data.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_data.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tbl_data.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tbl_data.setCornerButtonEnabled(True)
        self.tbl_data.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_3.addWidget(self.tbl_data)


        self.verticalLayout.addWidget(self.grp_name)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.grp_alias_settings = QGroupBox(DataEditor)
        self.grp_alias_settings.setObjectName(u"grp_alias_settings")
        self.horizontalLayout_2 = QHBoxLayout(self.grp_alias_settings)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.grp_alias_settings)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.cbx_lookup_mode = QComboBox(self.grp_alias_settings)
        self.cbx_lookup_mode.setObjectName(u"cbx_lookup_mode")

        self.horizontalLayout_2.addWidget(self.cbx_lookup_mode)

        self.btn_copy_column = QPushButton(self.grp_alias_settings)
        self.btn_copy_column.setObjectName(u"btn_copy_column")

        self.horizontalLayout_2.addWidget(self.btn_copy_column)

        self.lab_tooltip = QLabel(self.grp_alias_settings)
        self.lab_tooltip.setObjectName(u"lab_tooltip")
        self.lab_tooltip.setEnabled(False)
        self.lab_tooltip.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.lab_tooltip)


        self.horizontalLayout.addWidget(self.grp_alias_settings)

        self.grp_alias_data = QGroupBox(DataEditor)
        self.grp_alias_data.setObjectName(u"grp_alias_data")
        self.horizontalLayout_4 = QHBoxLayout(self.grp_alias_data)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")

        self.horizontalLayout.addWidget(self.grp_alias_data)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.grp_data_editor = QGroupBox(DataEditor)
        self.grp_data_editor.setObjectName(u"grp_data_editor")
        self.verticalLayout_2 = QVBoxLayout(self.grp_data_editor)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, 0, -1)
        self.btn_update = QPushButton(self.grp_data_editor)
        self.btn_update.setObjectName(u"btn_update")

        self.horizontalLayout_3.addWidget(self.btn_update)

        self.btn_export = QPushButton(self.grp_data_editor)
        self.btn_export.setObjectName(u"btn_export")

        self.horizontalLayout_3.addWidget(self.btn_export)

        self.btn_save = QPushButton(self.grp_data_editor)
        self.btn_save.setObjectName(u"btn_save")

        self.horizontalLayout_3.addWidget(self.btn_save)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.horizontalLayout.addWidget(self.grp_data_editor)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(DataEditor)

        QMetaObject.connectSlotsByName(DataEditor)
    # setupUi

    def retranslateUi(self, DataEditor):
        DataEditor.setWindowTitle(QCoreApplication.translate("DataEditor", u"Form", None))
        self.grp_name.setTitle(QCoreApplication.translate("DataEditor", u"<name>", None))
        self.grp_alias_settings.setTitle(QCoreApplication.translate("DataEditor", u"Alias Settings", None))
        self.label_3.setText(QCoreApplication.translate("DataEditor", u"Lookup Mode", None))
        self.btn_copy_column.setText(QCoreApplication.translate("DataEditor", u" Copy Values... ", None))
        self.lab_tooltip.setText(QCoreApplication.translate("DataEditor", u"Use ^ character (without spaces) to separate Alias Data values", None))
        self.grp_alias_data.setTitle(QCoreApplication.translate("DataEditor", u"Alias Data", None))
        self.grp_data_editor.setTitle(QCoreApplication.translate("DataEditor", u"Editing Options", None))
        self.btn_update.setText(QCoreApplication.translate("DataEditor", u" Update from CSV... ", None))
        self.btn_export.setText(QCoreApplication.translate("DataEditor", u" Save File As... ", None))
        self.btn_save.setText(QCoreApplication.translate("DataEditor", u" Save Changes ", None))
    # retranslateUi

