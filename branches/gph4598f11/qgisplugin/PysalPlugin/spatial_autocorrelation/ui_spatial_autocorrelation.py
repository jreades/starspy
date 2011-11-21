# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spatial_autocorrelation.ui'
#
# Created: Sun Nov 20 18:04:51 2011
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_spatial_autocorrelation(object):
    def setupUi(self, spatial_autocorrelation):
        spatial_autocorrelation.setObjectName(_fromUtf8("spatial_autocorrelation"))
        spatial_autocorrelation.resize(400, 462)
	spatial_autocorrelation.setMinimumSize(QtCore.QSize(400, 462)) # restrict the minimum size
	spatial_autocorrelation.setMaximumSize(QtCore.QSize(400, 462)) # restrict the maximum size
	spatial_autocorrelation.setMouseTracking(False)
        spatial_autocorrelation.setWindowTitle(QtGui.QApplication.translate("spatial_autocorrelation", "Spatial Autocorrelation", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonBox = QtGui.QDialogButtonBox(spatial_autocorrelation)
        self.buttonBox.setGeometry(QtCore.QRect(230, 430, 156, 23))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.input_groupbox = QtGui.QGroupBox(spatial_autocorrelation)
        self.input_groupbox.setGeometry(QtCore.QRect(20, 30, 361, 111))
        self.input_groupbox.setTitle(QtGui.QApplication.translate("spatial_autocorrelation", "Input", None, QtGui.QApplication.UnicodeUTF8))
        self.input_groupbox.setObjectName(_fromUtf8("input_groupbox"))
        self.activeradio = QtGui.QRadioButton(self.input_groupbox)
        self.activeradio.setGeometry(QtCore.QRect(10, 20, 141, 16))
        self.activeradio.setText(QtGui.QApplication.translate("spatial_autocorrelation", "Active Layer in Map", None, QtGui.QApplication.UnicodeUTF8))
        self.activeradio.setObjectName(_fromUtf8("activeradio"))
        self.savedshpradio = QtGui.QRadioButton(self.input_groupbox)
        self.savedshpradio.setGeometry(QtCore.QRect(10, 50, 121, 16))
        self.savedshpradio.setText(QtGui.QApplication.translate("spatial_autocorrelation", "Saved Shapefile", None, QtGui.QApplication.UnicodeUTF8))
        self.savedshpradio.setObjectName(_fromUtf8("savedshpradio"))
        self.activecombobox = QtGui.QComboBox(self.input_groupbox)
        self.activecombobox.setGeometry(QtCore.QRect(140, 20, 211, 22))
        self.activecombobox.setObjectName(_fromUtf8("activecombobox"))
        self.inputshplabel = QtGui.QLabel(self.input_groupbox)
        self.inputshplabel.setGeometry(QtCore.QRect(20, 80, 111, 16))
        self.inputshplabel.setText(QtGui.QApplication.translate("spatial_autocorrelation", "Input Shapefile", None, QtGui.QApplication.UnicodeUTF8))
        self.inputshplabel.setObjectName(_fromUtf8("inputshplabel"))
        self.inputshpline = QtGui.QLineEdit(self.input_groupbox)
        self.inputshpline.setGeometry(QtCore.QRect(100, 80, 211, 20))
        self.inputshpline.setObjectName(_fromUtf8("inputshpline"))
        self.inputshpbutton = QtGui.QPushButton(self.input_groupbox)
        self.inputshpbutton.setGeometry(QtCore.QRect(320, 80, 31, 23))
        self.inputshpbutton.setText(QtGui.QApplication.translate("spatial_autocorrelation", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.inputshpbutton.setObjectName(_fromUtf8("inputshpbutton"))
        self.output_groupBox = QtGui.QGroupBox(spatial_autocorrelation)
        self.output_groupBox.setGeometry(QtCore.QRect(20, 210, 361, 211))
        self.output_groupBox.setTitle(QtGui.QApplication.translate("spatial_autocorrelation", "Output", None, QtGui.QApplication.UnicodeUTF8))
        self.output_groupBox.setObjectName(_fromUtf8("output_groupBox"))
        self.MoranIcheck = QtGui.QCheckBox(self.output_groupBox)
        self.MoranIcheck.setGeometry(QtCore.QRect(10, 20, 121, 16))
        self.MoranIcheck.setText(QtGui.QApplication.translate("spatial_autocorrelation", "Value of Moran\'s I", None, QtGui.QApplication.UnicodeUTF8))
        self.MoranIcheck.setObjectName(_fromUtf8("MoranIcheck"))
        self.outputbutton = QtGui.QPushButton(self.output_groupBox)
        self.outputbutton.setGeometry(QtCore.QRect(310, 180, 31, 23))
        self.outputbutton.setText(QtGui.QApplication.translate("spatial_autocorrelation", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.outputbutton.setObjectName(_fromUtf8("outputbutton"))
        self.outputline = QtGui.QLineEdit(self.output_groupBox)
        self.outputline.setGeometry(QtCore.QRect(70, 180, 231, 20))
        self.outputline.setObjectName(_fromUtf8("outputline"))
        self.outputlabel = QtGui.QLabel(self.output_groupBox)
        self.outputlabel.setGeometry(QtCore.QRect(10, 180, 111, 16))
        self.outputlabel.setText(QtGui.QApplication.translate("spatial_autocorrelation", "Output File", None, QtGui.QApplication.UnicodeUTF8))
        self.outputlabel.setObjectName(_fromUtf8("outputlabel"))
        self.normalradioButton = QtGui.QRadioButton(self.output_groupBox)
        self.normalradioButton.setGeometry(QtCore.QRect(10, 50, 171, 16))
        self.normalradioButton.setText(QtGui.QApplication.translate("spatial_autocorrelation", "Under Normality Assumption", None, QtGui.QApplication.UnicodeUTF8))
        self.normalradioButton.setObjectName(_fromUtf8("normalradioButton"))
        self.randomradiobutton = QtGui.QRadioButton(self.output_groupBox)
        self.randomradiobutton.setGeometry(QtCore.QRect(10, 80, 191, 16))
        self.randomradiobutton.setText(QtGui.QApplication.translate("spatial_autocorrelation", "Under Randomization Assumption", None, QtGui.QApplication.UnicodeUTF8))
        self.randomradiobutton.setObjectName(_fromUtf8("randomradiobutton"))
        self.expectedcheckbox = QtGui.QCheckBox(self.output_groupBox)
        self.expectedcheckbox.setGeometry(QtCore.QRect(20, 110, 121, 16))
        self.expectedcheckbox.setText(QtGui.QApplication.translate("spatial_autocorrelation", "Expected Value", None, QtGui.QApplication.UnicodeUTF8))
        self.expectedcheckbox.setObjectName(_fromUtf8("expectedcheckbox"))
        self.variancecheckbox = QtGui.QCheckBox(self.output_groupBox)
        self.variancecheckbox.setGeometry(QtCore.QRect(20, 130, 73, 16))
        self.variancecheckbox.setText(QtGui.QApplication.translate("spatial_autocorrelation", "Variance of I", None, QtGui.QApplication.UnicodeUTF8))
        self.variancecheckbox.setObjectName(_fromUtf8("variancecheckbox"))
        self.standardcheckbox = QtGui.QCheckBox(self.output_groupBox)
        self.standardcheckbox.setGeometry(QtCore.QRect(20, 150, 141, 16))
        self.standardcheckbox.setText(QtGui.QApplication.translate("spatial_autocorrelation", "Standard Deviation of I", None, QtGui.QApplication.UnicodeUTF8))
        self.standardcheckbox.setObjectName(_fromUtf8("standardcheckbox"))
        self.Zcheckbox = QtGui.QCheckBox(self.output_groupBox)
        self.Zcheckbox.setGeometry(QtCore.QRect(180, 110, 73, 16))
        self.Zcheckbox.setText(QtGui.QApplication.translate("spatial_autocorrelation", "z-value of I", None, QtGui.QApplication.UnicodeUTF8))
        self.Zcheckbox.setObjectName(_fromUtf8("Zcheckbox"))
        self.Pcheckbox = QtGui.QCheckBox(self.output_groupBox)
        self.Pcheckbox.setGeometry(QtCore.QRect(180, 130, 73, 16))
        self.Pcheckbox.setText(QtGui.QApplication.translate("spatial_autocorrelation", "p-value of I", None, QtGui.QApplication.UnicodeUTF8))
        self.Pcheckbox.setObjectName(_fromUtf8("Pcheckbox"))
        self.MoranIlabel = QtGui.QLabel(spatial_autocorrelation)
        self.MoranIlabel.setGeometry(QtCore.QRect(20, 10, 91, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times New Roman"))
        self.MoranIlabel.setFont(font)
        self.MoranIlabel.setText(QtGui.QApplication.translate("spatial_autocorrelation", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'新細明體\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Moran\'s I</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.MoranIlabel.setObjectName(_fromUtf8("MoranIlabel"))
        self.Inputweighslabel = QtGui.QLabel(spatial_autocorrelation)
        self.Inputweighslabel.setGeometry(QtCore.QRect(30, 150, 111, 16))
        self.Inputweighslabel.setText(QtGui.QApplication.translate("spatial_autocorrelation", "Input Spatial Weights", None, QtGui.QApplication.UnicodeUTF8))
        self.Inputweighslabel.setObjectName(_fromUtf8("Inputweighslabel"))
        self.Inputweightsline = QtGui.QLineEdit(spatial_autocorrelation)
        self.Inputweightsline.setGeometry(QtCore.QRect(140, 150, 191, 20))
        self.Inputweightsline.setObjectName(_fromUtf8("Inputweightsline"))
        self.Inputweightsbutton = QtGui.QPushButton(spatial_autocorrelation)
        self.Inputweightsbutton.setGeometry(QtCore.QRect(340, 150, 31, 23))
        self.Inputweightsbutton.setText(QtGui.QApplication.translate("spatial_autocorrelation", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.Inputweightsbutton.setObjectName(_fromUtf8("Inputweightsbutton"))
        self.Inputweightscreate = QtGui.QPushButton(spatial_autocorrelation)
        self.Inputweightscreate.setGeometry(QtCore.QRect(140, 180, 75, 23))
        self.Inputweightscreate.setText(QtGui.QApplication.translate("spatial_autocorrelation", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.Inputweightscreate.setObjectName(_fromUtf8("Inputweightscreate"))

        self.retranslateUi(spatial_autocorrelation)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), spatial_autocorrelation.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), spatial_autocorrelation.reject)
        QtCore.QObject.connect(self.activeradio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.inputshpbutton.setDisabled)
        QtCore.QObject.connect(self.savedshpradio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.inputshpbutton.setEnabled)
        QtCore.QObject.connect(self.savedshpradio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.activecombobox.setDisabled)
        QtCore.QObject.connect(self.activeradio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.inputshpline.setDisabled)
        QtCore.QObject.connect(self.savedshpradio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.inputshpline.setEnabled)
        QtCore.QObject.connect(self.randomradiobutton, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.expectedcheckbox.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(spatial_autocorrelation)

    def retranslateUi(self, spatial_autocorrelation):
        pass

