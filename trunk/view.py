"""
abstract view class for refactoring of STARS

"""
import Tkinter as Tk

N=Tk.N
S=Tk.S
E=Tk.E
W=Tk.W
BG='gray'
LEGEND_WIDTH=50

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
        self.__draw()
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
            self.zoom_x1 = cx
            self.zoom_y1 = cy
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

    def __draw(self):

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
        self.menu=Tk.Menu(self.master,tearoff=0)
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

if __name__ == '__main__':

    v=View()
    v2=View(center=True)
    v3=View(center=True,title='V3')


