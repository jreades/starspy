import Tkinter as Tk


class Classifier:
    """ """
    def __init__(self,varlist,attribute_command,k_command,k=4,parent=None,
            title=None):
        self.attribute_command=attribute_command
        self.k_command=k_command
        self.variables=varlist
        top=Tk.Toplevel()
        self.top=top
        self.top.title(title)
        fr=Tk.Frame(top)
        vlab=Tk.Label(fr,text="Variable")
        lb=Tk.Listbox(fr)
        for var in varlist:
            lb.insert(Tk.END,var)
        vlab.grid(row=0)
        lb.grid(row=1)
        klab=Tk.Label(fr,text="No. of Classes")
        k_entry=Tk.Entry(fr)
        k_entry.insert(0,'4')
        klab.grid(row=2)
        k_entry.grid(row=3)
        bf=Tk.Frame(fr)
        bcancel=Tk.Button(bf,text="Cancel",command=self.on_cancel)
        bok=Tk.Button(bf,text='Ok',command=self.on_ok)
        bok.grid(row=0,column=0)
        bcancel.grid(row=0,column=1)
        bf.grid(row=4)
        self.lb=lb
        self.entry=k_entry
        fr.grid()

    def on_cancel(self):
        self.top.destroy()

    def on_ok(self):
        i=int(self.lb.curselection()[0])
        k=self.entry.get()
        print i,k
        self.k_command(int(k))
        self.attribute_command(i)
        self.top.destroy()






