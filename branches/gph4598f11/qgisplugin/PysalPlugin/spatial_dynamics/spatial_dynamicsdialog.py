"""
This dialog window is made for computing spatial markovs in PySal-->spatial_dynamics-->Markov Based methods-->spatial markovs
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.core import *
from ui_spatial_dynamics import ui_spatial_dynamics #in order to make functions of buttons and comboBoxs
import pysal
import os.path
from weights.weightsdialog import WeightsDialog # in order to create spatial weights for spatial markov 
import numpy as np # for markov methods

# create the dialog
class spatial_dynamicsdialog(QtGui.QWidget):
    def __init__(self,iface):
        QtGui.QWidget.__init__(self)
        # Set up the user interface from QTDesigner.
        self.ui = ui_spatial_dynamics() # read GUI 
	self.ui.setupui(self)
        self.iface = iface
        self.dir = os.path.realpath(os.path.curdir)# Return the canonical path of the specified filename
	        
        self.layers = [] #set a empty list?(is it necessary steps?)
        for i in range(self.iface.mapCanvas().layerCount()):    #this for loop adds current layers
            layer = self.iface.mapCanvas().layer(i)             #to dropdown menu
            self.layers += [layer]
            self.ui.sourceLayer.addItem(layer.name())
            
    @pyqtSignature('') #prevents actions being handled twice
    def on_pushButton_3_clicked(self):
	myFile = QFileDialog.getOpenFileName (self, "Select a Datafile","", "comma_separatedfile(*.csv);;textfile(*.txt);;arcgisfile(*.dbf);;multi_usagefile(*.dat)")
        self.ui.lineEdit.setText(myFile)

    @pyqtSignature('') #prevents actions being handled twice
    def on_pushButton_6_clicked(self):
	myFile = QFileDialog.getSaveFileName(self, "Save Data After Processing","","comma_separatedfile(*.csv);;textfile(*.txt);;arcgisfile(*.dbf);;multi_usagefile(*.dat)")
        self.ui.lineEdit_4.setText(myFile)
	#save?

    @pyqtSignature('') #prevents actions being handled twice
    def on_pushButton_4_clicked(self):
        myFile = QFileDialog.getOpenFileName (self, "Input Spatial Weights","", "*.gal;;*.gwt;;*.mat")
        self.ui.lineEdit_2.setText(myFile)
    
    @pyqtSignature('') #prevents actions being handled twice
    def on_pushButton_7_clicked(self):
	dlg = WeightsDialog(self.iface)
        dlg.show()
        results = dlg.exec_()
	self.ui.outputFile.setText(myFile)
	#how to use the file that generates in the weights module?

    @pyqtSignature('') #prevents actions being handled twice
    def on_pushButton_5_clicked(self):
        myFile = QFileDialog.getSaveFileName(self, "Save Matrixs","","comma_separatedfile(*.csv);;textfile(*.txt);;arcgisfile(*.dbf);;multi_usagefile(*.dat)")
        self.ui.lineEdit_3.setText(myFile)
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
	savefile_processing = str(self.ui.lineEdit_4.text()) #this will be a string like "c:\output.filename"
        
	#first comboBox
	classification = self.ui.comboBox.currentIndex()
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
	None_of_the_Above = 14 # how to avoid some keywords, such as none?
	methoddict_classification ={ 0 : User_Defined, 1 : Equal_Interval, 2 : Natural_Breaks, 3 : Quantiles, 4 : Percentiles, 5 : Standard_Mean, 6 : Maximum_Breaks, 7 : Fisher_Jenks, 8 : Jenks_Caspall, 9 : Jenks_Caspall_Forced, 10 : Jenks_Caspall_Sampled, 11 : Max_P_Classifier, 12 : K_classifiers, 13 : gadf, 14 : None_of_the_above}

	#another comboBox
	standardization = self.ui.comboBox_2.currentIndex()
	Yes = 1
	No = 2
	methoddict_standardization = { 0 : Yes, 1 : No}
	

#save matrixs
        savefile_matrix = str(self.ui.lineEdit_3.text()) #this will be a string like "c:\output.(GAL OR GWT OR MAT)"

        #Matrix comboBox
	matrix = self.ui.comboBox_3.currentIndex()
        Transition_Matrix = 0
        Transition_Probabilities = 1
        Steady_State_Distribution = 2
	First_Mean_Passage_Time = 3
	ALL = 4
	methoddict_matrix = { 0 : Transition_Matrix, 1 : Transition_Probabilities, 2 : Steady_State_Distribution, 3 : First_Mean_Passage_Time, 4 : ALL}



#read data and make it readable, try a csv file first
	opendatafile=str(self.ui.lineEdit.text())
	
	C=methoddict_classification[classification](opendatafile) #dictionary [index](file), for selecting methods
	S=methoddict_standardization[standardization](opendatafile)
	
	openweightsfile=str(self.ui.lineEdit_2.text())
	#
	readindata=pysal.open(savefile_matrix, 'w')
	arraydata=array(readindata.write(w).strip())
	readindata.close()

        self.close() #close the dialog window

    def reject(self):
	self.close() #when press the cancel button, then close the window. 

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


