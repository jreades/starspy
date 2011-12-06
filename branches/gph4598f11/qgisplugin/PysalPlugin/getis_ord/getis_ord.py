"""
/***************************************************************************
 getis_ord
                                 A QGIS plugin
 This is Getis-Ord General G
                              -------------------
        begin                : 2011-11-30
        copyright            : (C) 2011 by Nguyen Hong Ngoc
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog

from getis_orddialog import getis_ordDialog

      
class getis_ord:

    
    
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/getis_ord/icon.png"), \
            "ThucdonGetis-Ord General G", self.iface.mainWindow())
      
        self.action.setWhatsThis("Configuration for Getis-Ord General B")
        self.action.setStatusTip("This is status tip")

       # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&MenuGetis-Ord General G", self.action)

           
       
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&MenuGetis-Ord General G",self.action)
        self.iface.removeToolBarIcon(self.action)
           

    # run method that performs all the real work
    def run(self):

        # create and show the dialog
        dlg = getis_ordDialog(self.iface)
        # show the dialog
        dlg.show()
        result = dlg.exec_()
  
   
           
        # See if OK was pressed
        if result == 1:
           
           # do something useful (delete the line containing pass and
            # substitute with your code
            pass
 

