"""
This dialog window is made for computing spatial markovs in PySal-->spatial_dynamics-->Markov Based methods-->spatial markovs
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.core import *
from ui_spatial_dynamics import Ui_spatial_dynamics #in order to make functions of buttons and comboBoxs
import pysal
from pysal import *
import os.path
from weights.weightsdialog import WeightsDialog # in order to create spatial weights for spatial markov 
import numpy as np # for markov methods

# create the dialog
class spatial_dynamicsdialog(QtGui.QDialog):
    def __init__(self,iface):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from QTDesigner.
        self.ui = Ui_spatial_dynamics() # read GUI 
	self.ui.setupUi(self)
        self.iface = iface
        self.dir = os.path.realpath(os.path.curdir)# Return the canonical path of the specified filename
	        
        self.layers = [] #set a empty list?(is it necessary steps?)
        for i in range(self.iface.mapCanvas().layerCount()):    #this for loop adds current layers
            layer = self.iface.mapCanvas().layer(i)             #to dropdown menu
            self.layers += [layer]
            self.ui.sourceLayer.addItem(layer.name())
            
    @pyqtSignature('') #prevents actions being handled twice
    def on_Loadbutton_clicked(self):
	myFile1 = QFileDialog.getOpenFileName (self, "Select a Datafile","", "comma_separatedfile(*.csv);;textfile(*.txt);;arcgisfile(*.dbf);;multi_usagefile(*.dat)")
        self.ui.Loadline.setText(myFile1)

    @pyqtSignature('') #prevents actions being handled twice
    def on_savedatabutton_clicked(self):
	myFile2 = QFileDialog.getSaveFileName(self, "Save Data After Processing","","comma_separatedfile(*.csv);;textfile(*.txt);;arcgisfile(*.dbf);;multi_usagefile(*.dat)")
        self.ui.savedataline.setText(myFile2)
	#save?
#	if methoddict_classification == 14 or methoddict_standardization == 2:
#		pass
#	else:



    @pyqtSignature('') #prevents actions being handled twice
    def on_inputweightsbutton_clicked(self):
        myFile3 = QFileDialog.getOpenFileName (self, "Select a weightsfile","", "*.gal;;*.gwt;;*.mat")
        self.ui.inputweightsline.setText(myFile3)
    
    @pyqtSignature('') #prevents actions being handled twice
    def on_inputweightscreate_clicked(self):
	dlg = WeightsDialog(self.iface)
        dlg.show()
        results = dlg.exec_()
	self.ui.inputweightsline.setText(myFile3)
	#how to use the file that generates in the weights module?

    @pyqtSignature('') #prevents actions being handled twice
    def on_saveoutputbutton_clicked(self):
        myFile4 = QFileDialog.getSaveFileName(self, "Save Matrixs","","comma_separatedfile(*.csv);;textfile(*.txt);;arcgisfile(*.dbf);;multi_usagefile(*.dat)")
        self.ui.saveoutputline.setText(myFile4)
	#save?
    

#pysal seems not to support all filetypes I know. (write here for backup)"comma_separatedfile(*.csv);;textfile(*.txt);;excelfile(*.xls);;pythonfile(*.py);;accessfile(*.asc);;arcgisfile(*.dbf);;spssfile(*.sav);;multi_usagefile(*.dat)"

###############################################################################################
####                                                                                       #### 
####                                                                                       ####     
####       This is the method we need to implement.  When they click OK this method runs   ####
####                                                                                       #### 
####                                                                                       ####  
###############################################################################################
    
    def accept(self):

#save a result from data processing
	savefile_processing = str(self.ui.savedataline.text()) #this will be a string like "c:\output.filename"
        
	#first comboBox
	classification = self.ui.classcombobox.currentIndex()
	User_Defined = 0
	Equal_Interval = 1
	Natural_Breaks = 2
	Quantiles = 3
	Percentiles = 4
	Standard_Mean = 5
	Maximum_Breaks = 6
	Fisher_Jenks = 7
	Jenks_Caspall = 8
	Jenks_Caspall_Forced = 9
	Jenks_Caspall_Sampled = 10
	Max_P_Classifier = 11
	K_classifiers = 12
	gadf =13
	methoddict_classification ={ 0 : User_Defined, 1 : Equal_Interval, 2 : Natural_Breaks, 3 : Quantiles, 4 : Percentiles, 5 : Standard_Mean, 6 : Maximum_Breaks, 7 : Fisher_Jenks, 8 : Jenks_Caspall, 9 : Jenks_Caspall_Forced, 10 : Jenks_Caspall_Sampled, 11 : Max_P_Classifier, 12 : K_classifiers, 13 : gadf}

	#another comboBox
	standardization = self.ui.standardcombox.currentIndex()
	Yes = 1
	No = 2
	methoddict_standardization = { 0 : Yes, 1 : No}
	

#save matrixs
        savefile_matrix = str(self.ui.saveoutputline.text()) #this will be a string like "c:\output.(GAL OR GWT OR MAT)"



#read data and make it readable, try a csv file first
#classical markov procedures: transfer data from string to array, read data by each columns, data classification, transpose, matrixs 
#spatial markov procedures: transfer data from string to array, read data by each columns, data classification, transpose, standardization, input spatial weights with transform, matrixs
	opendatafile=str(self.ui.Loadline.text())
	
	C=methoddict_classification[classification](opendatafile) #dictionary [index](file), for selecting methods
	S=methoddict_standardization[standardization](opendatafile)
		
	openweightsfile=str(self.ui.inputweightsline.text())
				
	M=methoddict_matrix[matrix](opendatafile)
	
	
	
	
        self.close() #close the dialog window

""" 
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
        """


