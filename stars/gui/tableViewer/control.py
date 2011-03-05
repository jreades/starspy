import wx
import stars
import random

def spec2str(spec):
    """
    util function to help wx calculcate column widths.
    Returns a string based on the DBF spec.
    """
    typ,s,p = spec
    typ = typ.lower()
    value = 0
    if typ == "n": value = str(value).rjust(s, 'x')
    elif typ == 'd': value = 'X'*len('YYYY/MM/DD')
    elif typ == 'l': value = str(value)[0].upper()
    else: value = str(value)[:s].ljust(s, 'x')
    return value
class DbfTableList(wx.ListCtrl):
    def __init__(self,parent,layer):
        wx.ListCtrl.__init__(self,parent,style=wx.LC_REPORT|wx.LC_VIRTUAL)

        #bindings
        self.Bind(wx.EVT_IDLE,self.onIdle)
        self.Bind(wx.EVT_CHAR,self.onKey)

        self.layer = layer
        self.db = layer.data_table
        #Background Styles
        self.grey = wx.ListItemAttr(colBack=wx.Colour(237,243,254))
        self.white = wx.ListItemAttr(colBack=wx.Colour(255,255,255))
        # Fill the Header names with the max width for each field based on the spec
        # Use -2 for the width tells wx to adjust the column widths based on the header.
        # We'll capture these width (based on current font) Then we'll clear it all out.
        for field,spec in zip(self.db.header,self.db.field_spec):
            self.InsertColumn(-1,spec2str(spec),width=-2)
        widths = [self.GetColumnWidth(i) for i in range(len(self.db.header))]
        self.ClearAll()
        for field,w in zip(self.db.header,widths):
            self.InsertColumn(-1,field,width=w)
        self.SetItemCount(len(self.db))

        layer.addListener(self.updateLayer)
    def updateLayer(self,mdl,tag):
        if tag == 'selection':
            value = self.layer.selection
            nxt = -1
            # Unselect everything first.
            while 1:
                nxt = self.GetNextSelected(nxt)
                if nxt == -1:
                    break
                else:
                    self.Select(nxt,False)
            # Now select the new rows.
            for x in value:
                self.Select(x)

    def OnGetItemText(self,item,column):
        """
        Table is Virtual, i.e. not in ram.
        As the table is scrolled, wx will call this function to load values from.
        
        This is a little slower, but allows very very large tables to be viewed!
        """
        return str(self.db[item,column][0])
    def OnGetItemAttr(self,item):
        """
        Return the style for each row, alternates background color
        """
        if item%2: #odd
            return self.grey
        else:
            return self.white
    def onIdle(self,evt):
        """
        Because we are using a virtual list, selection events will not work as expected.
        Instead while Idle we'll check to see if the selection changed, if so, update the layer.
        """
        sel = self.layer.selection
        newSel = set()
        nxt = -1
        while 1:
            nxt = self.GetNextSelected(nxt)
            if nxt == -1:
                break
            else:
                newSel.add(nxt)
        if sel != newSel:
            self.layer.selection = newSel
    def onKey(self,evt):
        self.layer.selection = set(random.sample(xrange(len(self.db)),20))
        
    
class TableViewer(wx.Frame):
    def __init__(self,parent,layer):
        wx.Frame.__init__(self,parent)
        self.model = DbfTableList(self,layer)
        self.Bind(wx.EVT_CLOSE,self.toggleShown)
    def toggleShown(self,evt):
        self.Show(self.IsShown()^True)
        
        
        


