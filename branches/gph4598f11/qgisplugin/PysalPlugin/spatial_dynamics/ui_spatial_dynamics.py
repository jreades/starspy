# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_spatial_dynamics.ui'
#
# Created: Wed Nov 09 18:04:55 2011
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from pysal import *
import sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class ui_spatial_dynamics(object):
    def setupui(self, spatial_dynamics):
        spatial_dynamics.setObjectName(_fromUtf8("spatial_dynamics"))
        spatial_dynamics.resize(471, 498) 
	spatial_dynamics.setMinimumSize(QtCore.QSize(471, 498)) # restrict the minimum size
        spatial_dynamics.setMaximumSize(QtCore.QSize(471, 498)) # restrict the maximum size
        spatial_dynamics.setWindowTitle(QtGui.QApplication.translate("spatial_dynamics", "Spatial Markovs", None, QtGui.QApplication.UnicodeUTF8)) #set a name of windows
#"""-------------------------------------------------------------------------------------------------------------"""

	##### space for loading a new file #####
        self.lineEdit = QtGui.QLineEdit(spatial_dynamics)
        self.lineEdit.setGeometry(QtCore.QRect(130, 20, 291, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
		
	#####   find a place to save   #####
        self.pushButton_3 = QtGui.QPushButton(spatial_dynamics)
        self.pushButton_3.setGeometry(QtCore.QRect(430, 20, 31, 23))
        self.pushButton_3.setText(QtGui.QApplication.translate("spatial_dynamics", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
	#QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL('clicked'), self.openfile1())
	#self.pushButton_3.clicked.connect(self.openfile1()) 
        
#"""--------------------------------------------------------------------------------------------------------------"""

	###### group box for Data Processing #####
        self.groupBox_2 = QtGui.QGroupBox(spatial_dynamics)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 60, 451, 161))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("spatial_dynamics", "Data Processing", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
	       
	#####    Classification functions   #####
	self.comboBox = QtGui.QComboBox(self.groupBox_2)
        self.comboBox.setGeometry(QtCore.QRect(120, 40, 181, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("spatial_dynamics", "User Defined", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("spatial_dynamics", "Equal Interval", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("spatial_dynamics", "Natural Breaks", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(3, QtGui.QApplication.translate("spatial_dynamics", "Quantiles", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(4, QtGui.QApplication.translate("spatial_dynamics", "Percentiles", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(5, QtGui.QApplication.translate("spatial_dynamics", "Standard Mean", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(6, QtGui.QApplication.translate("spatial_dynamics", "Maximum_Breaks", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(7, QtGui.QApplication.translate("spatial_dynamics", "Fisher Jenks", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(8, QtGui.QApplication.translate("spatial_dynamics", "Jenks Caspall", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(9, QtGui.QApplication.translate("spatial_dynamics", "Jenks Caspall Forced", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(10, QtGui.QApplication.translate("spatial_dynamics", "Jenks Caspall Sampled", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(11, QtGui.QApplication.translate("spatial_dynamics", "Max P Classifier", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(12, QtGui.QApplication.translate("spatial_dynamics", "K classifiers", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
	self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(13, QtGui.QApplication.translate("spatial_dynamics", "gadf", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
	self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.setItemText(14, QtGui.QApplication.translate("spatial_dynamics", "None of the Above", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)

	#####         Standardization         #####
	self.comboBox_2 = QtGui.QComboBox(self.groupBox_2)
        self.comboBox_2.setGeometry(QtCore.QRect(120, 80, 51, 22))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.setItemText(0, QtGui.QApplication.translate("spatial_dynamics", "Yes", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.setItemText(1, QtGui.QApplication.translate("spatial_dynamics", "No", None, QtGui.QApplication.UnicodeUTF8))

	##### a space for saving a file after Data processing #####
	self.lineEdit_4 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(120, 120, 281, 20))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
	
	#####     find a place to save     #####
        self.pushButton_6 = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_6.setGeometry(QtCore.QRect(410, 120, 31, 23))
        self.pushButton_6.setText(QtGui.QApplication.translate("spatial_dynamics", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))

#"""--------------------------------------------------------------------------------------------------------------"""
	
	##### space for inputting spatial weights #####
        self.lineEdit_2 = QtGui.QLineEdit(spatial_dynamics)
        self.lineEdit_2.setGeometry(QtCore.QRect(130, 240, 281, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
	
	#####       find a place to input       #####
        self.pushButton_4 = QtGui.QPushButton(spatial_dynamics)
        self.pushButton_4.setGeometry(QtCore.QRect(420, 240, 31, 23))
        self.pushButton_4.setText(QtGui.QApplication.translate("spatial_dynamics", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))

	##### link with spatial weights module #####
	self.pushButton_7 = QtGui.QPushButton(spatial_dynamics)
        self.pushButton_7.setGeometry(QtCore.QRect(130, 270, 75, 23))
        self.pushButton_7.setText(QtGui.QApplication.translate("spatial_dynamics", "Create ", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))

#"""--------------------------------------------------------------------------------------------------------------"""

	#####        output functions        #####
        self.groupBox_4 = QtGui.QGroupBox(spatial_dynamics)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 300, 451, 141))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("spatial_dynamics", "Output", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
	
	#####             matrixs             #####
        self.comboBox_3 = QtGui.QComboBox(self.groupBox_4)
        self.comboBox_3.setGeometry(QtCore.QRect(120, 40, 301, 22))
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(0, QtGui.QApplication.translate("spatial_dynamics", "Transition Matrix", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(1, QtGui.QApplication.translate("spatial_dynamics", "Transition Probabilities", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(2, QtGui.QApplication.translate("spatial_dynamics", "Steady State Distribution", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(3, QtGui.QApplication.translate("spatial_dynamics", "First Mean Passage Time", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
	self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.setItemText(4, QtGui.QApplication.translate("spatial_dynamics", "ALL", None, QtGui.QApplication.UnicodeUTF8))
	#QtCore.QObject.connect(self., QtCore.SIGNAL('activated(QString)'), self.)
	
	##### a space for saving file after getting matrixs #####
        self.lineEdit_3 = QtGui.QLineEdit(self.groupBox_4)
        self.lineEdit_3.setGeometry(QtCore.QRect(120, 90, 281, 20))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
	
	#####       find a place to save       #####
        self.pushButton_5 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_5.setGeometry(QtCore.QRect(410, 90, 31, 23))
        self.pushButton_5.setText(QtGui.QApplication.translate("spatial_dynamics", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))

#"""--------------------------------------------------------------------------------------------------------------"""
	
	#####         OK and Cancel buttons         #####
        self.layoutWidget = QtGui.QWidget(spatial_dynamics)
        self.layoutWidget.setGeometry(QtCore.QRect(290, 450, 158, 25))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(self.layoutWidget)
        self.pushButton.setText(QtGui.QApplication.translate("spatial_dynamics", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
	#QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL('clicked()'), self.okbutton)
	self.horizontalLayout.addWidget(self.pushButton)
        
	self.pushButton_2 = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_2.setText(QtGui.QApplication.translate("spatial_dynamics", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)

	#self.pushButton_2.clicked.connect(QtGui.QApplication.instance().quit) #close all, including QGIS :(
	#self.pushButton_2=QtGui.QWidget(spatial_dynamics)
	#QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL('clicked()'), self.myquit()) #make effects for a button
	
#"""--------------------------------------------------------------------------------------------------------------"""

	#####            Labels              #####
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(30, 40, 71, 16))
        self.label.setText(QtGui.QApplication.translate("spatial_dynamics", "Classification", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 81, 16))
        self.label_2.setText(QtGui.QApplication.translate("spatial_dynamics", "Standardization", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(30, 120, 81, 16))
        self.label_7.setText(QtGui.QApplication.translate("spatial_dynamics", "Save Output as", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
	self.label_5 = QtGui.QLabel(self.groupBox_4)
        self.label_5.setGeometry(QtCore.QRect(70, 40, 31, 16))
        self.label_5.setText(QtGui.QApplication.translate("spatial_dynamics", "Matrix", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.groupBox_4)
        self.label_6.setGeometry(QtCore.QRect(30, 90, 81, 16))
        self.label_6.setText(QtGui.QApplication.translate("spatial_dynamics", "Save Output as", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
	self.label_3 = QtGui.QLabel(spatial_dynamics)
        self.label_3.setGeometry(QtCore.QRect(40, 20, 71, 16))
        self.label_3.setText(QtGui.QApplication.translate("spatial_dynamics", "Load New File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
	self.label_4 = QtGui.QLabel(spatial_dynamics)
        self.label_4.setGeometry(QtCore.QRect(20, 240, 101, 16))
        self.label_4.setText(QtGui.QApplication.translate("spatial_dynamics", "Input Spatial Weights ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
	##########################################

#"""--------------------------------------------------------------------------------------------------------------"""
	##### make effects for buttons and comboboxs #####

    	self.retranslateUi(spatial_dynamics)
	QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("rejected()")), spatial_dynamics.reject) #cancel button
	QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("accepted()")), spatial_dynamics.accept) #ok button
	QtCore.QMetaObject.connectSlotsByName(spatial_dynamics) #link buttons with functions in spatial_dynamicsdialog

#"""--------------------------------------------------------------------------------------------------------------"""

    def retranslateUi(self, spatial_dynamics):
	pass










	"""
    def openfile1(self):
	myFile = QFileDialog.getOpenFileName ("Select a datafile","","*.csv")
        self.ui.lineEdit.setText(myFile)    
    #def okbutton(self):
    def openfile1(self):
	#read by string
	filecontents=self.askopenfilename(filetypes=[ ("comma_separatedfiles","*.csv"),("textfiles","*.txt"),("excelfiles","*.xls"),("pythonfiles","*.py"),("accessfiles","*.asc"),("arcgisfiles","*.dbf"), ("spssfiles","*.sav"), ("multi_usagefiles","*.dat")])
	if filecontents != None:
		fp=open(filecontents) #fp is just the tag to open
		mydata=fp.read().strip() #mydata truly read the file in.

    def myquit(self):
	QtGui.QWidget.close()
	
"""
