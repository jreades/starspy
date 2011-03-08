import wx
import wx.lib.mixins.treemixin as treemixin

COLOR_SAMPLE_WIDTH = 20
COLOR_SAMPLE_HEIGHT = 20

class FileDropTarget(wx.FileDropTarget):
    """
    Generic FileDropTarget.

    Expect obj to be an instance of mapModel
    """
    def __init__(self, obj):
        wx.FileDropTarget.__init__(self)
        self.obj = obj
    def OnDropFiles(self,x,y,filenames):
        for fname in filenames:
            print "Dropped: ",fname, self.obj.addPath(fname)
class LayersControl(treemixin.DragAndDrop,treemixin.VirtualTree,wx.TreeCtrl):
    __mapModel = None
    def __get_mapModel(self):
        return self.__mapModel
    def __set_mapModel(self,value):
        self.__mapModel = value
        self.__mapModel.addListener(self.update)
        self.__imgList = wx.ImageList(COLOR_SAMPLE_WIDTH,COLOR_SAMPLE_HEIGHT)
        self.fdt = FileDropTarget(value)
        self.SetDropTarget(self.fdt)
        #self.AssignImageList(self.__imgList)
        self.update()
    mapModel = property(fget=__get_mapModel,fset=__set_mapModel)
    @property
    def layer(self):
        try:
            idx = self.GetIndexOfItem(self.GetSelection())
            return idx[0]
        except:
            return None
    def update(self,mdl=None,tag=None):
        if tag=='layers' or not tag:
            self.__imgList.RemoveAll()
            self.__layerColor2Image = {}
            if mdl and mdl.layers:
                c = 0
                for i,layer in enumerate(mdl.layers):
                    for j in xrange(len(layer.colors)):
                        r,g,b = layer.colors[j]
                        bitmap = wx.EmptyBitmapRGBA(COLOR_SAMPLE_WIDTH,COLOR_SAMPLE_HEIGHT,r,g,b,255)
                        self.__imgList.Add(bitmap)
                        self.__layerColor2Image[(i,j)]=c
                        c+=1
            self.SetImageList(self.__imgList)
            self.RefreshItems()
    def OnGetChildrenCount(self,index):
        if not self.mapModel: return 0
        if index == ():
            return len(self.mapModel)
        elif len(index) == 1:
            return len(self.mapModel.layers[index[0]].colors)
        return 0
    def OnGetItemText(self,index,column=0):
        if not self.mapModel: return ""
        if len(index) == 1:
            return self.mapModel.layers[index[0]].name
        elif len(index) == 2:
            return "Class %d"%index[1]
        return ""
    def OnGetItemImage(self,index,which=0,column=0):
        if index in self.__layerColor2Image:
            return self.__layerColor2Image[index]
        return -1
    def OnDrop(self,dropItem,dragItem):
        #print "OnDrop(%r,%r)"%(dropItem,dragItem)
        if not self.mapModel: return
        drop = self.GetIndexOfItem(dropItem)
        drag = self.GetIndexOfItem(dragItem)
        #print "dropped ", drag," on ",drop
        drag = drag[0]
        if drop == ():
            self.mapModel.moveLayer(drag,len(self.mapModel.layers))
        else:
            self.mapModel.moveLayer(drag,drop[0])
    def IsValidDragItem(self,dragItem):
        #print "IsValidDragItem(%r)"%dragItem
        index = self.GetIndexOfItem(dragItem)
        if len(index) == 1:
            return True
        return False
    def IsValidDropTarget(self,dropTarget):
        #print "IsValidDropTarget(%r)"%dropTarget
        return True
