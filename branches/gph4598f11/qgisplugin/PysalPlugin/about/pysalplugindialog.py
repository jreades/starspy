"""
/***************************************************************************
 PysalPluginDialog
                                 A QGIS plugin
 Pysal library
                             -------------------
        begin                : 2011-09-30
        copyright            : (C) 2011 by GPH598
        email                :  
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui
from ui_pysalplugin import Ui_PysalPlugin
# create the dialog for zoom to point
class PysalPluginDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_PysalPlugin()
        self.ui.setupUi(self)
