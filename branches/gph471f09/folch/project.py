import numpy as N
import matplotlib
matplotlib.use('TkAgg')
import pylab as PL
from matplotlib import collections as C
from matplotlib import colors as INK
from matplotlib import widgets as W
from matplotlib import nxutils as NX
from matplotlib import patches as P


class ScreenObject:
    '''
    Super class for display objects to go on the screen.

    Input
    id (string): ID for each point
    '''
    colorIn = INK.colorConverter.to_rgba('red')
    colorOut = INK.colorConverter.to_rgba('green')
    def __init__(self, id):
        self.id = id
        self.color = self.colorOut


class Point(ScreenObject):
    '''
    Class to create point objects to be displayed on the screen.

    Inputs
    id (string): ID for each point
    x (float, int): Location on the x-axis
    y (float, int): Location on the y-axis
    '''

    def __init__(self, id, x, y):
        self.xys = [(x,y)]
        ScreenObject.__init__(self, id)


class PointPair(ScreenObject):
    '''
    Class to create point pair objects to be displayed on the screen. Each
    display object is a base point and second point offset above and to the
    right.
    
    Inputs
    id (string): ID for each point pair
    x (float, int): Location on the x-axis for base point
    y (float, int): Location on the y-axis for base point
    '''
    
    def __init__(self, id, x, y):
        self.xys = [(x,y)]
        self.xys.append((x+0.05, y+0.05))
        ScreenObject.__init__(self, id)


class Rectangle(ScreenObject):
    '''
    Class to create rectangle objects to be displayed on the screen.

    Inputs
    id (string): ID for each rectangle
    x (float, int): Location on the x-axis for the origin of the rectangle
    y (float, int): Location on the y-axis for the origin of the rectangle
    width (float, int): Width of the rectangle
    height (float, int): Height of the rectangle
    '''
    
    def __init__(self, id, x, y, width, height):
        self.rectangle = P.Rectangle((x, y), width, height, facecolor=self.colorOut)
        # reference points for selection (corners and center)
        self.xys = [(x,y), (x+width,y), (x+width,y+height), (x,y+height),
                        (x+(width/2.),y+(height/2.))]
        ScreenObject.__init__(self, id)


class View:
    '''
    Super class for on-screen views.  Handles most of the graphics rendering
    and interaction.  It is called by the specific view types.

    Inputs
    id (string): ID for the view
    data (list): List of objects to be plotted.  Expected to come from Point, 
                 PointPair or Rectangle class within this module.
    geometry (string): In the form "ixj+m+n".  Where i is the width of the view 
                       window, j is the height, m is the x-location on the screen, 
                       n is the y-location on the screen.
    '''
    def __init__(self, id, data, geometry):
        self.id = id
        self.data = data
        self.geometry = geometry
        # build up the data structure
        self.point2id = {}
        self.id2ind = {}
        self.id2order = {}
        self.xys = []
        self.facecolors = []
        count = 0
        for enum, i in enumerate(data):
            self.id2ind[i.id] = []
            self.id2order[i.id] = enum
            for j in i.xys:
                self.xys.append(j)
                self.point2id[count] = i.id
                self.id2ind[i.id].append(count)
                self.facecolors.append(i.color)
                count += 1
        # plot the view
        self.figure = PL.figure()
        PL.get_current_fig_manager().window.wm_geometry(geometry)
        self.ax = self.figure.add_subplot(111, xlim=(0,1), ylim=(0,1), autoscale_on=False)
        self.canvas = self.ax.figure.canvas
        # setup the mouse press functionality
        self.cid = self.canvas.mpl_connect('button_press_event', self.onpress)
        self.lasso = W.RectangleSelector(self.ax, self.lineSelectCallback,
                       drawtype='box',useblit=False,
                       minspanx=5,minspany=5,spancoords='pixels')

    def lineSelectCallback(self, event1, event2):
        '''
        Actions to be performed when the lasso is used.

        Inputs
        event1: Press event from the lasso
        event2: Release event from the lasso
        '''
        x1, y1 = event1.xdata, event1.ydata
        x2, y2 = event2.xdata, event2.ydata
        verts = ((x1,y1), (x2,y1), (x2,y2), (x1,y2), (x1,y1))
        ind = N.nonzero(NX.points_inside_poly(self.xys, verts))[0]
        # format data for command line info
        indSet = set([])
        for i in ind:
            indSet.add(self.point2id[int(i)])
        indPrint = ''
        for i in indSet:
            indPrint += i
            indPrint += ', ' 
        print 'View %s; Observation(s) %s'%(self.id, indPrint[:-2])
        # color objects in all active views
        self.interaction(indSet)
        # clean up
        ind = None
        indSet = None
        indPrint = None
        
    def interaction(self, objectIDs):
        '''
        Simple interaction method to highlight selected objects in all views.
        It essentially calls each view's changeColor method.

        Input
        objectIDs (list or set): IDs of the objects selected in the origin view.
        '''
        for i in views:
            ind = []
            for j in objectIDs:
                ind.extend(i.id2ind[j])
            i.changeColors(ind)

    def onpress(self, event):
        '''
        Housekeeping method to keep track of what to do when a mouse click 
        event happens.

        Input
        event: Mouse click event.        
        '''
        if self.canvas.widgetlock.locked(): return
        if event.inaxes is None: return
        # acquire a lock on the widget drawing
        self.canvas.widgetlock(self.lasso)

