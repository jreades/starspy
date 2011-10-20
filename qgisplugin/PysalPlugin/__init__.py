"""
/***************************************************************************
 PysalPlugin
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
 This script initializes the plugin, making it known to QGIS.
"""
def name():
    return "Pysal for QGIS"
def description():
    return "Pysal library"
def version():
    return "Version 0.1"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.0"
def classFactory(iface):
    # load PysalPlugin class from file PysalPlugin
    from pysalplugin import PysalPlugin
    return PysalPlugin(iface)
