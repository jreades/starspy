# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spatial_dynamics.ui'
#
# Created: Thu Dec 01 16:22:51 2011
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_spatial_dynamics(object):
    def setupUi(self, spatial_dynamics):
        spatial_dynamics.setObjectName(_fromUtf8("spatial_dynamics"))
        spatial_dynamics.resize(400, 458)
	spatial_dynamics.setMinimumSize(QtCore.QSize(400, 458)) # restrict the minimum size
	spatial_dynamics.setMaximumSize(QtCore.QSize(400, 458)) # restrict the maximum size
	spatial_dynamics.setWindowTitle(QtGui.QApplication.translate("spatial_dynamics", "Spatial Dynamics", None, QtGui.QApplication.UnicodeUTF8))
        spatial_dynamics.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.Taiwan))
        self.inputweightslabel = QtGui.QLabel(spatial_dynamics)
        self.inputweightslabel.setGeometry(QtCore.QRect(20, 220, 111, 16))
        self.inputweightslabel.setText(QtGui.QApplication.translate("spatial_dynamics", "Input Spatial Weights", None, QtGui.QApplication.UnicodeUTF8))
        self.inputweightslabel.setObjectName(_fromUtf8("inputweightslabel"))
        self.inputweightsline = QtGui.QLineEdit(spatial_dynamics)
        self.inputweightsline.setGeometry(QtCore.QRect(130, 220, 221, 20))
        self.inputweightsline.setObjectName(_fromUtf8("inputweightsline"))
        self.inputweightsbutton = QtGui.QPushButton(spatial_dynamics)
        self.inputweightsbutton.setGeometry(QtCore.QRect(360, 220, 31, 23))
        self.inputweightsbutton.setText(QtGui.QApplication.translate("spatial_dynamics", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.inputweightsbutton.setObjectName(_fromUtf8("inputweightsbutton"))
        self.inputweightscreate = QtGui.QPushButton(spatial_dynamics)
        self.inputweightscreate.setGeometry(QtCore.QRect(130, 250, 75, 23))
        self.inputweightscreate.setText(QtGui.QApplication.translate("spatial_dynamics", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.inputweightscreate.setObjectName(_fromUtf8("inputweightscreate"))
        self.outputgroupbox = QtGui.QGroupBox(spatial_dynamics)
        self.outputgroupbox.setGeometry(QtCore.QRect(10, 280, 381, 141))
        self.outputgroupbox.setTitle(QtGui.QApplication.translate("spatial_dynamics", "Output", None, QtGui.QApplication.UnicodeUTF8))
        self.outputgroupbox.setObjectName(_fromUtf8("outputgroupbox"))
        self.matrixcheckbox = QtGui.QCheckBox(self.outputgroupbox)
        self.matrixcheckbox.setGeometry(QtCore.QRect(20, 20, 241, 16))
        self.matrixcheckbox.setText(QtGui.QApplication.translate("spatial_dynamics", "Global Transition Probability Matrix", None, QtGui.QApplication.UnicodeUTF8))
        self.matrixcheckbox.setObjectName(_fromUtf8("matrixcheckbox"))
        self.probabilitiescheckbox = QtGui.QCheckBox(self.outputgroupbox)
        self.probabilitiescheckbox.setGeometry(QtCore.QRect(20, 40, 231, 16))
        self.probabilitiescheckbox.setText(QtGui.QApplication.translate("spatial_dynamics", "Conditioned Transition Probability Matrices", None, QtGui.QApplication.UnicodeUTF8))
        self.probabilitiescheckbox.setObjectName(_fromUtf8("probabilitiescheckbox"))
        self.steadystatecheckbox = QtGui.QCheckBox(self.outputgroupbox)
        self.steadystatecheckbox.setGeometry(QtCore.QRect(20, 60, 141, 16))
        self.steadystatecheckbox.setText(QtGui.QApplication.translate("spatial_dynamics", "Steady State Distributions", None, QtGui.QApplication.UnicodeUTF8))
        self.steadystatecheckbox.setObjectName(_fromUtf8("steadystatecheckbox"))
        self.firstcheckbox = QtGui.QCheckBox(self.outputgroupbox)
        self.firstcheckbox.setGeometry(QtCore.QRect(20, 80, 151, 16))
        self.firstcheckbox.setText(QtGui.QApplication.translate("spatial_dynamics", "First Mean Passage Time", None, QtGui.QApplication.UnicodeUTF8))
        self.firstcheckbox.setObjectName(_fromUtf8("firstcheckbox"))
        self.saveoutputbutton = QtGui.QPushButton(self.outputgroupbox)
        self.saveoutputbutton.setGeometry(QtCore.QRect(340, 110, 31, 23))
        self.saveoutputbutton.setText(QtGui.QApplication.translate("spatial_dynamics", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.saveoutputbutton.setObjectName(_fromUtf8("saveoutputbutton"))
        self.saveoutputlabel = QtGui.QLabel(self.outputgroupbox)
        self.saveoutputlabel.setGeometry(QtCore.QRect(20, 110, 81, 16))
        self.saveoutputlabel.setText(QtGui.QApplication.translate("spatial_dynamics", "Save Output as", None, QtGui.QApplication.UnicodeUTF8))
        self.saveoutputlabel.setObjectName(_fromUtf8("saveoutputlabel"))
        self.saveoutputline = QtGui.QLineEdit(self.outputgroupbox)
        self.saveoutputline.setGeometry(QtCore.QRect(100, 110, 231, 20))
        self.saveoutputline.setObjectName(_fromUtf8("saveoutputline"))
        self.buttonBox = QtGui.QDialogButtonBox(spatial_dynamics)
        self.buttonBox.setGeometry(QtCore.QRect(230, 430, 156, 23))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(spatial_dynamics)
        self.label.setGeometry(QtCore.QRect(10, 10, 121, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        self.label.setFont(font)
        self.label.setText(QtGui.QApplication.translate("spatial_dynamics", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'新細明體\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Spatial Markovs</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.groupBox = QtGui.QGroupBox(spatial_dynamics)
        self.groupBox.setGeometry(QtCore.QRect(10, 30, 381, 181))
        self.groupBox.setTitle(QtGui.QApplication.translate("spatial_dynamics", "Input", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.inputbutton = QtGui.QPushButton(self.groupBox)
        self.inputbutton.setGeometry(QtCore.QRect(340, 90, 31, 23))
        self.inputbutton.setText(QtGui.QApplication.translate("spatial_dynamics", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.inputbutton.setObjectName(_fromUtf8("inputbutton"))
        self.inputline = QtGui.QLineEdit(self.groupBox)
        self.inputline.setGeometry(QtCore.QRect(100, 90, 231, 20))
        self.inputline.setObjectName(_fromUtf8("inputline"))
        self.savedshpradio = QtGui.QRadioButton(self.groupBox)
        self.savedshpradio.setGeometry(QtCore.QRect(10, 60, 111, 16))
        self.savedshpradio.setText(QtGui.QApplication.translate("spatial_dynamics", "Saved .csv File", None, QtGui.QApplication.UnicodeUTF8))
        self.savedshpradio.setObjectName(_fromUtf8("savedshpradio"))
        self.inputshplabel = QtGui.QLabel(self.groupBox)
        self.inputshplabel.setGeometry(QtCore.QRect(10, 90, 121, 16))
        self.inputshplabel.setText(QtGui.QApplication.translate("spatial_dynamics", "Input .csv File", None, QtGui.QApplication.UnicodeUTF8))
        self.inputshplabel.setObjectName(_fromUtf8("inputshplabel"))
        self.activeradio = QtGui.QRadioButton(self.groupBox)
        self.activeradio.setGeometry(QtCore.QRect(10, 30, 121, 16))
        self.activeradio.setText(QtGui.QApplication.translate("spatial_dynamics", "Active Layer in map", None, QtGui.QApplication.UnicodeUTF8))
        self.activeradio.setObjectName(_fromUtf8("activeradio"))
        self.activecombobox = QtGui.QComboBox(self.groupBox)
        self.activecombobox.setGeometry(QtCore.QRect(140, 30, 231, 22))
        self.activecombobox.setObjectName(_fromUtf8("activecombobox"))
        self.startyear = QtGui.QLabel(self.groupBox)
        self.startyear.setGeometry(QtCore.QRect(20, 120, 81, 16))
        self.startyear.setText(QtGui.QApplication.translate("spatial_dynamics", "Start Year", None, QtGui.QApplication.UnicodeUTF8))
        self.startyear.setObjectName(_fromUtf8("startyear"))
        self.startcombobox = QtGui.QComboBox(self.groupBox)
        self.startcombobox.setGeometry(QtCore.QRect(100, 120, 231, 22))
        self.startcombobox.setObjectName(_fromUtf8("startcombobox"))
        self.endyear = QtGui.QLabel(self.groupBox)
        self.endyear.setGeometry(QtCore.QRect(20, 150, 81, 16))
        self.endyear.setText(QtGui.QApplication.translate("spatial_dynamics", "End Year", None, QtGui.QApplication.UnicodeUTF8))
        self.endyear.setObjectName(_fromUtf8("endyear"))
        self.endcombobox = QtGui.QComboBox(self.groupBox)
        self.endcombobox.setGeometry(QtCore.QRect(100, 150, 231, 22))
        self.endcombobox.setObjectName(_fromUtf8("endcombobox"))

        self.retranslateUi(spatial_dynamics)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), spatial_dynamics.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), spatial_dynamics.reject)
        QtCore.QObject.connect(self.activeradio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.inputline.setDisabled)
        QtCore.QObject.connect(self.activeradio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.inputbutton.setDisabled)
        QtCore.QObject.connect(self.savedshpradio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.activecombobox.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(spatial_dynamics)

    def retranslateUi(self, spatial_dynamics):
        pass