class Points(View):
    '''
    Generates a view containing points.

    Inputs
    id (string): ID for the view
    data (list): List of objects to be plotted.  Expected to come from Point or 
                 PointPair class within this module.
    geometry (string): In the form "ixj+m+n".  Where i is the width of the view 
                       window, j is the height, m is the x-location on the screen, 
                       n is the y-location on the screen.
    '''
    def __init__(self, id, data, geometry):
        View.__init__(self, id, data, geometry)
        self.collection = C.RegularPolyCollection(self.figure.dpi, sizes=(100,),
            facecolors=self.facecolors, offsets=self.xys, transOffset = self.ax.transData)
        self.ax.add_collection(self.collection)
        
    def changeColors(self, ind):
        '''
        Changes the color of selected objects.

        Input
        ind (list): Indexes identifying which points need to change color.
        '''
        facecolors = self.collection.get_facecolors()
        for i in range(len(facecolors)):
            if i in ind:
                facecolors[i] = Point.colorIn
            else:
                facecolors[i] = Point.colorOut
        self.canvas.draw_idle()
        self.canvas.widgetlock.release(self.lasso)

class Rectangles(View):
    '''
    Generates a view containing rectangles.

    Inputs
    id (string): ID for the view
    data (list): List of objects to be plotted.  Expected to come from Rectangle 
                 class within this module.
    geometry (string): In the form "ixj+m+n".  Where i is the width of the view 
                       window, j is the height, m is the x-location on the screen, 
                       n is the y-location on the screen.
    '''
    def __init__(self, id, data, geometry):
        View.__init__(self, id, data, geometry)
        self.collection = []
        for i in data:
            self.collection.append(i.rectangle)
        self.collection = C.PatchCollection(self.collection,
                facecolors=self.facecolors)
        self.ax.add_collection(self.collection)

    def changeColors(self, ind):
        '''
        Changes the color of selected objects.

        Input
        ind (list): Indexes identifying which points need to change color.
                    Note that since the viewable objects are rectangles these
                    "points" need to be tied to their associated rectangle
                    inside this function.
        '''
        selectedPolygons = self.polyINpoly(ind)
        facecolors = self.collection.get_facecolors()
        for i in range(len(facecolors)):
            if i in selectedPolygons:
                facecolors[i] = Rectangle.colorIn
            else:
                facecolors[i] = Rectangle.colorOut
        self.canvas.draw_idle()
        self.canvas.widgetlock.release(self.lasso)

    def polyINpoly(self, ind):
        '''
        Rudimentary polygon in polygon function. The data structure ties
        hidden points on the screen to viewable polygons on the screen.  This
        method translates the points selected by the lasso into the rectangle
        objects needing to be colored.

        Input
        ind (list): Indexes identifying which points need to change color.

        Returns (list)
        List of indexes identifying which rectangles need to change color.
        '''
        selectedPolygons = set([])
        for i in ind:
            selectedPolygons.add(self.id2order[self.point2id[i]])
        return selectedPolygons
        
views = []

if __name__ == '__main__':

    letters = [chr(i) for i in range(97, 123)]  
    # setup View A
    data = [Point(letters[count], *xy) for count, xy in enumerate(N.random.rand(25, 2))]
    geometry = "400x400+50+50"
    views.append(Points('A', data, geometry))
    # setup View B
    data = [PointPair(letters[count], *xy) for count, xy in enumerate(N.random.uniform(0,0.95, (25, 2)))]
    geometry = "400x400+500+50"
    views.append(Points('B', data, geometry))
    # setup View C
    xRec,yRec = 0.0, 0.0
    width, height = 0.2, 0.2
    data = []
    count = 0
    for i in range(5):
        for j in range(5):
            rec = Rectangle(letters[count], xRec, yRec, width, height)
            data.append(rec)
            yRec += 0.2
            count += 1
        xRec += 0.2
        yRec = 0
    geometry = "400x400+500+500"
    views.append(Rectangles('C', data, geometry))

    PL.show()


