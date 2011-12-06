"""
/***************************************************************************
 getis_ord
                                 A QGIS plugin
 This is Getis-Ord General G
                             -------------------
        begin                : 2011-11-30
        copyright            : (C) 2011 by Nguyen Hong Ngoc
        email                : ngoc.hong.nguyen@asu.edu
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
    return "Getis-Ord General G"
def description():
    return "This is Getis-Ord General G"
def version():
    return "Version 0.3"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.0"


def classFactory(iface):
    # load getis_ord class from file getis_ord
    from getis_ord import getis_ord
    return getis_ord(iface)






    
