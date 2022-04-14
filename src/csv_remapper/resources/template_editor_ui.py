# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'template_editor_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_TemplateEditor(object):
    def setupUi(self, TemplateEditor):
        if not TemplateEditor.objectName():
            TemplateEditor.setObjectName(u"TemplateEditor")
        TemplateEditor.setWindowModality(Qt.ApplicationModal)
        TemplateEditor.resize(1069, 792)
        self.verticalLayout_6 = QVBoxLayout(TemplateEditor)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.grp_templates = QGroupBox(TemplateEditor)
        self.grp_templates.setObjectName(u"grp_templates")
        self.grp_templates.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout = QVBoxLayout(self.grp_templates)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.btn_delete_template = QPushButton(self.grp_templates)
        self.btn_delete_template.setObjectName(u"btn_delete_template")

        self.horizontalLayout_4.addWidget(self.btn_delete_template)

        self.btn_new_template = QPushButton(self.grp_templates)
        self.btn_new_template.setObjectName(u"btn_new_template")

        self.horizontalLayout_4.addWidget(self.btn_new_template)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.tre_browse_templates = QTreeView(self.grp_templates)
        self.tre_browse_templates.setObjectName(u"tre_browse_templates")
        self.tre_browse_templates.setAnimated(True)
        self.tre_browse_templates.setAllColumnsShowFocus(False)
        self.tre_browse_templates.setHeaderHidden(True)

        self.verticalLayout.addWidget(self.tre_browse_templates)


        self.horizontalLayout_2.addWidget(self.grp_templates)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.grp_template_veiws = QGroupBox(TemplateEditor)
        self.grp_template_veiws.setObjectName(u"grp_template_veiws")
        self.verticalLayout_3 = QVBoxLayout(self.grp_template_veiws)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")

        self.verticalLayout_4.addWidget(self.grp_template_veiws)

        self.line_2 = QFrame(TemplateEditor)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.grp_aliases = QGroupBox(TemplateEditor)
        self.grp_aliases.setObjectName(u"grp_aliases")
        self.grp_aliases.setEnabled(True)
        self.verticalLayout_5 = QVBoxLayout(self.grp_aliases)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tab_aliases = QTabWidget(self.grp_aliases)
        self.tab_aliases.setObjectName(u"tab_aliases")
        self.tab_aliases.setEnabled(True)
        self.tab_aliases.setTabPosition(QTabWidget.North)
        self.tab_aliases.setTabShape(QTabWidget.Rounded)
        self.tab_aliases.setUsesScrollButtons(True)
        self.tab_aliases.setDocumentMode(False)
        self.tab_aliases.setTabsClosable(False)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab_aliases.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tab_aliases.addTab(self.tab_2, "")

        self.verticalLayout_5.addWidget(self.tab_aliases)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.btn_new_alias = QPushButton(self.grp_aliases)
        self.btn_new_alias.setObjectName(u"btn_new_alias")

        self.horizontalLayout_3.addWidget(self.btn_new_alias)

        self.btn_new_alias_from_csv = QPushButton(self.grp_aliases)
        self.btn_new_alias_from_csv.setObjectName(u"btn_new_alias_from_csv")

        self.horizontalLayout_3.addWidget(self.btn_new_alias_from_csv)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)


        self.verticalLayout_4.addWidget(self.grp_aliases)

        self.line_3 = QFrame(TemplateEditor)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_3)

        self.grp_mappings = QGroupBox(TemplateEditor)
        self.grp_mappings.setObjectName(u"grp_mappings")
        self.grp_mappings.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.grp_mappings)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tbl_mappings = QTableView(self.grp_mappings)
        self.tbl_mappings.setObjectName(u"tbl_mappings")
        self.tbl_mappings.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbl_mappings.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbl_mappings.horizontalHeader().setStretchLastSection(False)

        self.verticalLayout_2.addWidget(self.tbl_mappings)


        self.verticalLayout_4.addWidget(self.grp_mappings)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.line = QFrame(TemplateEditor)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_6.addWidget(self.line)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(TemplateEditor)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_save = QPushButton(TemplateEditor)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setMinimumSize(QSize(120, 40))

        self.horizontalLayout.addWidget(self.btn_save)


        self.verticalLayout_6.addLayout(self.horizontalLayout)


        self.retranslateUi(TemplateEditor)

        self.tab_aliases.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TemplateEditor)
    # setupUi

    def retranslateUi(self, TemplateEditor):
        TemplateEditor.setWindowTitle(QCoreApplication.translate("TemplateEditor", u"Form", None))
        self.grp_templates.setTitle(QCoreApplication.translate("TemplateEditor", u"Templates", None))
        self.btn_delete_template.setText(QCoreApplication.translate("TemplateEditor", u"Delete", None))
        self.btn_new_template.setText(QCoreApplication.translate("TemplateEditor", u"New..", None))
        self.grp_template_veiws.setTitle(QCoreApplication.translate("TemplateEditor", u"Template Views", None))
        self.grp_aliases.setTitle(QCoreApplication.translate("TemplateEditor", u"Alias Data", None))
        self.tab_aliases.setTabText(self.tab_aliases.indexOf(self.tab), QCoreApplication.translate("TemplateEditor", u"Clients", None))
        self.tab_aliases.setTabText(self.tab_aliases.indexOf(self.tab_2), QCoreApplication.translate("TemplateEditor", u"Suppliers", None))
        self.btn_new_alias.setText(QCoreApplication.translate("TemplateEditor", u"New", None))
        self.btn_new_alias_from_csv.setText(QCoreApplication.translate("TemplateEditor", u" New from CSV... ", None))
        self.grp_mappings.setTitle(QCoreApplication.translate("TemplateEditor", u"Mappings", None))
        self.label.setText(QCoreApplication.translate("TemplateEditor", u"TIPS: 1. Drag and Drop table headers to make Mappings  2. Right-Click & Double-Click items to Edit them", None))
        self.btn_save.setText(QCoreApplication.translate("TemplateEditor", u"Save", None))
    # retranslateUi

