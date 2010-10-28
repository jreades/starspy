"""
abstract view class for refactoring of STARS

"""
import Tkinter as Tk
import dialogues

N=Tk.N
S=Tk.S
E=Tk.E
W=Tk.W
BG='gray'
LEGEND_WIDTH=50
import projections

class View(object,Tk.Frame):
    """
    Abstract View class for STARS
    
    """
    def __init__(self,master=None,height=900,width=900,dynamic_size=True,
            center=False,title=None):
        top=Tk.Toplevel(master)
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)
        Tk.Frame.__init__(self,top,height=height,width=width)
        self.top=top
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        if dynamic_size:
            w=min(self.top.wm_maxsize())
            w/=2.
            h=w
            height=w
            width=w
        self.canvas=Tk.Canvas(self, bg=BG,width=width,height=height)
        self.width=self.canvas.winfo_reqwidth()
        self.height=self.canvas.winfo_reqheight()
        self.canvas.grid(row=0,column=0,sticky=N+S+E+W)
        self.bind('<Configure>', self.__on_configure)
        self.grid(sticky=N+S+E+W)
        self.draw()
        if center:
            self.__center()
        self._title=title
        self.top.title(title)
        self.make_menu()

        # bindings
        self.canvas.bind("<1>", self.button_1)
        self.canvas.bind("<2>", self.button_2)
        self.canvas.bind("<3>", self.button_3)

        # zooming
        self.canvas.bind("<Control-z>", self.start_zooming_e)
        self.canvas.bind("<Control-u>", self.zoom_reverse_e)
        self.canvas.bind("<Control-p>", self.start_panning_e)
        self.canvas.bind("<Control-m>", self.do_menu_e)
        self.zoom_on=0
        self.zoom_history=[]
        self.canvas.focus_set()

        # panning
        self.panning_on=0

    def start_panning_e(self,event):
        self.toggle_panning()

    def toggle_panning(self):
        if self.panning_on:
            self.panning_on=0
            self.canvas.unbind("<1>")
            self.canvas.unbind("<Button1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.canvas.bind("<1>", self.button_1)
        else:
            self.panning_on=1
            self.canvas.bind("<1>",self.panning_start)
            self.canvas.bind("<Button1-Motion>",self.panning_stretch)
            self.canvas.bind("<ButtonRelease-1>",self.panning_stop)

   
    def panning_start(self,event):
        if self.panning_on:
            self.zoom_on=0
            self.canvas.scan_mark(event.x,event.y)

    def panning_stretch(self,event):
        if self.panning_on:
            self.canvas.scan_dragto(event.x,event.y,gain=1)

    def panning_stop(self,event):
        pass

    def start_zooming_e(self,event):
        print 'start zooming'
        self.toggle_zooming()

    def toggle_zooming(self):
        if self.zoom_on:
            self.zoom_on=0
            self.canvas.unbind("<1>")
            self.canvas.unbind("<Button1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.canvas.bind("<1>", self.button_1)
        else:
            self.zoom_on=1
            self.panning_on=0
            self.canvas.unbind("<1>")
            self.canvas.unbind("<Button1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.canvas.bind("<1>",self.zoom_window_start)
            self.canvas.bind("<Button1-Motion>",self.zoom_window_stretch)
            self.canvas.bind("<ButtonRelease-1>",self.zoom_window_stop)

    def button_1(self,event):
        print 'button 1'
    def button_2(self,event):
        print 'button 2'
    def button_3(self,event):
        print 'button 3'
    
    def zoom_window_start(self, event):
        if self.zoom_on:
            self.zoom_x0 = self.canvas.canvasx(event.x)
            self.zoom_y0 = self.canvas.canvasy(event.y)

    def zoom_window_stop(self, event):
        if self.zoom_on:
            try:
                #handle case where no size change occurs
                x0,y0,x1,y1 = self.canvas.coords("zoom_window")
                self.zoom_window_delete()
                self.zoom_window_on=0
                self.zoom(coords=(x0,y0,x1,y1))
            except:
                pass

    def zoom_window_stretch(self, event):
        if self.zoom_on:
            cx = self.canvas.canvasx(event.x)
            cy = self.canvas.canvasy(event.y)
            self.zoom_window_delete()
            self.zoom_window_create([self.zoom_x0,self.zoom_y0,cx,cy])

    def zoom_window_create(self, coords):
        if self.zoom_on:
            x0,y0,x1,y1=coords
            self.zoom_window = self.canvas.create_rectangle(x0,y0,x1,y1,
                    tag='zoom_window',outline='white')

    def zoom_window_delete(self):
        self.canvas.delete('zoom_window')
    
    def zoom(self, percent=2.0, coords=None):
        Mx=self.width/2.
        My=self.height/2.

        if coords:
            x0,y0,x1,y1=coords
            mx = (x0+x1)/2.
            my = (y0+y1)/2.
        else:
            my=My
            mx=Mx

        dx = Mx-mx
        dy = My-my
        self.zoom_history.append((percent,dx,dy))
        self.percent=percent
        self.canvas.move(Tk.ALL,dx,dy)
        self.canvas.scale(Tk.ALL, Mx, My, percent, percent)
        print 'zoom'

    def zoom_reverse_e(self, event):
        self.zoom_reverse()

    def zoom_reverse(self):
        try:
            percent,dx,dy = self.zoom_history.pop()
            percent = 1./percent
            dx = -1 * dx
            dy = -1 * dy
            My = self.height / 2.
            Mx = self.width / 2.
         
            self.canvas.scale(Tk.ALL,Mx,My,percent,percent)
            self.canvas.move(Tk.ALL,dx,dy)
            self.percent=percent
        except:
            print 'back at original scale'

    def draw(self):

        # override this in subclasses
        w=self.width/10.
        h=self.canvas.winfo_reqheight()/10.
        for i in range(100):
            x0=i*w
            x1=x0+w
            for j in range(10):
                y0=j*h
                y1=y0+h
                coords=(x0,y0,x1,y0,x1,y1,x0,y0)
                self.canvas.create_polygon(coords,fill='green')

    def __center(self):
        self.update_idletasks()
        h=self.top.winfo_height()
        w=self.top.winfo_width()
        ws,hs=self.top.winfo_screenwidth(),self.top.winfo_screenheight()
        self.top.geometry("%dx%d+%d+%d" % (w,h, (ws/2) - (w/2), (hs/2) - (h/2)))

    def __on_configure(self,event):
        """
        Handles window resizing events
        """
        self.canvas.delete('legend')
        x_scale = event.width*1.0/self.width
        y_scale = event.height*1.0/self.height
        self.width = event.width
        self.height = event.height
        self.canvas.scale(Tk.ALL,0,0,x_scale,y_scale)

    def show_legend(self):
        self.do_legend()
    def hide_legend(self):
        self.canvas.delete('legend')
    def do_legend(self):
        self.zoom_on=0
        self.update_idletasks()
        h=self.top.winfo_height()
        w=self.top.winfo_width()
        lheight=100
        lwidth=100
        x0=10
        x1=x0+lwidth
        y0=h-10-lheight
        y1=h-10
        xm=(x1+x0)/2.
        ym=(y1+y0)/2.
        legend=self.canvas.create_rectangle(x0,y0,x1,y1,fill='white',tag='legend')
        ltext=self.canvas.create_text(xm,ym,text='Legend',tag='legend')
        self.canvas.tag_bind('legend','<Button-1>',self.legend_b1)
        self.canvas.tag_bind('legend','<ButtonRelease-1>',
                self.legend_b1_release)
        self.l_x0=x0
        self.l_y0=y0

    def legend_b1(self, event):
        print 'button pressed on legend'
        self.canvas.tag_bind('legend','<Button1-Motion>', self.legend_motion)

    def legend_motion(self, event):
        print 'mouse moving in legend'
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        try:
            dx = cx - self.l_x0
            dy = cy - self.l_y0
        except:
            pass
        self.canvas.move('legend',dx,dy)
        self.l_x0=cx
        self.l_y0=cy

    def legend_b1_release(self, event):
        self.canvas.unbind("<Button1-Motion>")
        print 'mouse release'

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title=value
        print 'setter'
        self.top.title(value)

    def start_zooming_E(self, event):
        self.toggle_zooming()

    def start_zooming(self):
        self.toggle_zooming()


    # menu
    def make_menu(self):
        # override in subclasses
        self.menu=Tk.Menu(self.master,tearoff=0,postcommand=self.menu_update)
        self.file_menu()
        self.menu.add('separator')
        self.legend_menu()

    def do_menu_e(self,event):
        try:
            self.menu.tk_popup(event.x_root,event.y_root,0)
        finally:
            self.menu.grab_release()

    def file_menu(self):
        choices=Tk.Menu()
        choices.add_command(label='Save',underline=0,
                command=self.save)
        choices.add_command(label="Quit",underline=0,
                command=self.quit)
        self.menu.add_cascade(label="File",underline=0,menu=choices)
    def legend_menu(self): 
        choices=Tk.Menu()
        choices.add_command(label='Show Legend',underline=0,
                command=self.show_legend)
        choices.add_command(label="Hide Legend",underline=0,
                command=self.hide_legend)
        self.menu.add_cascade(label="Legend",underline=0,menu=choices)
    def save(self):
        from tkFileDialog import asksaveasfilename
        f = asksaveasfilename(parent=self.top,
                             defaultextension=".ps",title="Save map as..")
        if not f:
            raise Cancel
        try:
            f=f+".ps"
            self.canvas.postscript(file=f)
        except IOError:
            from tkMessageBox import showwarning
            showwarning("Save As", "Cannot save the file.")
            raise Cancel
    def quit(self):
        self.top.destroy()

    def menu_update(self):
        print 'override'


class Choropleth(View):
    """Choropleth Mapping """
    def __init__(self,polygons,bb=None, p2s=None,colors=None):
        self.polygons=polygons
        if bb:
            self.bb=bb
        else:
            self.set_bb()
        self.p2s=p2s
        if p2s:
            s2p={}
            vals=p2s.values()
            for val in vals:
                s2p[val]=[]
            for key in p2s.keys():
                right=p2s[key]
                s2p[right].append(key)
            self.s2p=s2p
        self.colors=colors
        View.__init__(self)

    def set_bb(self):
        print 'not implemented'
    def legend_menu(self): 
        choices=Tk.Menu()
        choices.add_command(label='Show Legend',underline=0,
                command=self.show_legend)
        choices.add_command(label="Hide Legend",underline=0,
                command=self.hide_legend)
        choices.add('separator')
        choices.add_command(label="Quantiles",underline=0,
                command=self.do_quantiles)
        choices.add_command(label="Equal Intervals",underline=0,
                command=self.do_equal_intervals)
        choices.add_command(label="Maximum Breaks",underline=0,
                command=self.do_maximum_breaks)
        self.menu.add_cascade(label="Legend",underline=0,menu=choices)

    def do_quantiles(self):
        print 'quantiles'
        self.classifier='quantiles'
 
        dbf=self.shape_file.split(".")[0]
        dbf=dbf+".dbf"
        f=ps.open(dbf)
        vnames=f.header
        cd=dialogues.Classifier(vnames,attribute_command=self.set_variable,
                k_command=self.set_k,parent=self,title="Quantiles")

    def set_variable(self,id):
        self.classifier='quantiles'
        dbf=self.shape_file.split(".")[0]
        dbf=dbf+".dbf"
        f=ps.open(dbf)
        vnames=f.header
        self.variable_name=vnames[id]
        v=np.array(f.by_col(self.variable_name))
        c=ps.Quantiles(v,self.k)
        self.c=c
        self.y=v
        colors=color.colorSchemes.getScheme('projector','sequential',self.k).colors
        k=self.p2s.keys()
        k.sort()
        colors=[colors[c.yb[self.p2s[i]]] for i in k]
        self.colors=colors
        self.recolor()
        self.c=c


    def set_k(self,k):
        k=int(k)
        self.k=k

    def do_equal_intervals(self):
        self.classifier='equal_intervals'
        print 'ei'

    def do_maximum_breaks(self):
        self.classifer='maximum_breaks'
        print 'mb'

    def world_2_screen(self):
        w=self.width
        h=self.height

        mx=w/2.
        my=h/2.
        self.screen_polygons=self.polygons[:]
        x0,y0,x1,y1=self.bb

        mwx=(x1+x0)/2.
        mwy=(y1+y0)/2.

        # scale
        sx=w/(x1-x0)
        sy=h/(y1-y0)

        sx=min(sx,sy)*0.9
        self.sx=sx

        for i,polygon  in enumerate(self.screen_polygons):
            for j,vert in enumerate(polygon):
                x,y=vert

                xs=(x-mwx)*sx + mx
                ys=(mwy-y)*sx + my
                polygon[j]=(xs,ys)
            self.screen_polygons[i]=polygon

    def draw(self):
        self.world_2_screen()

        marks2p={}
        p2marks={}
        for i,polygon in enumerate(self.screen_polygons):
            color=self.colors[i]
            marks2p[i]=self.canvas.create_polygon(polygon,fill=color,outline='black')
            p2marks[marks2p[i]]=i
        self.marks2p=marks2p
        self.p2marks=p2marks

            #print i
            #t=raw_input('here')
    def recolor(self):
        for i in self.marks2p:
            self.canvas.itemconfigure(self.marks2p[i],fill=self.colors[i])

class PlotShapeFile:
    """exploring shapefiles """
    def __init__(self,shapefile="us48join.shp",variable=None,classifier='quantiles',
            k=5,scheme='sequential', projection='unproj'):

        if projection=='unproj':
            proj=projections.unproj
        elif projection=='mercator':
            proj=projections.mercator

        head,tail=shapefile.split(".")
        f=ps.open(shapefile)
        bb=f.bbox
        polygons=[]
        flag=1
        while flag:
            try:
                shp=f.next()
                polygons.append(shp)
            except:
                flag=0

        # unprojected first
        new_polygons=[]
        p2s={}
        s2p={}
        x0,y0=proj(bb[0],bb[1])
        x1,y1=proj(bb[2],bb[3])
        bb=[x0,y0,x1,y1]
        print bb
        pid=0
        for i,polygon in enumerate(polygons):
            s2p[i]=[]
            for part in polygon.parts:
                verts=[]
                for j,point in enumerate(part):
                    lon,lat=point
                    x,y=proj(lon,lat)
                    verts.append((x,y))
                    x0=min(x,x0)
                    x1=max(x,x1)
                    y0=min(y,y0)
                    y1=max(y,y1)
                new_polygons.append(verts)
                s2p[i].append(pid)
                p2s[pid]=i
                pid+=1
        self.s2p=s2p
        self.p2s=p2s
        f.close()
        if variable:
            d=ps.open(head+".dbf")
            y=np.array(map(int,d.by_col(variable)))
            mc=ps.Quantiles(y)
            cs=color.colorSchemes.getScheme('projector','sequential',5).colors
            k=p2s.keys()
            k.sort()
            colors=[cs[mc.yb[p2s[i]]] for i in k]
        else:
            colors=['white' for i in p2s.keys()]
        cm=Choropleth(new_polygons, bb,self.p2s,colors=colors)
        cm.shape_file=shapefile
        self.cm=cm




if __name__ == '__main__':
    import pysal as ps
    import projections as mercator
    import numpy as np
    import color

    p=PlotShapeFile('us48join.shp')
    """
    vu=PlotShapeFile('data/virginiacounties.shp')
    v=PlotShapeFile('data/virginiacounties.shp',projection='mercator')
    #v=View()
    #v2=View(center=True)
    #v3=View(center=True,title='V3')
    head="us48join"

    f=ps.open(head+".shp")
    bb=f.bbox
    polygons=[]
    flag=1
    while flag:
        try:
            shp=f.next()
            polygons.append(shp)
        except:
            flag=0

    # unprojected first
    new_polygons=[]
    p2s={}
    x0,y0=proj(bb[0],bb[1])
    x1,y1=proj(bb[2],bb[3])
    bb=[x0,y0,x1,y1]
    print bb
    pid=0
    for i,polygon in enumerate(polygons):
        for part in polygon.parts:
            verts=[]
            for j,point in enumerate(part):
                lon,lat=point
                x,y=proj(lon,lat)
                verts.append((x,y))
                x0=min(x,x0)
                x1=max(x,x1)
                y0=min(y,y0)
                y1=max(y,y1)
            new_polygons.append(verts)
            p2s[pid]=i
            pid+=1

    f.close()
    d=ps.open(head+".dbf")
    y=np.array(map(int,d.by_col('N88')))
    mc=ps.Quantiles(y)
    cs=color.colorSchemes.getScheme('projector','sequential',5).colors
    colors=[cs[i] for i in mc.yb]
    cm=Choropleth(new_polygons, bb,p2s,colors=cs)
    """


















