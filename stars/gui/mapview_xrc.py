# This file was automatically generated by pywxrc.
# -*- coding: UTF-8 -*-

import wx
import wx.xrc as xrc

__res = None

def get_resources():
    """ This function provides access to the XML resources in this module."""
    global __res
    if __res == None:
        __init_resources()
    return __res




class xrcMapFrame(wx.Frame):
#!XRCED:begin-block:xrcMapFrame.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcMapFrame.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PreFrame()
        self.PreCreate(pre)
        get_resources().LoadOnFrame(pre, parent, "MapFrame")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers
        self.mapToolBar = xrc.XRCCTRL(self, "mapToolBar")
        self.openTool = self.GetToolBar().FindById(xrc.XRCID("openTool"))
        self.panTool = self.GetToolBar().FindById(xrc.XRCID("panTool"))
        self.zoomTool = self.GetToolBar().FindById(xrc.XRCID("zoomTool"))
        self.extentTool = self.GetToolBar().FindById(xrc.XRCID("extentTool"))
        self.mapPanelHolder = xrc.XRCCTRL(self, "mapPanelHolder")
        self.FileOpen = self.GetMenuBar().FindItemById(xrc.XRCID("FileOpen"))
        self.MenuToolPan = self.GetMenuBar().FindItemById(xrc.XRCID("MenuToolPan"))
        self.MenuToolZoom = self.GetMenuBar().FindItemById(xrc.XRCID("MenuToolZoom"))
        self.MenuToolExtent = self.GetMenuBar().FindItemById(xrc.XRCID("MenuToolExtent"))

        self.Bind(wx.EVT_TOOL, self.OnTool_openTool, self.openTool)
        self.Bind(wx.EVT_TOOL, self.OnTool_panTool, self.panTool)
        self.Bind(wx.EVT_TOOL, self.OnTool_zoomTool, self.zoomTool)
        self.Bind(wx.EVT_TOOL, self.OnTool_extentTool, self.extentTool)
        self.Bind(wx.EVT_MENU, self.OnMenu_FileOpen, self.FileOpen)
        self.Bind(wx.EVT_MENU, self.OnMenu_MenuToolPan, self.MenuToolPan)
        self.Bind(wx.EVT_MENU, self.OnMenu_MenuToolZoom, self.MenuToolZoom)
        self.Bind(wx.EVT_MENU, self.OnMenu_MenuToolExtent, self.MenuToolExtent)

#!XRCED:begin-block:xrcMapFrame.OnTool_openTool
    def OnTool_openTool(self, evt):
        # Replace with event handler code
        print "OnTool_openTool()"
#!XRCED:end-block:xrcMapFrame.OnTool_openTool        

#!XRCED:begin-block:xrcMapFrame.OnTool_panTool
    def OnTool_panTool(self, evt):
        # Replace with event handler code
        print "OnTool_panTool()"
#!XRCED:end-block:xrcMapFrame.OnTool_panTool        

#!XRCED:begin-block:xrcMapFrame.OnTool_zoomTool
    def OnTool_zoomTool(self, evt):
        # Replace with event handler code
        print "OnTool_zoomTool()"
#!XRCED:end-block:xrcMapFrame.OnTool_zoomTool        

#!XRCED:begin-block:xrcMapFrame.OnTool_extentTool
    def OnTool_extentTool(self, evt):
        # Replace with event handler code
        print "OnTool_extentTool()"
#!XRCED:end-block:xrcMapFrame.OnTool_extentTool        

#!XRCED:begin-block:xrcMapFrame.OnMenu_FileOpen
    def OnMenu_FileOpen(self, evt):
        # Replace with event handler code
        print "OnMenu_FileOpen()"
#!XRCED:end-block:xrcMapFrame.OnMenu_FileOpen        

#!XRCED:begin-block:xrcMapFrame.OnMenu_MenuToolPan
    def OnMenu_MenuToolPan(self, evt):
        # Replace with event handler code
        print "OnMenu_MenuToolPan()"
