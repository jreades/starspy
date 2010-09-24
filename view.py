"""
abstract view class for refactoring of STARS

modification of yin's solution
"""

import Tkinter as Tk

N=Tk.N
S=Tk.S
E=Tk.E
W=Tk.W
BG='gray'

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

    def __draw(self):

        # override this in subclasses
        w=self.width/10.
        for i in range(10):
            x0=i*w
            x1=x0+w
            for j in range(10):
                y0=j*w
                y1=y0+w
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
        x_scale = event.width*1.0/self.width
        y_scale = event.height*1.0/self.height
        self.width = event.width
        self.height = event.height
        self.canvas.scale(Tk.ALL,0,0,x_scale,y_scale)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title=value
        print 'setter'
        self.top.title(value)
    




if __name__ == '__main__':

    v=View()
    v2=View(center=True)
    v3=View(center=True,title='V3')


