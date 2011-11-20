"""
This dialog window is made for computing spatial autocorrelation in PySal-->ESDA-->Moran's I
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_spatial_autocorrelation import Ui_spatial_autocorrelation
import pysal
import os.path
from weights.weightsdialog import WeightsDialog # in order to create spatial weights for spatial autocorrelation

# create the dialog
class spatial_autocorrelationDialog(QtGui.QDialog):
    def __init__(self,iface):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from QTDesigner.
        self.ui = Ui_spatial_autocorrelation()
        self.ui.setupUi(self)
        self.iface = iface
        self.dir = os.path.realpath(os.path.curdir)

        self.layers = []
        for i in range(self.iface.mapCanvas().layerCount()):    #this for loop adds current layers
            layer = self.iface.mapCanvas().layer(i)             #to dropdown menu
            self.layers += [layer]
            self.ui.sourceLayer.addItem(layer.name())


    @pyqtSignature('') #prevents actions being handled twice
    def on_inputshpbutton_clicked(self):
        myFile = QFileDialog.getOpenFileName (self, "Select a shapefile","","*.shp")
        self.ui.inputshpline.setText(myFile)
    
    @pyqtSignature('') #prevents actions being handled twice
    def on_Inputweightsbutton_clicked(self):
        myFile2 = QFileDialog.getOpenFileName (self, "Select a weights file","","*.gal")
        self.ui.Inputweightsline.setText(myFile2)
    
    @pyqtSignature('') #prevents actions being handled twice
    def on_Inputweightscreate_clicked(self):
	dlg = WeightsDialog(self.iface)
        dlg.show()
        results = dlg.exec_()
	self.ui.Inputweightsline.setText(myFile2)

    @pyqtSignature('') #prevents actions being handled twice
    def on_outputbutton_clicked(self):
        dlg = QFileDialog()
        myFile3 = dlg.getSaveFileName(self, "Select a file for the weights matrix", "Save Files", "comma_separatedfile(*.csv);;textfile(*.txt);;arcgisfile(*.dbf);;multi_usagefile(*.dat)")
        self.ui.outputline.setText(myFile3)


###############################################################################################
####                                                                                       ####
####                                                                                       ####
####       This is the method we need to implement.  When they click OK this method runs   ####
####                                                                                       ####
####                                                                                       ####
###############################################################################################
    def accept(self):
        savefile = str(self.ui.outputFile.text()) #this will be a string like "c:\output.(GAL OR GWT OR MAT)"
        cont = self.ui.contComboBox.currentIndex()
        Rook = 0
        Queen = 1
        Bishop = 2
        methoddict = { 0: pysal.rook_from_shapefile, 1 : pysal.queen_from_shapefile}

        addNumNeighbors = self.ui.addNumNeighbors.checkState() #this will be 0 or 2 but we can treat it as False/True
        addY = self.ui.addY.checkState() #this will be 0 or 2 but we can treat it as False/True
        layer = None
        if not self.ui.rbUseActiveLayer.isChecked():

            openfile = str(self.ui.inputFile.text()) #using a saved file this will be a string like "c:\shapefile.shp"


            if self.ui.rbContiguity.isChecked(): #use shapefile and rook/queen/bishop
                w = methoddict[cont](openfile)
                output = pysal.open(savefile, 'w')
                output.write(w)
                output.close()
            else: #use shapefile at location: openfile and distance based method
                pass
        else:
            layer = self.layers[self.ui.sourceLayer.currentIndex()]

        if layer:
            if layer.type() == layer.VectorLayer:
                pass


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


