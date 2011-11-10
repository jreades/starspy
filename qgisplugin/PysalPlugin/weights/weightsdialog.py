"""
This dialog window is made for computing spatial weights in PySal-->Weights-->Compute Weights
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_weights import Ui_Weights
import pysal
import os.path
# create the dialog
class WeightsDialog(QtGui.QDialog):
    def __init__(self,iface):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from QTDesigner.
        self.ui = Ui_Weights()
        self.ui.setupUi(self)
        self.iface = iface
        self.dir = os.path.realpath(os.path.curdir)

        self.layers = []
        for i in range(self.iface.mapCanvas().layerCount()):    #this for loop adds current layers
            layer = self.iface.mapCanvas().layer(i)             #to dropdown menu
            self.layers += [layer]
            self.ui.sourceLayer.addItem(layer.name())


    @pyqtSignature('') #prevents actions being handled twice
    def on_pbnInput_clicked(self):
        myFile = QFileDialog.getOpenFileName (self, "Select a shapefile","","*.shp")
        self.ui.inputFile.setText(myFile)

    @pyqtSignature('') #prevents actions being handled twice
    def on_pbnOutput_clicked(self):
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
        savefile = str(self.ui.outputFile.text()) #this will be a string like "c:\output"
        
        addNumNeighbors = self.ui.addNumNeighbors.checkState() #this will be 0 or 2 but we can treat it as False/True
        addY = self.ui.addY.checkState() #this will be 0 or 2 but we can treat it as False/True      
        if self.ui.rbSaveShapefile.isChecked():
            openfile = str(self.ui.inputFile.text()) #using a saved file this will be a string like "c:\shapefile.shp"
            w = 0
            if self.ui.rbContiguity.isChecked():
                contIdx = self.ui.contComboBox.currentIndex()
                if contIdx == 0:
                    w = pysal.rook_from_shapefile(openfile)
                elif contIdx == 1:
                    w = pysal.queen_from_shapefile(openfile)
                else:
                    return
            elif self.ui.rbDistance.isChecked():
                distIdx = self.ui.distMethod.currentIndex()
                # k = 2
                #try:
                #    k = int(str(self.ui.inputDistance.text()))
                #except Exception:
                #    raise Exception
                if distIdx == 0:
                    # w = pysal.knnW_from_shapefile(openfile, k)
                    w = pysal.knnW_from_shapefile(openfile)
                else:
                    return

            output = pysal.open(savefile, 'w')
            output.write(w)
            output.close()
            #can pysal easily do all the work?          
        elif self.ui.rbUseActiveLayer.isChecked():
            layer = self.layers[self.ui.sourceLayer.currentIndex()]
        ###################################################################
        ### Now we have either a layer in QGIS or a path to a shapefile ###
        ### What are the next steps? Import Pysal?                      ###
        ###################################################################
        
            if layer.type() == layer.VectorLayer:
                pass
            elif layer.type() == layer.RasterLayer:
                pass
            #Do weights have meaning for rasters?  We can limit the user to only choosing vectors at the
            #dropdown menu. Also can choose geometry type like layer.geometryType() == QGis.Polygon
            else: raise "unknown layer type"
        
        #qgis api http://doc.qgis.org/stable/annotated.html
        
        self.close() #close the dialog window


        '''
        # example code from a hillshade plugin
        myEngine = ShadedReliefEngine()
        myEngine.minSlopeParam = self.ui.spinBoxMinSlope.value()
        myEngine.maxSlopeParam = self.ui.spinBoxMaxSlope.value()
        myEngine.azimuthParam = self.ui.spinBoxAzi.value()
        myEngine.incParam = self.ui.spinBoxInc.value()
        myEngine.vzParam = self.ui.doubleSpinBoxVz.value()
        myEngine.strideParam = self.ui.spinBoxStride.value()

        if self.ui.rbUseActiveLayer.isChecked():



          if self.iface.mapCanvas().layerCount() == 0:
            QMessageBox.warning(self.iface.mainWindow(),
                "Shaded Relief", "First open any one-band (DEM) raster layer, please")
            return 2
          layer = self.iface.activeLayer()

          if layer == None or layer.type() != layer.RasterLayer or layer.bandCount() != 1:
            QMessageBox.warning(self.iface.mainWindow(),
                "Shaded Relief", "Please select one-band (DEM) raster layer")
            return 3

          myEngine.extentParam = layer.extent()
          myEngine.widthParam = layer.width()
          myEngine.heightParam = layer.height()
          myEngine.noDataParam = layer.noDataValue()
          myEngine.outFileParam = f
          myEngine.sourceFileParam = layer.source()
          myEngine.wktParam = layer.srs().toWkt()
          myEngine.run()
          if len(f) > 0:
            newLayer = QgsRasterLayer(str(f),os.path.basename(str(f)))
            QgsMapLayerRegistry.instance().addMapLayer(newLayer)
            newLayer.setContrastEnhancementAlgorithm("StretchToMinimumMaximum")
            newLayer.triggerRepaint()
            #remember path to file
            self.dir = os.path.split(str(f))[0]
          return
        else: # batch mode
          # loop through all the layers in the input
          # dir and write them to the output dir
          # with an added suffix if needed
          myOutputDir = str(self.ui.leOutputDir.text())
          myInputDir = str(self.ui.leInputDir.text())
          mySuffix = str(self.ui.leSuffix.text())
          for myFile in glob.glob(os.path.join(myInputDir, '*.tif')):

            if not os.path.isdir(myOutputDir):
              try:
                os.makedirs(myOutputDir)
              except OSError:
                QMessageBox.warning(self.iface.mainWindow(),
                    "Shaded Relief", "Unable to make the output directory. Check permissions and retry.")
                return 3
            myLayer = QgsRasterLayer(myFile,os.path.basename(myFile))
            myEngine.extentParam = myLayer.extent()
            myEngine.widthParam = myLayer.width()
            myEngine.heightParam = myLayer.height()
            myEngine.noDataParam = myLayer.noDataValue()
            myFileBase = os.path.split(myFile)[1]
            myFileBase = os.path.splitext(myFileBase)[0]
            myOutFileName = os.path.join(myOutputDir,myFileBase + mySuffix + ".tiff")
            myEngine.outFileParam = myOutFileName
            myEngine.sourceFileParam = myLayer.source()
            myEngine.wktParam = myLayer.srs().toWkt()
            del myLayer
            myEngine.run()
            myNewLayer = QgsRasterLayer(str(myOutFileName),os.path.basename(str(myOutFileName)))
            QgsMapLayerRegistry.instance().addMapLayer(myNewLayer)
            myNewLayer.setContrastEnhancementAlgorithm("StretchToMinimumMaximum")
            myNewLayer.triggerRepaint()
        return
        '''


