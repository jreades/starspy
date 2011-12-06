"""

This dialog window is made for computing spatial autocorrelation in PySal-->ESDA-->Getis-Ord General G
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_getis_ord import Ui_getis_ord



import pysal
from pysal import *
import os.path
from weights.weightsdialog import WeightsDialog
from pysal.esda.getisord import G

#to create spatial weights for spatial autocorrelation

import numpy as np 
from weights.ui_weights import Ui_Weights

# create the dialog for GETIS
class getis_ordDialog(QtGui.QDialog):
    def __init__(self,iface):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_getis_ord()  
        self.ui.setupUi(self)
    
        self.iface = iface  # DUNG O DAY, LOI O DAY
        self.dir = os.path.realpath(os.path.curdir)
        self.layers = []  	    
        for i in range(self.iface.mapCanvas().layerCount()):   
                layer = self.iface.mapCanvas().layer(i) #to dropdown menu #get the currently active layer
                self.layers += [layer] 

                if layer.type() ==layer.VectorLayer:
			self.ui.activecombobox.addItem(layer.name()) #set dynamic labels in the combobox
	
                elif layer.type == layer.RasterLayer:
		            pass
		
                else:
                    pass


    @pyqtSignature('') #prevents actions being handled twice
    def on_InputButton_clicked(self):     	
        NFile = QFileDialog.getOpenFileName (self, "Select a shapefile","","*.shp")
        self.ui.InputTextLine.setText(NFile)


#create a new combobox(1)use pysal to open file(2) read  in
    #for saved shapefile to show columns
        openfile=str(self.ui.InputTextLine.text())         #co the PHAI SUA HANG TREN!
        
        f=pysal.open(openfile)
        opendbf=openfile[:-3] + "dbf" #open the same file only with dbf 
        f_dbf = pysal.open(opendbf)
        self.fileheader=f_dbf.header #find columns, already in a list
# CO THE CAN MO LAI

    @pyqtSignature('') #prevents actions being handled twice
    def on_activecombobox_currentIndexChanged(self):	
         #for active layer to show columns
    	self.ui.activecombobox.currentIndexChanged(int)
    	QMessageBox.information(self,"Vector file","Layer is ok")
	    
        self.ui.activecombobox.text()    

    	openfile=str(self.ui.activecombobox.getPath().Text())
        f=pysal.open(openfile)
        #opendbf=openfile[:-3] + "dbf" #open the same file only with dbf 
        #f_dbf = pysal.open(opendbf)
        self.fileheader=f.header #find columns, already in a list THU VOI TURONG HOP KHONG CO FILE DBF
	
        for i in self.fileheader: 
	            self.ui.selectcombobox.addItem(i)
	
    @pyqtSignature('') #prevents actions being handled twice
    def on_InputWeightsButton_clicked(self):
        NFile2 = QFileDialog.getOpenFileName (self, "Select a weights file","","*.gal;;*.gwt;;*.mat")
        self.ui.InputWeightsTextLine.setText(NFile2)
    
    @pyqtSignature('') #prevents actions being handled twice
    def on_CreateWeightsButton_clicked(self):
	dlg = WeightsDialog(self.iface)
        dlg.show()
        results = dlg.exec_()
	if self.ui.InputWeightsTextLine != None: 
        
            pass
	else:
		pass

    @pyqtSignature('') #prevents actions being handled twice
    def on_OutputButton_clicked(self):
	dlg = QFileDialog()
	NFile3 = dlg.getSaveFileName(self, "Save Output", "", "comma_separatedfile(*.csv)")
	NFile3 += dlg.selectedNameFilter()[0] 
        self.ui.OuputTextLine.setText(NFile3[0:-1])

###############################################################################################
####                                                                                       ####
####                                                                                       ####
####       This is the method we need to implement.  When they click OK this method runs   ####
####                                                                                       ####
####                                                                                       ####
###############################################################################################

def accept(self):
        	
    if self.ui.SavedRadio.isChecked():
        # if selecting saved shp   TAI  SAO PHAI SHAVED SHAPE FILE?
		openfile=str(self.ui.InputTextLine.text()) #make a string of saved file
		savefile = str(self.ui.OuputTextLine.text()) #this will be a string like "c:\output.(.csv)"
		weightsfile=str(self.ui.InputWeightsTextLine.text())

		
		if  self.ui.GetisOrdcheck.checkState():#if check run Getis Ord
			np.random.seed(10) #
			#f=pysal.open(openfile) #
			w=pysal.open(weightsfile).read() #read a weights fil 
                opendbf=openfile[:-3] + "csv" # only with dbf 
                f_dbf = pysal.open(opendbf) #read the dbf attribute file
    	        fileheader=f_dbf.header
           
           #select a column and let it function
    	        columnindex=self.ui.selectcombobox.currentText()  #when select a field
	        y=np.array(f_dbf.by_col[columnindex]) #change into array, 
                threshDist = float(self.ui.ThreshDistLine.text())
            #calculate value of getis ord
                dist_w = pysal.threshold_binaryW_from_shapefile(openfile,threshDist)
                dist_w.transform = "B"
                g = G(y, self.dist_w)
			
          			
                savestring=str(g.G)
    #savestring=','.join(str(n) for n in g) #change from list to string for saving
                output=pysal.open(savefile, 'w')
                output.write(savestring) 
                output.close()
			
                if self.ui.Zvalue.checkState():
					gZ=g.z_norm
					savestring2=columnindex+'\n'+'Getis-Ord'+','+savestring+'\n'+'\n'+'\n'+'z-value'+','+str(gZ)
					output=pysal.open(savefile, 'w')
					output.write(savestring2)
					output.close()
				    
                else:
					pass
				
                if self.ui.Pvalue.checkState():
					gP=g.p_norm
					savestring3=columnindex+'\n'+'Getis-Ord'+','+savestring+'\n'+'\n'+'\n'+'p-value'+','+str(gP)
					output=pysal.open(savefile, 'w')
					output.write(savestring3)
					output.close()
                else:
					pass
             
    elif self.ui.activecombobox.isChecked(): #when selecting active shp and then import pysal
		layer = self.layers[self.ui.activecombobox.currentIndex()] #select a shp layer
		savefile = str(self.ui.OuputTextLine.text())
		weightsfile=str(self.ui.InputWeightsTextLine.text())
		
		pass
		
		if self.ui.GetisOrdcheck.checkState(): 
			np.random.seed(10)
			#f=pysal.open() #calculate Moran's I and other value, but do not know how to get the file path from active layers?
		else:
			return
	
    self.close() #close the dialog            
            
            # print g.G
            #0.103483215873
            #print g.EG
            #0.0752580752581
            #print g.z_norm
            #3.28090342959
            #print g.p_norm
            #0.000517375830488
            
            #g = G(y, dist_w, permutations = 9999)
            #print g.p_z_sim
            #0.00061476957041
            #print g.p_sim
            #0.0061
            




