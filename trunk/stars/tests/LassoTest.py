'''
Created on Feb 3, 2011

@author: Xing Kang
'''

BG='Light Gray'
LEGEND_WIDTH=50
BUFFER=0.05
LINE_COLORS='blue','green','red','yellow','cyan','magenta','purple'

import wx
from wx.lib.floatcanvas import FloatCanvas

class FloatView(wx.Frame):
    
    def __init__(self, parent, id, title, position, size):
        wx.Frame.__init__(self, parent, id, title, position, size)
        
        self.master = parent
        self.width = size[0]
        self.height = size[1]
        
        self.canvas = FloatCanvas.FloatCanvas(self, size=self.GetClientSize(), BackgroundColor=BG, Debug=0)
        self.title = title
        self.canvas.SetDoubleBuffered(True)
        self.width, self.height = self.canvas.GetClientSizeTuple()
        print self.width, self.height
        
        self.Bind(wx.EVT_SIZING, self.onSizing)
        self.canvas.Bind(wx.EVT_LEFT_DOWN, self.mouseDown)
        self.canvas.Bind(wx.EVT_MOTION, self.mouseMove)
        self.canvas.Bind(wx.EVT_LEFT_UP, self.mouseUp)
        self.canvas.Bind(wx.EVT_LEFT_DCLICK, self.mouseDClick)
        
        if self.master:
            self.master.SetTitle(title)
        
        self.isInput = False
        self.isLasso = False
        self.polygons = []
        self.polyBoxes = []
        self.polyPts = []
        self.currentPt = (0, 0)
        self.lasso = None
        self.BBox = wx.lib.floatcanvas.FloatCanvas.BBox.BBox([[0, self.height], [0, self.width]])
        
        self.makeMenu()
        
    def onSizing(self, event):
        print 'Sizing'
    
    def makeMenu(self):
        menuBar = wx.MenuBar()
        self.menuBar = menuBar
        
        self.fileMenu()
        self.legendMenu()
        self.inputMenu()
        
        self.SetMenuBar(menuBar)
    
    def inputMenu(self):
        menu2 = wx.Menu()
        iItem = wx.MenuItem(menu2, -1, '&Input Polygon', 'Click to start inputing polygon data')
        self.Bind(wx.EVT_MENU, self.onInputPoly, iItem)
        menu2.AppendItem(iItem)
        
        iItem1 = wx.MenuItem(menu2, -1, '&Lasso Test', 'Click to start drawing a lasso to do hit test')
        self.Bind(wx.EVT_MENU, self.onLasso, iItem1)
        menu2.AppendItem(iItem1)
        
        self.menuBar.Append(menu2, "Functionality")
        
    def fileMenu(self):
        menu = wx.Menu()
        fItem = wx.MenuItem(menu, -1, '&Save', 'Click to save file')
        menu.AppendItem(fItem)
        
        menu.AppendSeparator()
        
        fItem1 = wx.MenuItem(menu, -1, '&Quit', 'Quit the program')
        self.Bind(wx.EVT_MENU, self.quit, fItem1)
        menu.AppendItem(fItem1)
        
        self.menuBar.Append(menu, "&File")

    def legendMenu(self):
        menu1 = wx.Menu()
        lItem = wx.MenuItem(menu1, -1, 'Show Legend', 'Click to see legend')
        menu1.AppendItem(lItem)
        
        lItem1 = wx.MenuItem(menu1, -1, 'Hide Legend', 'Click to invisible legend')
        menu1.AppendItem(lItem1)
        
        self.menuBar.Append(menu1, "&Legend")
    
    def onInputPoly(self, event):
        self.isInput = True
        self.isLasso = False
        self.polygons.append([])
        self.polyBoxes.append([100000, 100000, -100000, -100000])
        self.polyPts.append([(0, 0), (0, 0), (0, 0), (0, 0)])
        
    def onLasso(self, event):
        self.isInput = False
        self.isLasso = True
        
    def mouseDown(self, event):
        print self.isLasso
        if self.isInput and len(self.polygons) > 0:
            num = len(self.polygons) - 1
            pos = event.GetPositionTuple()
            pos = pos[0], self.height - pos[1] - 12
            print pos
            self.polygons[num].append(pos)
            self.currentPt = pos
            
            if pos[0] < self.polyBoxes[num][0]:
                self.polyBoxes[num][0] = pos[0]
                self.polyPts[num][0] = pos
            if pos[1] < self.polyBoxes[num][1]:
                self.polyBoxes[num][1] = pos[1]
                self.polyPts[num][1] = pos
            if pos[0] > self.polyBoxes[num][2]:
                self.polyBoxes[num][2] = pos[0]
                self.polyPts[num][2] = pos
            if pos[1] > self.polyBoxes[num][3]:
                self.polyBoxes[num][3] = pos[1]
                self.polyPts[num][3] = pos

            self.draw()
        if self.isLasso:
            if self.lasso == None:
                self.lasso = [0, 0, 0, 0]
            pos = event.GetPositionTuple()
            pos = pos[0], self.height - pos[1] - 12
            self.lasso[0] = pos[0]
            self.lasso[1] = pos[1]
            self.draw()
    
    def mouseMove(self, event):
        if self.isInput and len(self.polygons) > 0:
            num = len(self.polygons) - 1
            if len(self.polygons[num]) > 0:
                pos = event.GetPositionTuple()
                pos = pos[0], self.height - pos[1] - 12
                self.currentPt = pos
                self.draw()
        if self.isLasso and self.lasso != None:
            pos = event.GetPositionTuple()
            pos = pos[0], self.height - pos[1] - 12
            self.lasso[2] = pos[0] - self.lasso[0]
            self.lasso[3] = pos[1] - self.lasso[1]
            self.draw()
    
    def mouseDClick(self, event):
        self.isInput = False
        self.isLasso = False
        
    def mouseUp(self, event):
        if self.isLasso:
            self.isLasso = False
            self.lasso = None
            self.draw()
    
    def hitTest(self, idx, polygon):
        if self.lasso != None:
            polyBox = self.polyBoxes[idx]
            polyPts = self.polyPts[idx]
            left = min(self.lasso[0], self.lasso[0] + self.lasso[2])
            bottom = min(self.lasso[1], self.lasso[1] + self.lasso[3])
            right = max(self.lasso[0], self.lasso[0] + self.lasso[2])
            up = max(self.lasso[1], self.lasso[1] + self.lasso[3])
            
            if polyBox[0] > right or polyBox[1] > up or polyBox[2] < left or polyBox[3] < bottom:
                return False
            else:
                intersect = [0, 0, 0, 0]
                if left >= polyBox[0] and left <= polyBox[2]:
                    intersect[0] = left
                    intersect[2] = min(right, polyBox[2])
                if right >= polyBox[0] and right <= polyBox[2]:
                    intersect[0] = max(left, polyBox[0])
                    intersect[2] = right
                if bottom >= polyBox[1] and bottom <= polyBox[3]:
                    intersect[1] = bottom
                    intersect[3] = min(up, polyBox[3])
                if up >= polyBox[1] and up <= polyBox[3]:
                    intersect[1] = max(bottom, polyBox[1])
                    intersect[3] = up
                
                for pt in polyPts:
                    if pt[0] >= left and pt[1] >= bottom and pt[0] <= right and pt[1] <= up:
                        return True
                for pt in polygon:
                    if pt[0] >= left and pt[1] >= bottom and pt[0] <= right and pt[1] <= up:
                        return True
                return False
        else:
            return False
        
    def draw(self):
        self.canvas.ClearAll()
        self.canvas.AddRectangle((0,0), (self.width, self.height), LineWidth=1.0, LineColor=BG)
        for idx, polygon in enumerate(self.polygons):
            if len(polygon) >= 3:
                color = 'black'
                if self.hitTest(idx, polygon):
                    color = 'green'
                self.canvas.AddLine(polygon, LineWidth=1.0, LineColor=color)
                finalLine = []
                num = len(polygon) - 1
                if idx != len(self.polygons) - 1:
                    finalLine = [polygon[num], polygon[0]]
                else:
                    if self.isInput:
                        finalLine = [polygon[num], self.currentPt, polygon[0]]
                    else:
                        finalLine = [polygon[num], polygon[0]]
                self.canvas.AddLine(finalLine, LineWidth=1.0, LineColor=color)
            elif len(polygon) == 1:
                polygon.append(self.currentPt)
                self.canvas.AddLine(polygon, LineWidth=1.0, LineColor='black')
                polygon.pop()
            elif len(polygon) == 2:
                polygon.append(self.currentPt)
                self.canvas.AddLine(polygon, LineWidth=1.0, LineColor='black')
                finalLine = [polygon[2], polygon[0]]
                self.canvas.AddLine(finalLine, LineWidth=1.0, LineColor='black')
                polygon.pop()
        
        if self.isLasso and self.lasso:
            left = min(self.lasso[0], self.lasso[0] + self.lasso[2])
            bottom = min(self.lasso[1], self.lasso[1] + self.lasso[3])
            self.canvas.AddRectangle((left, bottom), (abs(self.lasso[2]), abs(self.lasso[3])), LineWidth=1.0, LineColor='red')
        self.canvas.Zoom(1.0, (self.width/2., self.height/2.))
                
        
    def quit(self, event):
        return self.Destroy()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    view = FloatView(None, -1, 'New Frame', wx.DefaultPosition, (1024, 768))
    app.SetTopWindow(view)
    view.Show()
    app.MainLoop()