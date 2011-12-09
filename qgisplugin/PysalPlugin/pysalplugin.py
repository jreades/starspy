


# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
try:
    from about.pysalplugindialog import PysalPluginDialog
    #import pysal module
    import pysal

except ImportError:
        dlg = PysalPluginDialog()
        user_plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins"
        PySal_dir = user_plugin_dir + "/PySalPlugin/"
        dlg.ui.webView.setUrl(QUrl("file:///%s//about/error.html" % PySal_dir))
        # show the dialog
        dlg.show()
        results = dlg.exec_()

#from getis_ord.getis_orddialog import getis_ordDialog
from weights.weightsdialog import WeightsDialog
from spatial_dynamics.spatial_dynamicsdialog import spatial_dynamicsdialog
from spatial_autocorrelation.spatial_autocorrelationdialog import spatial_autocorrelationDialog

class PysalPlugin:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        #save reference to plugin folder
        self.user_plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins"
        self.PySalPlugin_dir = self.user_plugin_dir + "/PySalPlugin/"

    def initGui(self):

        # Create about pysal menu item that will start plugin configuration
        self.about = QAction(QIcon(":/plugins/pysalplugin/resources/icon.png"), \
            "About PySAL", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.about, SIGNAL("triggered()"), self.runAbout)
        # Add toolbar button and menu item
        self.iface.addPluginToMenu("&PySAL", self.about)

        ############ Create different sublists for the different PySal functions ########
        self.menu1 = QMenu("PySAL")



##############################################
###  Set up the Spatial Dynamics Menu Tree  ##
##############################################

        self.menu2 = QMenu("Spatial Dynamics") #Main Spatial Dynamics Menu
        self.menu2.setIcon(QIcon(":/plugins/pysalplugin/resources/spatdyn_icon.png")) #Give it a colorful Icon

        #self.menu21 = QMenu("Markov Based Methods") #First SubMenu

### start of items in first Submenu
        self.classicMarkovAction = QAction(QIcon(":/plugins/pysalplugin/icon1.png"), \
            "Classic Markov", self.iface.mainWindow())
        QObject.connect(self.classicMarkovAction, SIGNAL("triggered()"), self.classicMarkov)

        self.spatialMarkovAction = QAction(QIcon(":/plugins/pysalplugin/icon2.png"), \
            "Spatial Markov", self.iface.mainWindow())
        QObject.connect(self.spatialMarkovAction, SIGNAL("triggered()"), self.spatialMarkov)

        self.lisaMarkovAction = QAction(QIcon(":/plugins/pysalplugin/icon3.png"), \
            "LISA Markov", self.iface.mainWindow())
        QObject.connect(self.lisaMarkovAction, SIGNAL("triggered()"), self.lisaMarkov)
### End of items in first submenu

        self.menu22 = QMenu("Rank Based Methods") #Second SubMenu

### start of items in Second Submenu

        self.spRankCorAction = QAction(QIcon(":/plugins/pysalplugin/icon4.png"), \
            "Spatial Rank Correlation", self.iface.mainWindow())
        QObject.connect(self.spRankCorAction, SIGNAL("triggered()"), self.spRankCor)

        self.rankDecompAction = QAction(QIcon(":/plugins/pysalplugin/icon5.png"), \
            "Rank Decomposition", self.iface.mainWindow())
        QObject.connect(self.rankDecompAction, SIGNAL("triggered()"), self.rankDecomp)

### End of items in Second submenu

        self.menu23 = QMenu("Space-Time Interaction Tests")  # Third Submenu
### start of items in Third Submenu

        self.knoxTestAction = QAction(QIcon(":/plugins/pysalplugin/icon6.png"), \
            "Knox Test", self.iface.mainWindow())
        QObject.connect(self.knoxTestAction, SIGNAL("triggered()"), self.knoxTest)

        self.mantelTestAction = QAction(QIcon(":/plugins/pysalplugin/icon7.png"), \
            "Mantel Test", self.iface.mainWindow())
        QObject.connect(self.mantelTestAction, SIGNAL("triggered()"), self.mantelTest)

        self.jacquezTestAction = QAction(QIcon(":/plugins/pysalplugin/icon8.png"), \
            "Jacquez Test", self.iface.mainWindow())
        QObject.connect(self.jacquezTestAction, SIGNAL("triggered()"), self.JacquezTest)
