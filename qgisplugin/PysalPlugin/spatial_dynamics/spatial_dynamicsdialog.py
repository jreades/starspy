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
            if layer.type() ==layer.VectorLayer:
		self.ui.activecombobox.addItem(layer.name()) #set dynamic labels in the combobox
	    elif layer.type == layer.RasterLayer:
	    	pass
	    else:
		pass


    @pyqtSignature('') #prevents actions being handled twice
    def on_inputbutton_clicked(self):
	myFile1 = QFileDialog.getOpenFileName(self, "Select a shapefile","","shapefile(*.shp);;comma_separatedfile(*.csv)")
	if self.ui.inputbutton != None:
		self.ui.inputline.setText(myFile1)
	else:
		pass

	#create a new combobox(1)use pysal to open file(2) read  in
    #for saved shapefile to show columns
	openfile=str(self.ui.inputline.text()) 
	f=pysal.open(openfile)
	#opendbf=openfile[:-3] + "dbf" #open the same file only with dbf 
	#f_dbf = pysal.open(opendbf)
	self.fileheader=f.header #find columns, already in a list
	
	for i in self.fileheader: #i is in a string
		self.ui.startcombobox.addItem(i)
		self.ui.endcombobox.addItem(i)


    #@pyqtSignature('') #prevents actions being handled twice
    #def on_activecombobox_currentIndexChanged(self):	#when selecting	any shapefile from active layers, but do not know how to get the file path from active layers?
    #for active layer to show columns
    	#self.ui.activecombobox.currentIndexChanged(int)
	#QMessageBox.information(self,"Vector file","Layer is ok")
	#self.ui.activecombobox.text()
    	#openfile=str(self.ui.activecombobox.getPath().Text())
	#f=pysal.open(openfile)
	#opendbf=openfile[:-3] + "dbf" #open the same file only with dbf 
	#f_dbf = pysal.open(opendbf)
	#self.fileheader=f.header #find columns, already in a list
	
	#for i in self.fileheader: #i is in a string
	#	self.ui.selectcombobox.addItem(i)


    @pyqtSignature('') #prevents actions being handled twice
    def on_inputweightsbutton_clicked(self):
        myFile2 = QFileDialog.getOpenFileName (self, "Select a weights file","","*.gal")
        self.ui.inputweightsline.setText(myFile2)
    
    @pyqtSignature('') #prevents actions being handled twice
    def on_inputweightscreate_clicked(self):
	dlg = WeightsDialog(self.iface)
        dlg.show()
        results = dlg.exec_()
	if self.ui.inputweightscreate != None: #how to call variable from other files?
		#self.ci=WeightsDialog(WeightsDialog.accept)
		#myfile4=WeightsDialog.accept(savefile)
		#self.ui.Inputweightsline.setText(myfile4)
		pass
	else:
		pass

    @pyqtSignature('') #prevents actions being handled twice
    def on_saveoutputbutton_clicked(self):
	dlg = QFileDialog()
	myFile3 = dlg.getSaveFileName(self, "Save Matrix", "", "comma_separatedfile(*.csv)")
	myFile3 += dlg.selectedNameFilter()[0] #?
        self.ui.saveoutputline.setText(myFile3[0:-1])

#pysal seems not to support all filetypes I know. (write here for backup)"comma_separatedfile(*.csv);;textfile(*.txt);;excelfile(*.xls);;pythonfile(*.py);;accessfile(*.asc);;arcgisfile(*.dbf);;spssfile(*.sav);;multi_usagefile(*.dat)"

###############################################################################################
####                                                                                       #### 
####                                                                                       ####     
####       This is the method we need to implement.  When they click OK this method runs   ####
####                                                                                       #### 
####                                                                                       ####  
###############################################################################################
#classical markov procedures: transfer data from string to array, read data by each columns, data classification, transpose, matrixs 
#spatial markov procedures: transfer data from string to array, read data by each columns, data classification, transpose, standardization, input spatial weights with transform, matrix

    def accept(self):
	if self.ui.savedshpradio.isChecked(): #when selecting saved shp
		openfile=str(self.ui.inputline.text()) #make a string of saved file
		savefile = str(self.ui.saveoutputline.text()) #this will be a string like "c:\output.(.csv)"
		weightsfile=str(self.ui.inputweightsline.text())
		if self.ui.matrixcheckbox.checkState():

		#run spatial Matrix
			f=pysal.open(openfile) #read a shp file, not need to read
			w=pysal.open(weightsfile).read() #read a weights file
			#opendbf=openfile[:-3] + "dbf" #open the same file only with dbf 
			#f_dbf = pysal.open(opendbf) #read the dbf attribute file
			fileheader=f.header

		#select a column and let it function
			columnindex1=int(self.ui.startcombobox.currentText()) #when select a column
			columnindex2=int(self.ui.endcombobox.currentText())+1 #avoid random selection?
		
		#change into array, by_col function is only for dbf file
			pci=np.array([f.by_col[str(y)] for y in range(columnindex1, columnindex2)]) 
			#only number? by_col works for dbf, but the sample data use csv?

			#q5 = np.array([pysal.Quantiles(y).yb for y in pci]) #map classification?

			pci=pci.transpose()
			rpci = pci / (pci.mean(axis = 0)) #standardization
			w.transform='r'
		
			sm=pysal.Spatial_Markov(rpci, w, fixed=True, k=5) #what did k mean? does it equal to quantile?
		
		#results
			transition_matrix=sm.p #numpy.matrixlib.defmatrix.matrix
			results = "\n".join([ "\t".join(map(str,row)) for row in transition_matrix])
			#results=repr(transition_matrix).replace('matrix',' ')
			#results='      '+''.join([ c for c in s if c not in ('(', ')','[',']',',')])
			output=pysal.open(savefile,'w')
			output.write(results)
			output.close

			if self.ui.probabilitiescheckbox.checkState():
				for p in sm.P:
					transition_probabilities=p
					#results=repr(transition_probabilities).replace('matrix',' ')
					#results='      '+''.join([ c for c in s if c not in ('(', ')','[',']',',')])
					results = "\n".join([ "\t".join(map(str,row)) for row in transition_probabilities])
					output=pysal.open(savefile,'w')
					output.write(results)
					output.close
			#else:
			#	pass

			elif self.ui.steadystatecheckbox.checkState():
				steady_state_distribution=sm.S
				#results=repr(Steady_State_Distribution).replace('matrix',' ')
				#results='      '+''.join([ c for c in s if c not in ('(', ')','[',']',',')])
				results = "\n".join([ "\t".join(map(str,row)) for row in steady_state_distribution])
				output=pysal.open(savefile,'w')
				output.write(results)
				output.close
			#else:
				#pass

			elif self.ui.firstcheckbox.checkState():
				for f in sm.F:
					first_mean_passage_time=f
					#resultss=repr(first_mean_passage_time).replace('matrix',' ')
					#results='      '+''.join([ c for c in s if c not in ('(', ')','[',']',',')])
					results = "\n".join([ "\t".join(map(str,row)) for row in first_mean_passage_time])
					output=pysal.open(savefile,'w')
					output.write(results)
					output.close
			else:
				pass

		else:
			pass
	
	elif self.ui.activecombobox.isChecked(): #when selecting active shp and then import pysal
		layer = self.layers[self.ui.activecombobox.currentIndex()] #select a shp layer
		savefile = str(self.ui.outputline.text())
		weightsfile=str(self.ui.Inputweightsline.text())
		
		pass
		
		#if 
			#f=pysal.open() #calculate Moran's I and other value, but do not know how to get the file path from active layers?
		#else:
		#	return

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


