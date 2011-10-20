# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_pysalplugin.ui'
#
# Created: Mon Oct 03 12:56:23 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PysalPlugin(object):
    def setupUi(self, PysalPlugin):
        PysalPlugin.setObjectName(_fromUtf8("PysalPlugin"))
        PysalPlugin.resize(640, 490)
        PysalPlugin.setWindowTitle(QtGui.QApplication.translate("PysalPlugin", "PysalPlugin", None, QtGui.QApplication.UnicodeUTF8))
        self.webView = QtWebKit.QWebView(PysalPlugin)
        self.webView.setObjectName(_fromUtf8("webView"))
        self.webView.setGeometry(QtCore.QRect(0, 0, 640, 490))
        self.retranslateUi(PysalPlugin)
        QtCore.QMetaObject.connectSlotsByName(PysalPlugin)

    def retranslateUi(self, PysalPlugin):
        pass

from PyQt4 import QtWebKit
