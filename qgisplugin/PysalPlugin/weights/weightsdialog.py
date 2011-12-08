"""
This dialog window is made for computing spatial weights in PySal-->Weights-->Compute Weights
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_weights import Ui_Weights
import pysal, numpy
import os.path
# create the dialog
class WeightsDialog(QtGui.QDialog):
    '''This class is the weights dialog and contains all weights methods.  It loads the ui_weights.py ui file'''
    def __init__(self,iface):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from QTDesigner.
        self.ui = Ui_Weights()
        self.ui.setupUi(self)
        self.iface = iface
        self.dir = os.path.realpath(os.path.curdir)
        self.scount = -1
        self.lcount = -1
        self.layers = []
        self.w = 0
        for i in range(self.iface.mapCanvas().layerCount()):   #this for loop adds current layers
            layer = self.iface.mapCanvas().layer(i)             #to dropdown menu
            if layer.type()== 0:
                self.layers += [layer]
                self.ui.sourceLayer.addItem(layer.name())
                
    @pyqtSignature('') #prevents actions being handled twice
    def on_rbUseActiveLayer_clicked(self):
        '''When radiobutton Use Active Layer update the NN slider'''
        if self.lcount != -1:
            self.ui.horizontalSlider.setMaximum(self.lcount-1)
            self.ui.horizontalSlider.setTickInterval((self.lcount-1)/10 or 1)
    @pyqtSignature('') #prevents actions being handled twice
    def on_rbSaveShapefile_clicked(self):
        '''if the user toggles back to a saved shapefile already selected update NN slider'''
        if self.scount != -1:
            self.ui.horizontalSlider.setMaximum(self.scount-1)
            self.ui.horizontalSlider.setTickInterval((self.scount-1)/10 or 1) 
    @pyqtSignature('') #prevents actions being handled twice
    def on_pbnInput_clicked(self):
        '''Pressbutton Input clicked.  Users selects a shapefile and the NNslider updates'''
        myFile = QFileDialog.getOpenFileName (self, "Select a shapefile","","*.shp")
        self.ui.inputFile.setText(myFile)
        vlayer = QgsVectorLayer(myFile, "temp", "ogr")
        pr = vlayer.dataProvider()
        self.scount = pr.featureCount()
        self.ui.horizontalSlider.setMaximum(self.scount-1)
        self.ui.horizontalSlider.setTickInterval((self.scount-1)/10 or 1)
    @pyqtSignature('int') #prevents actions being handled twice    
    def on_sourceLayer_currentIndexChanged(self,i):
        '''User selects a new layer from the active layers and the NN slider updates'''
        l = self.layers[i]
        self.lcount = l.featureCount()
        self.ui.horizontalSlider.setMaximum(self.lcount-1)
        self.ui.horizontalSlider.setTickInterval((self.lcount-1)/10 or 1)
        
    @pyqtSignature('') #prevents actions being handled twice
    def on_pbnOutput_clicked(self):
        '''Select a location for the output file'''
        dlg = QFileDialog()
        myFile = dlg.getSaveFileName(self, "Select a file for the weights matrix", "Saved File", "*.gal;;*.gwt;;*.mat")
        myFile += dlg.selectedNameFilter()[0]
        self.ui.outputFile.setText(myFile[0:-1])

###############################################################################################
####                                                                                       ####
####                                                                                       ####
####       This is the method we need to implement.  When they click OK this method runs   ####
####                                                                                       ####
####                                                                                       ####
###############################################################################################
    def accept(self):
        '''The user has hit OK, run the script and create the output file'''
        savefile = str(self.ui.outputFile.text()) #this will be a string like "c:\output"
        addNumNeighbors = self.ui.addNumNeighbors.checkState() #this will be 0 or 2 but we can treat it as False/True
        addY = self.ui.addY.checkState() #this will be 0 or 2 but we can treat it as False/True      
        k = self.ui.horizontalSlider.value() #nearest neighbor
        threshDist = ""
        invDist = ""
            
        # use shapefile
        if self.ui.rbSaveShapefile.isChecked():
            openfile = str(self.ui.inputFile.text()) #using a saved file this will be a string like "c:\shapefile.shp"

            # contiguity-based
            if self.ui.rbContiguity.isChecked():
                contIdx = self.ui.contComboBox.currentIndex()
                if contIdx == 0:
                    self.w = pysal.rook_from_shapefile(openfile)
                elif contIdx == 1:
                    self.w = pysal.queen_from_shapefile(openfile)
                else:
                    return
            # distance-based
            elif self.ui.rbDistance.isChecked():
                distIdx = self.ui.distMethod.currentIndex()
                if distIdx == 0:
                    threshDist = float(self.ui.threshDist.text())
                    self.w = pysal.threshold_binaryW_from_shapefile(openfile,
                                                                threshDist)
                elif distIdx == 1:
                    invDist = float(self.ui.invDist.text())
                    self.w = pysal.threshold_continuousW_from_shapefile(openfile,
                                                                   invDist)
                elif distIdx == 2:
                    self.w = pysal.knnW_from_shapefile(openfile, k)
                else:
                    return
    
            output = pysal.open(savefile, 'w')
            output.write(self.w)
            output.close()
            #can pysal easily do all the work?          
        elif self.ui.rbUseActiveLayer.isChecked():
            layer = self.layers[self.ui.sourceLayer.currentIndex()]
        ###################################################################
        ### Now we have either a layer in QGIS or a path to a shapefile ###
        ### What are the next steps? Import Pysal?                      ###
        ###################################################################
            
            if layer.type() == layer.VectorLayer:
                pts = []
                provider = layer.dataProvider()
                
                # select all features
                feat = QgsFeature()
                allAttrs = provider.attributeIndexes()
                provider.select(allAttrs)
                
                while provider.nextFeature(feat):
                    
                    geom = feat.geometry()
                    # for Point Dataset,
                    # append itself
                    if geom.type() == QGis.Point:
                        pt = geom.asPoint()
                        pts.append((pt.x(), pt.y()))
                    # for Polygon Dataset,
                    # append the centroid of multiPolygon
                    elif geom.type() == QGis.Polygon:
                        pt = geom.centroid().asPoint()
                        pts.append((pt.x(), pt.y()))
                    else:
                        QMessageBox.warning(self.iface.mainWindow(),
                        "Spatial Weights", " Unsupported Geometric Type")
                
                pts = numpy.array(pts)
                # contiguity-based
                if self.ui.rbContiguity.isChecked():
                    QMessageBox.warning(self.iface.mainWindow(),
                        "Spatial Weights", "Contiguity Weights Created from Layer Not Supported")
                    return
                # distance-based
                elif self.ui.rbDistance.isChecked():
                    distIdx = self.ui.distMethod.currentIndex()
                    if distIdx == 0:
                        threshDist = float(self.ui.threshDist.text())
                        self.w = pysal.threshold_binaryW_from_array(
                                                                pts,threshDist)
                    elif distIdx == 1:
                        invDist = float(self.ui.invDist.text())
                        self.w = pysal.threshold_continuousW_from_array(
                                                                pts,invDist)
                    elif distIdx == 2:
                        self.w = pysal.knnW_from_array(pts, k)
                    else:
                        return
        
                output = pysal.open(savefile, 'w')
                output.write(self.w)
                output.close()
            elif layer.type() == layer.RasterLayer:
                QMessageBox.warning(self.iface.mainWindow(),
                        "Spatial Weights", "Raster Layer Not Supported")
                return
            #Do weights have meaning for rasters?  We can limit the user to only choosing vectors at the
            #dropdown menu. Also can choose geometry type like layer.geometryType() == QGis.Polygon
            else:
                QMessageBox.warning(self.iface.mainWindow(),
                        "Spatial Weights", "Unknown Layer Type")
                return
            
        #qgis api http://doc.qgis.org/stable/annotated.html
            
        self.close() #close the dialog window


        
