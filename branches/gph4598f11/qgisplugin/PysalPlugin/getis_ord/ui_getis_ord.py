# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_getis_ord.ui'
#
# Created: Tue Dec 06 01:52:41 2011
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_getis_ord(object):
    def setupUi(self, getis_ord):
        getis_ord.setObjectName(_fromUtf8("getis_ord"))
        getis_ord.resize(405, 439)
        getis_ord.setWindowTitle(QtGui.QApplication.translate("getis_ord", "getis_ord", None, QtGui.QApplication.UnicodeUTF8))
        self.OutputButton = QtGui.QPushButton(getis_ord)
        self.OutputButton.setGeometry(QtCore.QRect(320, 350, 51, 19))
        self.OutputButton.setText(QtGui.QApplication.translate("getis_ord", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.OutputButton.setObjectName(_fromUtf8("OutputButton"))
        self.OuputTextLine = QtGui.QLineEdit(getis_ord)
        self.OuputTextLine.setGeometry(QtCore.QRect(20, 350, 281, 20))
        self.OuputTextLine.setObjectName(_fromUtf8("OuputTextLine"))
        self.label = QtGui.QLabel(getis_ord)
        self.label.setGeometry(QtCore.QRect(20, 330, 53, 17))
        self.label.setText(QtGui.QApplication.translate("getis_ord", "Output File", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(getis_ord)
        self.label_2.setGeometry(QtCore.QRect(160, 10, 111, 16))
        self.label_2.setText(QtGui.QApplication.translate("getis_ord", "Input File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.InputWeightsTextLine = QtGui.QLineEdit(getis_ord)
        self.InputWeightsTextLine.setGeometry(QtCore.QRect(20, 180, 251, 20))
        self.InputWeightsTextLine.setObjectName(_fromUtf8("InputWeightsTextLine"))
        self.label_3 = QtGui.QLabel(getis_ord)
        self.label_3.setGeometry(QtCore.QRect(20, 150, 121, 16))
        self.label_3.setText(QtGui.QApplication.translate("getis_ord", "Iput Spatial Weights", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.selectcombobox = QtGui.QComboBox(getis_ord)
        self.selectcombobox.setGeometry(QtCore.QRect(110, 60, 251, 22))
        self.selectcombobox.setObjectName(_fromUtf8("selectcombobox"))
        self.label_4 = QtGui.QLabel(getis_ord)
        self.label_4.setGeometry(QtCore.QRect(30, 60, 111, 16))
        self.label_4.setText(QtGui.QApplication.translate("getis_ord", "Input Column", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.ThreshDistLine = QtGui.QLineEdit(getis_ord)
        self.ThreshDistLine.setGeometry(QtCore.QRect(20, 250, 81, 20))
        self.ThreshDistLine.setObjectName(_fromUtf8("ThreshDistLine"))
        self.label_5 = QtGui.QLabel(getis_ord)
        self.label_5.setGeometry(QtCore.QRect(20, 230, 111, 20))
        self.label_5.setText(QtGui.QApplication.translate("getis_ord", "Threshold Distance", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.InputWeightsButton = QtGui.QPushButton(getis_ord)
        self.InputWeightsButton.setGeometry(QtCore.QRect(280, 180, 51, 19))
        self.InputWeightsButton.setText(QtGui.QApplication.translate("getis_ord", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.InputWeightsButton.setObjectName(_fromUtf8("InputWeightsButton"))
        self.CreateWeightsButton = QtGui.QPushButton(getis_ord)
        self.CreateWeightsButton.setGeometry(QtCore.QRect(280, 210, 91, 23))
        self.CreateWeightsButton.setText(QtGui.QApplication.translate("getis_ord", "Create Weights", None, QtGui.QApplication.UnicodeUTF8))
        self.CreateWeightsButton.setObjectName(_fromUtf8("CreateWeightsButton"))
        self.activeradio = QtGui.QRadioButton(getis_ord)
        self.activeradio.setGeometry(QtCore.QRect(20, 100, 141, 17))
        self.activeradio.setText(QtGui.QApplication.translate("getis_ord", "Active Layer in Map", None, QtGui.QApplication.UnicodeUTF8))
        self.activeradio.setObjectName(_fromUtf8("activeradio"))
        self.activecombobox = QtGui.QComboBox(getis_ord)
        self.activecombobox.setGeometry(QtCore.QRect(160, 100, 201, 22))
        self.activecombobox.setObjectName(_fromUtf8("activecombobox"))
        self.layoutWidget = QtGui.QWidget(getis_ord)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 341, 25))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.SavedRadio = QtGui.QRadioButton(self.layoutWidget)
        self.SavedRadio.setText(QtGui.QApplication.translate("getis_ord", "Shaved shape file", None, QtGui.QApplication.UnicodeUTF8))
        self.SavedRadio.setObjectName(_fromUtf8("SavedRadio"))
        self.horizontalLayout.addWidget(self.SavedRadio)
        self.InputTextLine = QtGui.QLineEdit(self.layoutWidget)
        self.InputTextLine.setObjectName(_fromUtf8("InputTextLine"))
        self.horizontalLayout.addWidget(self.InputTextLine)
        self.InputButton = QtGui.QPushButton(self.layoutWidget)
        self.InputButton.setText(QtGui.QApplication.translate("getis_ord", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.InputButton.setObjectName(_fromUtf8("InputButton"))
        self.horizontalLayout.addWidget(self.InputButton)
        self.layoutWidget1 = QtGui.QWidget(getis_ord)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 300, 312, 19))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.GetisOrdcheck = QtGui.QCheckBox(self.layoutWidget1)
        self.GetisOrdcheck.setText(QtGui.QApplication.translate("getis_ord", "Verify Getis-Ord", None, QtGui.QApplication.UnicodeUTF8))
        self.GetisOrdcheck.setObjectName(_fromUtf8("GetisOrdcheck"))
        self.horizontalLayout_2.addWidget(self.GetisOrdcheck)
        self.Zvalue = QtGui.QCheckBox(self.layoutWidget1)
        self.Zvalue.setText(QtGui.QApplication.translate("getis_ord", "Z value", None, QtGui.QApplication.UnicodeUTF8))
        self.Zvalue.setObjectName(_fromUtf8("Zvalue"))
        self.horizontalLayout_2.addWidget(self.Zvalue)
        self.Pvalue = QtGui.QCheckBox(self.layoutWidget1)
        self.Pvalue.setText(QtGui.QApplication.translate("getis_ord", "P value", None, QtGui.QApplication.UnicodeUTF8))
        self.Pvalue.setObjectName(_fromUtf8("Pvalue"))
        self.horizontalLayout_2.addWidget(self.Pvalue)
        self.buttonBox = QtGui.QDialogButtonBox(getis_ord)
        self.buttonBox.setGeometry(QtCore.QRect(220, 400, 156, 23))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(getis_ord)
        QtCore.QObject.connect(self.InputButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.InputTextLine.copy)
        QtCore.QObject.connect(self.OutputButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.OuputTextLine.copy)
        QtCore.QObject.connect(self.SavedRadio, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.InputButton.setEnabled)
        QtCore.QObject.connect(self.SavedRadio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.activecombobox.setDisabled)
        QtCore.QObject.connect(self.activeradio, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.activecombobox.setEnabled)
        QtCore.QObject.connect(self.activeradio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.InputButton.setDisabled)
        QtCore.QObject.connect(self.activeradio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.activecombobox.setEnabled)
        QtCore.QObject.connect(self.activeradio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.SavedRadio.setDisabled)
        QtCore.QObject.connect(self.SavedRadio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.activeradio.setDisabled)
        QtCore.QObject.connect(self.SavedRadio, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.selectcombobox.setEnabled)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("clicked(QAbstractButton*)")), getis_ord.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), getis_ord.reject)
        QtCore.QMetaObject.connectSlotsByName(getis_ord)

    def retranslateUi(self, getis_ord):
        pass