## End of items in Third Submenu

        self.menu2.addActions([self.spatialMarkovAction])
        #self.menu21.addActions([self.spatialMarkovAction])  #put three tools in first Submenu
        #self.menu22.addActions([self.spRankCorAction,self.rankDecompAction]) #Put two tools in second Submenu
        #self.menu23.addActions([self.knoxTestAction,self.mantelTestAction,self.jacquezTestAction]) #Put three tools in third submenu
        #self.menu2.addMenu(self.menu21) #add these submenus to the Spatial Dynamics Menu
        #self.menu2.addMenu(self.menu22) #add these submenus to the Spatial Dynamics Menu
        #self.menu2.addMenu(self.menu23) #add these submenus to the Spatial Dynamics Menu

#####################################
### Set up the Weights Menu Tree  ###
#####################################

        self.menu3 = QMenu("Weights")  #Main Weights Menu
        self.menu3.setIcon(QIcon(":/plugins/pysalplugin/resources/weights_icon.png"))

        self.computeMatrixAction = QAction(QIcon(":/plugins/pysalplugin/icon9.png"), \
            "Compute Matrix", self.iface.mainWindow())
        QObject.connect(self.computeMatrixAction, SIGNAL("triggered()"), self.computeMatrix)

        self.menu3.addActions([self.computeMatrixAction])

#############################################
### Set up the Autocorrelation Menu Tree  ###
#############################################

        self.menu4 = QMenu("ESDA")  #Main ESDA Menu
        self.menu4.setIcon(QIcon(":/plugins/pysalplugin/resources/esda_icon.png"))

        self.computeMatrixAction = QAction(QIcon(":/plugins/pysalplugin/icon8.png"), \
            "Moran's I", self.iface.mainWindow())
        QObject.connect(self.computeMatrixAction, SIGNAL("triggered()"), self.MoransI)

        self.menu4.addActions([self.computeMatrixAction])

#############################################
### Set up the Getis-Ord Menu Tree  ###
#############################################
        '''
        self.menu5 = QMenu("Getis-Ord")
        #Main Getis Menu
        self.menu5.setIcon(QIcon(":/plugins/pysalplugin/resources/esda_icon.png"))

        self.computeMatrixAction = QAction(QIcon(":/plugins/pysalplugin/icon8.png"), \
            "Getis-Ord", self.iface.mainWindow())
        QObject.connect(self.computeMatrixAction, SIGNAL("triggered()"), self.getis_ord)

        self.menu5.addActions([self.computeMatrixAction])
        '''


################################################################
### Pack all the menus together and add them to QGIS MenuBar ###
################################################################
        self.menu1.addActions([self.about])
        self.menu1.addMenu(self.menu2)
        self.menu1.addMenu(self.menu3)
	self.menu1.addMenu(self.menu4)
        #self.menu1.addMenu(self.menu5)
        menuBar = self.iface.mainWindow().menuBar()
        menuBar.addMenu(self.menu1)




    def unload(self):
        self.iface.removePluginMenu("Pysal",self.about)
        self.iface.removeToolBarIcon(self.about)

    ############ run methods that performs all the real work#############
    def runAbout(self):
        '''When users click on the 'About' Action'''
        # create and show the dialog
        dlg = PysalPluginDialog()
        dlg.ui.webView.setUrl(QUrl("file:///%s/about/about.html" % self.PySalPlugin_dir))
        dlg.show()
        results = dlg.exec_()


    def classicMarkov(self):
        raise notImplemented()

    def spatialMarkov(self):
        dlg = spatial_dynamicsdialog(self.iface)
        dlg.show()
        results = dlg.exec_()
	
    def lisaMarkov(self):
        raise notImplemented()

    def spRankCor(self):
        raise notImplemented()

    def rankDecomp(self):
        raise notImplemented()

    def knoxTest(self):
        raise notImplemented()

    def mantelTest(self):
        raise notImplemented()

    def JacquezTest(self):
        raise notImplemented()

    def MoransI(self):
	dlg = spatial_autocorrelationDialog(self.iface)
        dlg.show()
        results = dlg.exec_()

    def computeMatrix(self):
        dlg = WeightsDialog(self.iface)
        dlg.show()
        results = dlg.exec_()
''' def getis_ord(self):
        dlg = getis_ordDialog(self.iface)
        dlg.show()
        results = dlg.exec_()
'''

class notImplemented(Exception):
    pass

