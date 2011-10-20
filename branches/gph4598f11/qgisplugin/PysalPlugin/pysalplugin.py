


# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
try:
    #import pysal module
    import pysal

except ImportError:
        dlg = PySalError()
        dlg.ui.webView.setUrl(QUrl("Error.html"))
        user_plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins"
        PySal_dir = user_plugin_dir + "/python/plugins"
        dlg.ui.webView.setUrl(QUrl("file:///%s/resources/error.html" % PySal_dir))
        # show the dialog
        dlg.show()

from about.pysalplugindialog import PysalPluginDialog
from weights.weightsdialog import WeightsDialog

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
            "About Pysal", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.about, SIGNAL("triggered()"), self.runAbout)
        # Add toolbar button and menu item
        self.iface.addPluginToMenu("&Pysal", self.about)

        ############ Create different sublists for the different PySal functions ########
        self.menu1 = QMenu("PySal")

        self.menu2 = QMenu("Computational Geometry")
        self.menu2.setIcon(QIcon(":/plugins/pysalplugin/resources/compgeo_icon.png"))

        self.menu3 = QMenu("Clustering")
        self.menu3.setIcon(QIcon(":/plugins/pysalplugin/resources/cluster_icon.png"))

        self.menu4 = QMenu("ESDA")
        self.menu4.setIcon(QIcon(":/plugins/pysalplugin/resources/esda_icon.png"))

        self.menu5 = QMenu("Spatial Dynamics")
        self.menu5.setIcon(QIcon(":/plugins/pysalplugin/resources/spatdyn_icon.png"))

        self.menu6 = QMenu("Spatial Econometrics")
        self.menu6.setIcon(QIcon(":/plugins/pysalplugin/resources/spatecon_icon.png"))

        self.menu7 = QMenu("Weights")
        self.menu7.setIcon(QIcon(":/plugins/pysalplugin/resources/weights_icon.png"))


        ########### Create actions that will execute the different PySal functions #########
        self.tool1Action = QAction(QIcon(":/plugins/pysalplugin/icon1.png"), \
            "Voroni", self.iface.mainWindow())
        QObject.connect(self.tool1Action, SIGNAL("triggered()"), self.tool1)

        self.tool2Action = QAction(QIcon(":/plugins/pysalplugin/icon2.png"), \
            "Hulls", self.iface.mainWindow())
        QObject.connect(self.tool2Action, SIGNAL("triggered()"), self.tool2)

        self.tool3Action = QAction(QIcon(":/plugins/pysalplugin/icon3.png"), \
            "MST", self.iface.mainWindow())
        QObject.connect(self.tool3Action, SIGNAL("triggered()"), self.tool3)

        self.tool4Action = QAction(QIcon(":/plugins/pysalplugin/icon4.png"), \
            "ARISEL", self.iface.mainWindow())
        QObject.connect(self.tool4Action, SIGNAL("triggered()"), self.tool4)

        self.tool5Action = QAction(QIcon(":/plugins/pysalplugin/icon5.png"), \
            "AZP", self.iface.mainWindow())
        QObject.connect(self.tool5Action, SIGNAL("triggered()"), self.tool5)

        self.tool6Action = QAction(QIcon(":/plugins/pysalplugin/icon6.png"), \
            "max-p", self.iface.mainWindow())
        QObject.connect(self.tool6Action, SIGNAL("triggered()"), self.tool6)

        self.tool7Action = QAction(QIcon(":/plugins/pysalplugin/icon7.png"), \
            "Smoothing", self.iface.mainWindow())
        QObject.connect(self.tool7Action, SIGNAL("triggered()"), self.tool7)

        self.tool8Action = QAction(QIcon(":/plugins/pysalplugin/icon8.png"), \
            "LISA", self.iface.mainWindow())
        QObject.connect(self.tool8Action, SIGNAL("triggered()"), self.tool8)

        self.tool9Action = QAction(QIcon(":/plugins/pysalplugin/icon9.png"), \
            "spatial theta", self.iface.mainWindow())
        QObject.connect(self.tool9Action, SIGNAL("triggered()"), self.tool9)

        self.tool10Action = QAction(QIcon(":/plugins/pysalplugin/icon10.png"), \
            "spatial tau", self.iface.mainWindow())
        QObject.connect(self.tool10Action, SIGNAL("triggered()"), self.tool10)

        self.tool11Action = QAction(QIcon(":/plugins/pysalplugin/icon11.png"), \
            "Spatial Markov", self.iface.mainWindow())
        QObject.connect(self.tool11Action, SIGNAL("triggered()"), self.tool11)

        self.tool12Action = QAction(QIcon(":/plugins/pysalplugin/icon12.png"), \
            "Estimation", self.iface.mainWindow())
        QObject.connect(self.tool12Action, SIGNAL("triggered()"), self.tool12)

        self.tool13Action = QAction(QIcon(":/plugins/pysalplugin/icon13.png"), \
            "Testing", self.iface.mainWindow())
        QObject.connect(self.tool13Action, SIGNAL("triggered()"), self.tool13)

        self.tool14Action = QAction(QIcon(":/plugins/pysalplugin/icon14.png"), \
            "Diagnostics", self.iface.mainWindow())
        QObject.connect(self.tool14Action, SIGNAL("triggered()"), self.tool14)

        self.tool15Action = QAction(QIcon(":/plugins/pysalplugin/icon15.png"), \
            "Simulation", self.iface.mainWindow())
        QObject.connect(self.tool15Action, SIGNAL("triggered()"), self.tool15)

        self.tool16Action = QAction(QIcon(":/plugins/pysalplugin/icon16.png"), \
            "Diagnostics", self.iface.mainWindow())
        QObject.connect(self.tool16Action, SIGNAL("triggered()"), self.tool16)

        self.tool17Action = QAction(QIcon(":/plugins/pysalplugin/icon17.png"), \
            "Compute Matrix", self.iface.mainWindow())
        QObject.connect(self.tool17Action, SIGNAL("triggered()"), self.tool17)

        '''self.tool18Action = QAction(QIcon(":/plugins/pysalplugin/icon18.png"), \
            "GWT", self.iface.mainWindow())
        QObject.connect(self.tool18Action, SIGNAL("triggered()"), self.tool18)

        self.tool19Action = QAction(QIcon(":/plugins/pysalplugin/icon19.png"), \
            "MAT", self.iface.mainWindow())
        QObject.connect(self.tool19Action, SIGNAL("triggered()"), self.tool19)'''

        ########### Organize the functions into the sublists ###########
        self.menu1.addActions([self.about])
        self.menu2.addActions([self.tool1Action,self.tool2Action,self.tool3Action])
        self.menu3.addActions([self.tool4Action,self.tool5Action,self.tool6Action])
        self.menu4.addActions([self.tool7Action,self.tool8Action])
        self.menu5.addActions([self.tool9Action,self.tool10Action,self.tool11Action,])
        self.menu6.addActions([self.tool12Action,self.tool13Action,self.tool14Action,self.tool15Action,self.tool16Action])
        self.menu7.addActions([self.tool17Action])#,self.tool18Action,self.tool19Action]) removed these

        ########### Add these sublists to the main list
        menuBar = self.iface.mainWindow().menuBar()
        menuBar.addMenu(self.menu1)
        self.menu1.addMenu(self.menu2)
        self.menu1.addMenu(self.menu3)
        self.menu1.addMenu(self.menu4)
        self.menu1.addMenu(self.menu5)
        self.menu1.addMenu(self.menu6)
        self.menu1.addMenu(self.menu7)


    def unload(self):
        self.iface.removePluginMenu("Pysal",self.about)
        self.iface.removeToolBarIcon(self.about)

    ############ run methods that performs all the real work#############
    def runAbout(self):
        # create and show the dialog
        dlg = PysalPluginDialog()
        dlg.ui.webView.setUrl(QUrl("file:///%s/about/about.html" % self.PySalPlugin_dir))
        dlg.show()
        results = dlg.exec_()


    def tool1(self):
        raise notImplemented()
    def tool2(self):
        raise notImplemented()
    def tool3(self):
        raise notImplemented()
    def tool4(self):
        raise notImplemented()
    def tool5(self):
        raise notImplemented()
    def tool6(self):
        raise notImplemented()
    def tool7(self):
        raise notImplemented()
    def tool8(self):
        raise notImplemented()
    def tool9(self):
        raise notImplemented()
    def tool10(self):
        raise notImplemented()
    def tool11(self):
        raise notImplemented()
    def tool12(self):
        raise notImplemented()
    def tool13(self):
        raise notImplemented()
    def tool14(self):
        raise notImplemented()
    def tool15(self):
        raise notImplemented()
    def tool16(self):
        raise notImplemented()
    def tool17(self):
        dlg = WeightsDialog()
        dlg.show()
        results = dlg.exec_()
    def tool18(self):
        raise notImplemented()
    def tool19(self):
        raise notImplemented()

class notImplemented(Exception):
    pass

