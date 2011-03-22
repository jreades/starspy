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
    def __init__(self,parent,mapModel,size=(150,400)):
        # Note: treemixin seems to take care of the TreeCtrl __init__
        treemixin.DragAndDrop.__init__(self,parent,size=size)
        self.mapCanvas = parent
        self.mapModel = mapModel
        self.dragging = False
        self.Bind(wx.EVT_TREE_ITEM_MENU,self.onMenu)
        self.Bind(wx.EVT_TREE_SEL_CHANGED,self.onSelect)
        self.Bind(wx.EVT_TREE_SEL_CHANGING,self.onSelecting)
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
    #@property
    #def layer(self):
    #    try:
    #        idx = self.GetIndexOfItem(self.GetSelection())
    #        return idx[0]
    #    except:
    #        return None
    def update(self,mdl=None,tag=''):
        if 'classification' in tag or tag=='layers' or not tag:
            self.__imgList.RemoveAll()
            self.__layerColor2Image = {}
            if mdl and mdl.layers:
                c = 0
                for i,layer in enumerate(mdl.layers):
                    for j in xrange(len(layer.colors)):
                        r,g,b,a = layer.colors[j]
                        bitmap = wx.EmptyBitmapRGBA(COLOR_SAMPLE_WIDTH,COLOR_SAMPLE_HEIGHT,r,g,b,a)
                        self.__imgList.Add(bitmap)
                        self.__layerColor2Image[(i,j)]=c
                        c+=1
            self.SetImageList(self.__imgList)
            self.RefreshItems()
        if tag=='selected_layer' or tag=='layers':
            if not mdl.selected_layer:
                self.Unselect()
            else:
                try:
                    new_idx = mdl.layers.index(mdl.selected_layer)
                    idx = self.GetIndexOfItem(self.GetSelection())[0]
                    if new_idx != idx:
                        itm = self.GetItemByIndex((new_idx,))
                        self.SelectItem(itm)
                except:
                    pass #probably no items in the Tree yet.
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
            layer = self.mapModel.layers[index[0]]
            if not layer.classification:
                return "Class %d"%index[1]
            else:
                k = index[1]
                if k == 0:
                    return "x[i] <= %.3f"%layer.classification.bins[k]
                else:
                    return "%.3f < x[i] <= %.3f"%(layer.classification.bins[k-1],layer.classification.bins[k])
        return ""
    def OnGetItemImage(self,index,which=0,column=0):
        if index in self.__layerColor2Image:
            return self.__layerColor2Image[index]
        return -1
    def OnDrop(self,dropItem,dragItem):
        #print "OnDrop(%r,%r)"%(dropItem,dragItem)
        self.dragging = False
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
    def onMenu(self,evt):
        self.PopupMenu(self.mapCanvas.layerMenu,evt.GetPoint())
    def onSelecting(self,evt):
        if self.dragging:
            evt.Veto()
        evt.Skip()
    def onSelect(self,evt):
        idx = self.GetIndexOfItem(self.GetSelection())
        if idx: #has no index if the item is being moved.
            self.mapModel.selected_layer = self.mapModel.layers[idx[0]]
    def OnDragging(self,evt):
        self.dragging = True
        evt.Skip()
        
