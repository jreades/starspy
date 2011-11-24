"""
This dialog window is made for computing spatial autocorrelation in PySal-->ESDA-->Moran's I
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_spatial_autocorrelation import Ui_spatial_autocorrelation
import pysal
from pysal import *
import os.path
import subprocess #for Chinese characters?
from weights.weightsdialog import WeightsDialog # in order to create spatial weights for spatial autocorrelation
import numpy as np # for Moran's I module
from weights.ui_weights import Ui_Weights

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

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
	for i in range(self.iface.mapCanvas().layerCount()):    #this for loop adds current layers; layercount: current map layer 
            layer = self.iface.mapCanvas().layer(i)             #to dropdown menu
            self.layers += [layer]
            self.ui.activecombobox.addItem(layer.name())


    @pyqtSignature('') #prevents actions being handled twice
    def on_inputshpbutton_clicked(self):
        myFile = QFileDialog.getOpenFileName (self, "Select a shapefile","","*.shp")
        self.ui.inputshpline.setText(myFile)

	#create a new combobox(1)use pysal to open file(2) read  in
	openfile=str(self.ui.inputshpline.text()) 
	f=pysal.open(openfile)
	opendbf=openfile[:-3] + "dbf" #open the same file only with dbf 
	f_dbf = pysal.open(opendbf)
	self.fileheader=f_dbf.header #find columns, already in a list
	
	#self.columns=[]
	for i in self.fileheader: #i is in a string
		self.ui.selectcombobox.addItem(i)
		#self.columns+=fileheader #can not use i+=1, due to i is a string, not a list
	
	
    @pyqtSignature('') #prevents actions being handled twice
    def on_Inputweightsbutton_clicked(self):
        myFile2 = QFileDialog.getOpenFileName (self, "Select a weights file","","*.gal")
        self.ui.Inputweightsline.setText(myFile2)
    
    @pyqtSignature('') #prevents actions being handled twice
    def on_Inputweightscreate_clicked(self):
	dlg = WeightsDialog(self.iface)
        dlg.show()
        results = dlg.exec_()
	if self.ui.Inputweightsline != None: #how to call variable from other files?
		#self.ci=WeightsDialog(WeightsDialog.accept)
		#myfile4=WeightsDialog.accept(savefile)
		#self.ui.Inputweightsline.setText(myfile4)
		pass
	else:
		pass

    @pyqtSignature('') #prevents actions being handled twice
    def on_outputbutton_clicked(self):
	dlg = QFileDialog()
	myFile3 = dlg.getSaveFileName(self, "Save Output", "", "comma_separatedfile(*.csv)")
	myFile3 += dlg.selectedNameFilter()[0] #?
        self.ui.outputline.setText(myFile3[0:-1])
   
###############################################################################################
####                                                                                       ####
####                                                                                       ####
####       This is the method we need to implement.  When they click OK this method runs   ####
####                                                                                       ####
####                                                                                       ####
###############################################################################################
    def accept(self):
        	
	#normalradioButton = self.ui.normalradioButton.checkState() #this will be 0 or 2 but we can treat it as False/True
        #randomradiobutton = self.ui.randomradiobutton.checkState() #this will be 0 or 2 but we can treat it as False/True

	if self.ui.savedshpradio.isChecked(): #when selecting saved shp
		openfile=str(self.ui.inputshpline.text()) #make a string of saved file
		savefile = str(self.ui.outputline.text()) #this will be a string like "c:\output.(.csv)"
		weightsfile=str(self.ui.Inputweightsline.text())
			
		if self.ui.MoranIcheck.checkState(): #run moran's I value
			np.random.seed(10) #? Is this step necessary?
			f=pysal.open(openfile) #read a shp file, not need to read
			w=pysal.open(weightsfile).read() #read a weights file
			opendbf=openfile[:-3] + "dbf" #open the same file only with dbf 
			f_dbf = pysal.open(opendbf) #read the dbf attribute file
			fileheader=f_dbf.header

			#select a column and let it function
			
			columnindex=self.ui.selectcombobox.currentText() #when select a column
			y=np.array(f_dbf.by_col[columnindex]) #change into array, by_col function is only for dbf file
			
			mi=pysal.Moran(y,w) #value of Moran's I
			MI=mi.I #list
			
			savestring=str(MI)
			#savestring=','.join(str(n) for n in MI) #change from list to string for saving
			output=pysal.open(savefile, 'w')
			output.write(savestring)
			output.close()
			
			if self.ui.normalradioButton.isChecked(): #under the assumption of normal distribution 
				if self.ui.expectedcheckbox.checkState():
					NE=mi.EI
					savestring1=columnindex+'\n'+'Moron\'s I'+','+savestring+'\n'+'\n'+'Normality Assumption'+'\n'+'Expected Value'+','+str(NE)
					output=pysal.open(savefile, 'w')
					output.write(savestring1)
					output.close()
				elif self.ui.variancecheckbox.checkState():
					NV=mi.VI_norm
					savestring2=columnindex+'\n'+'Moron\'s I'+','+savestring+'\n'+'\n'+'Normality Assumption'+'\n'+'Variance'+','+str(NV)
					output=pysal.open(savefile, 'w')
					output.write(savestring2)
					output.close()
				elif self.ui.standardcheckbox.checkState():
					NS=mi.seI_norm
					savestring3=columnindex+'\n'+'Moron\'s I'+','+savestring+'\n'+'\n'+'Normality Assumption'+'\n'+'Standard Deviation'+','+str(NS)
					output=pysal.open(savefile, 'w')
					output.write(savestring3)
					output.close()
				elif self.ui.Zcheckbox.checkState():
					Nz=mi.z_norm
					savestring4=columnindex+'\n'+'Moron\'s I'+','+savestring+'\n'+'\n'+'Normality Assumption'+'\n'+'z-value'+','+str(Nz)
					output=pysal.open(savefile, 'w')
					output.write(savestring4)
					output.close()
				elif self.ui.Pcheckbox.checkState():
					Np=mi.p_norm
					savestring5=columnindex+'\n'+'Moron\'s I'+','+savestring+'\n'+'\n'+'Normality Assumption'+'\n'+'p-value'+','+str(Np)
					output=pysal.open(savefile, 'w')
					output.write(savestring5)
					output.close()
				else:
					pass

			elif self.ui.randomradiobutton.isChecked(): #under the assumption of random distribution
				if self.ui.variancecheckbox.checkState():
					RV=mi.VI_rand
					savestring6=columnindex+'\n'+'Moron\'s I'+','+savestring+'\n'+'\n'+'Randomization Assumption'+'\n'+'Variance'+','+str(RV)
					output=pysal.open(savefile, 'w')
					output.write(savestring6)
					output.close()
				elif self.ui.standardcheckbox.checkState():
					RS=mi.seI_rand
					savestring7=columnindex+'\n'+'Moron\'s I'+','+savestring+'\n'+'\n'+'Randomization Assumption'+'\n'+'Standard Deviation'+','+str(RS)
					output=pysal.open(savefile, 'w')
					output.write(savestring7)
					output.close()
				elif self.ui.Zcheckbox.checkState():
					Rz=mi.z_rand
					savestring8=columnindex+'\n'+'Moron\'s I'+','+savestring+'\n'+'\n'+'Randomization Assumption'+'\n'+'z-value'+','+str(Rz)
					output=pysal.open(savefile, 'w')
					output.write(savestring8)
					output.close()
				elif self.ui.Pcheckbox.checkState():
					Rp=mi.p_rand
					savestring9=columnindex+'\n'+'Moron\'s I'+','+savestring+'\n'+'\n'+'Randomization Assumption'+'\n'+'p-value'+','+str(Rp)
					output=pysal.open(savefile, 'w')
					output.write(savestring9)
					output.close()
				else:
					pass
			
			else:
				pass
			
		else:
			return	#differences between pass and return: "pass" just skip the code, while "return" will terminate the program

	elif self.ui.activecombobox.isChecked(): #when selecting active shp? import pysal?
		layer = self.layers[self.ui.activecombobox.currentIndex()]
		if layer.type() == layer.VectorLayer:
                	pass
            	elif layer.type() == layer.RasterLayer:
                	pass
		else: raise "unknown layer type"
	
	

	self.close() #close the dialog window


"""
        #normalradioButton = self.ui.normalradioButton.checkState() #this will be 0 or 2 but we can treat it as False/True
        #randomradiobutton = self.ui.randomradiobutton.checkState() #this will be 0 or 2 but we can treat it as False/True
        layer = None #for Active Layer in Map
	if not self.ui.rbUseActiveLayer.isChecked(): #not Active layer in map

            openfile = str(self.ui.inputshpline.text()) #using a saved file this will be a string like "c:\shapefile.shp"


            if self.ui.MoranIcheck.checkState(): #check Moran I as one of outputs
            #w = methoddict[cont](openfile)
            	output = pysal.open(openfile) #open by pysal
	    	output.write(savefile) #save a new file
            	output.close()
            else: #use shapefile at location: openfile and distance based method
                pass
        else:
            layer = self.layers[self.ui.activecombobox.currentIndex()]

        #if layer: #?
        #    if layer.type() == layer.VectorLayer:
        #        pass


        #qgis api http://doc.qgis.org/stable/annotated.html



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