#!XRCED:end-block:xrcMapFrame.OnMenu_MenuToolPan        

#!XRCED:begin-block:xrcMapFrame.OnMenu_MenuToolZoom
    def OnMenu_MenuToolZoom(self, evt):
        # Replace with event handler code
        print "OnMenu_MenuToolZoom()"
#!XRCED:end-block:xrcMapFrame.OnMenu_MenuToolZoom        

#!XRCED:begin-block:xrcMapFrame.OnMenu_MenuToolExtent
    def OnMenu_MenuToolExtent(self, evt):
        # Replace with event handler code
        print "OnMenu_MenuToolExtent()"
#!XRCED:end-block:xrcMapFrame.OnMenu_MenuToolExtent        




# ------------------------ Resource data ----------------------

def __init_resources():
    global __res
    __res = xrc.EmptyXmlResource()

    wx.FileSystem.AddHandler(wx.MemoryFSHandler())

    mapview_xrc = '''\
<?xml version="1.0" ?><resource>
  <object class="wxFrame" name="MapFrame">
    <object class="wxToolBar" name="mapToolBar">
      <object class="tool" name="openTool">
        <bitmap stock_id="wxART_FILE_OPEN"/>
        <tooltip>Open a Shapefile...</tooltip>
        <XRCED>
          <events>EVT_TOOL</events>
          <assign_var>1</assign_var>
        </XRCED>
      </object>
      <object class="separator"/>
      <object class="tool" name="panTool">
        <bitmap>icons_tbpan_png</bitmap>
        <toggle>1</toggle>
        <tooltip>Pan</tooltip>
        <label>This is a Label</label>
        <XRCED>
          <events>EVT_TOOL</events>
          <assign_var>1</assign_var>
        </XRCED>
      </object>
      <object class="tool" name="zoomTool">
        <bitmap>icons_tbzoomin_png</bitmap>
        <toggle>1</toggle>
        <tooltip>Zoom</tooltip>
        <XRCED>
          <events>EVT_TOOL</events>
          <assign_var>1</assign_var>
        </XRCED>
      </object>
      <object class="tool" name="extentTool">
        <bitmap>icons_tbzoomout_png</bitmap>
        <tooltip>Zoom to Extent</tooltip>
        <XRCED>
          <events>EVT_TOOL</events>
          <assign_var>1</assign_var>
        </XRCED>
      </object>
      <XRCED>
        <assign_var>1</assign_var>
      </XRCED>
    </object>
    <object class="wxBoxSizer">
      <orient>wxVERTICAL</orient>
      <object class="sizeritem">
        <object class="wxPanel" name="mapPanelHolder">
          <size>500,500</size>
          <XRCED>
            <assign_var>1</assign_var>
          </XRCED>
        </object>
        <option>1</option>
        <flag>wxALL|wxEXPAND</flag>
      </object>
    </object>
    <title>STARS -- Map View</title>
    <object class="wxMenuBar" name="mapMenuBar">
      <object class="wxMenu" name="FileMenu">
        <object class="wxMenuItem" name="FileOpen">
          <label>Open...</label>
          <XRCED>
            <events>EVT_MENU</events>
            <assign_var>1</assign_var>
          </XRCED>
        </object>
        <label>File</label>
      </object>
      <object class="wxMenu" name="ToolMenu">
        <label>Tools</label>
        <object class="wxMenuItem" name="MenuToolPan">
          <label>Pan Tool</label>
          <XRCED>
            <events>EVT_MENU</events>
            <assign_var>1</assign_var>
          </XRCED>
        </object>
        <object class="wxMenuItem" name="MenuToolZoom">
          <label>Zoom Tool</label>
          <XRCED>
            <events>EVT_MENU</events>
            <assign_var>1</assign_var>
          </XRCED>
        </object>
        <object class="wxMenuItem" name="MenuToolExtent">
          <label>Zoom to Extent</label>
          <XRCED>
            <events>EVT_MENU</events>
            <assign_var>1</assign_var>
          </XRCED>
        </object>
      </object>
    </object>
  </object>
</resource>'''

    icons_tbpan_png = '''\
\x89PNG\x0d
\x1a
\x00\x00\x00\x0dIHDR\x00\x00\x00\x1a\x00\x00\x00\x1a\x08\x02\x00\x00\x00\
&(\xdb\x99\x00\x00\x00,tEXtCreation Time\x00Tue 27 Jan 2004 14:04:27 -0\
000\xc2\xe8\xde\xe1\x00\x00\x00\x07tIME\x07\xd4\x01\x1b\x0e\x04,\xa3)\x89\
Z\x00\x00\x00\x09pHYs\x00\x00.|\x00\x00.|\x01\xb8^\xc4\xcf\x00\x00\x00\x04\
gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\xa6IDATx\xdac|\xf3\xf2\x06\
\x03\xf5\x00\x13\x15\xcd\x1a8\xe3D\xc45\x80\x88\xa02\x16\x82\xa6@\x18\xff\
\xff\xff\x07\x92\x8c\x8c\x8c\x10.\xae\x10g\xc2o\xd60@\x16\x84\x88\xe0r\
\xe9\xa0\x89
\xac\xa1\xc9B\x96QP_3\xc0B\x13\x1e\x94\x83\xc6\xb3\xf40\x0e%\xec\xe0AK\
vFfA6\x0b\x9e\xc4\xe0\xc9\x95|\xcf\x02]\xc4\x08\x06\x0c\xb0\xb4
\x97\x82\xb31\x19\xf8\xc2\x8e\xf2\xc2
=* n\xc4\xef\x04\x12\x8c\xa3\xb2\xeb\xa8o\x1cr\x9c\x90
\xb0\xe7YH\x9c\x00M\xc4\x13|h\xb9\x95
\x9e\xc5L\x09\x04J\x14R\xbd\xcc8\x92*F\x00\x87\xc0M=mb\x18m\x00\x00\x00\
\x00IEND\xaeB`\x82'''

    icons_tbzoomin_png = '''\
\x89PNG\x0d
\x1a
\x00\x00\x00\x0dIHDR\x00\x00\x00\x1a\x00\x00\x00\x1a\x08\x02\x00\x00\x00\
&(\xdb\x99\x00\x00\x00,tEXtCreation Time\x00Tue 27 Jan 2004 14:02:38 -0\
000\xf5\x14\xde\xd1\x00\x00\x00\x07tIME\x07\xd4\x01\x1b\x0e\x03,\xech\x1f\
\x9d\x00\x00\x00\x09pHYs\x00\x00.|\x00\x00.|\x01\xb8^\xc4\xcf\x00\x00\x00\
\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x01\x11IDATx\xda\xe5\xd5\xc1\
\x0d\x820\x14\x06\xe0\x962\x82\x89#h\xe2\x95\x1d\xbc\x9ax4a8\x12\x8f\x18\
\x8f\x0e\xd1\x01t\x04\x13W\x00,\xb5\x85\xd7\xc7+\xbc&\xdclHS
|\xf9\xfb\xa8"?\xef\xa7X\xafe+Z\xebs9\xf3\xbe\xcdv\x0fOc%Z\xe6\x1c\xd4\
4\xc1\xa4R$\x9a-[\x06\xf2V\x97\xf9\xfb\xed$\x8a\xbc\xc09\xcb\xb7\x9f5\x8a\
\x16Eb\xc2\xab\x90m;\xf4\x01\xca\xe1\xc8h\xd0rb\x18\x90\x95\x0e>oz\x183\
\xa1v\xc5\xf5\x8e\x96\x89\xc44N_NS1\x96\x8b\x95\x0e\x8a\xd0M\xe6\xcc\x16\
\xd5\xe5\x19\x8a\xc8uM)\xb8\x99g\xdf\xac_/\xec\x07\x97\xd6\x8d==\xec\x95\
\xce\x1e\xfdV(\xaa\x9a\xec\xa7\x8f\xe7\x91\\=TT7!j\xad\x946c3\x80I\xcb\xb3\
(\x89\xdf\xacDS~Ov\xd6\x12\x8f\xe3!\x9c\x1f\xd7D\x96(\xe0\xc2\\\xa3\x15\
+\xee\xdc?J\x92\x15k\xa8v\xb2\xaf1#\x17\x1c\xc0\x8ch\xb1;{\xf9\xc5\x09B\
.6H\xc7\x84f\x9a\xfc\xa7\x0f\xe3\x17p;\xd1\x16\xa8\xeb\xfc\xa8\x00\x00\x00\
\x00IEND\xaeB`\x82'''

    icons_tbzoomout_png = '''\
\x89PNG\x0d
\x1a
\x00\x00\x00\x0dIHDR\x00\x00\x00\x1a\x00\x00\x00\x1a\x08\x02\x00\x00\x00\
&(\xdb\x99\x00\x00\x00,tEXtCreation Time\x00Tue 27 Jan 2004 14:03:06 -0\
000\xc4f\xc9Q\x00\x00\x00\x07tIME\x07\xd4\x01\x1b\x0e\x03\x14\xc4j\xa7\x03\
\x00\x00\x00\x09pHYs\x00\x00.|\x00\x00.|\x01\xb8^\xc4\xcf\x00\x00\x00\x04\
gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x01\x0bIDATx\xda\xcd\xd4\xcd\x0d\
\x820\x14\x07\xf0~0\x82\x89#h\xe2\x95\x1d\xbc\x9ax4a8\x12\x8f\x18\x8f\x0e\
\xd1\x01t\x04\x13W\x00,\xb5\x85\xd7\xd7B[\xed\xc1\x17\xd2`\x81_\xfe}\x14\
\xe9\xeby\x27\xf9\x8ae\xb4\xf2sE\xe4}\xab\xf5\x16\xfe\x9ckQ\x98\xd3P\xdb\
Z\x93\x9c{Q\x16\xb6$d\xac\x9e\x99\xfb\xd5$\x8a\x1c\xe0\xb4e\xeacM\xa2B\x91\
\x98\xf0*h\xd7\x8d\xa3\x85\xc6p\xdeh\xd0\xd2\xa2\x1d0*\x1d|^\x8e0fB\xef\
\xca\xf3\x15-\x13\x89i\x9c8\x1d\\q.WT:(B7\x99\x93[TTG("W\x17\xe7p3/\xbe\
Y\xb3^8\x8e\xae_\x97\xb6{\xa8+\xbd:\x86\xadP\xd6\x8dwt\x1f/fr\x0dPY_\x08\
i\x04\xe7B\x9e\xcb\x13\x98\xb4:\x92\xca\xf3\xcdR4e\xf6d\xaf,r\xdb\xef\xec\
\xf9iM\xde\x16Y\x9c\x9dk\xb2\xe2\x8be\xb4\x88\xf3G\x87\x1e\x87\xac\x85\
\x85\xa3\xc5n\xd4\xe5\xc7\x17\xb9<\xe9~\x81p\xef\xb2\xd4so\xdf\x01\xc8\
\x17\x27llx\x00\x00\x00\x00IEND\xaeB`\x82'''

    wx.MemoryFSHandler.AddFile('XRC/mapview/mapview_xrc', mapview_xrc)
    wx.MemoryFSHandler.AddFile('XRC/mapview/icons_tbpan_png', icons_tbpan_png)
    wx.MemoryFSHandler.AddFile('XRC/mapview/icons_tbzoomin_png', icons_tbzoomin_png)
    wx.MemoryFSHandler.AddFile('XRC/mapview/icons_tbzoomout_png', icons_tbzoomout_png)
    __res.Load('memory:XRC/mapview/mapview_xrc')

