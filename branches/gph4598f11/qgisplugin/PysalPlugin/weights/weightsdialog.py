"""
This dialog button is made for computing spatial weights in PySal-->Weights-->Compute Weights
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.core import *
from ui_weights import Ui_Weights
import os.path
# create the dialog for zoom to point
class WeightsDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_Weights()
        self.ui.setupUi(self)
        self.dir = os.path.realpath(os.path.curdir)

    @pyqtSignature('') #prevents actions being handled twice
    def on_pbnInput_clicked(self):
        myFile = QFileDialog.getOpenFileName (self, "Select a shapefile")
        self.ui.inputFile.setText(myFile)

    @pyqtSignature('') #prevents actions being handled twice
    def on_pbnOutput_clicked(self):
        myFile = QFileDialog.getSaveFileName(self, "Select a file for the weights matrix")
        self.ui.outputFile.setText(myFile)
###############################################################################################
####                                                                                       #### 
####                                                                                       ####     
####       This is the method we need to implement.  When they click OK this method runs   ####
####                                                                                       #### 
####                                                                                       ####  
###############################################################################################
    def accept(self):
        savefile = str(self.ui.outputFile.text()) #this will be a string like "c:\output"
        ext = str(self.ui.outputExt.currentIndex())
        #these are the options for file extension.  We can say "if ext == GAL:"
        GAL = 0
        GWT = 1
        MAT = 2      
        addX = self.ui.addX.checkState() #this will be 0 or 2 but we can treat it as False/True
        addY = self.ui.addY.checkState() #this will be 0 or 2 but we can treat it as False/True      
        if not self.ui.rbUseActiveLayer.isChecked():
            openfile = str(self.ui.inputFile.text()) #using a saved file this will be a string like "c:\shapefile.shp"
        else:
            pass #using the active layer
        

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


