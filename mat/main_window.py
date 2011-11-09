'''
Created on Mar 6, 2011

@author: dhyou
'''

from Tkinter import *
import tkFileDialog


class Project_GPH(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("PySal Plots")
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open GAL", command=self.openGAL)
        fileMenu.add_command(label="Open TXT", command=self.openTXT)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)


        plotMenu = Menu(menubar)
        plotMenu.add_command(label="Moran's I Scatter", command=self.openGAL)
        plotMenu.add_command(label="P-values", command=self.openTXT)
        plotMenu.add_command(label="Box-Plot", command=self.onExit)
        menubar.add_cascade(label="Plot", menu=plotMenu)

        

    def openGAL(self):
        self.fileGAL = tkFileDialog.askopenfilename(filetypes = [('.gal files','.gal')], title = 'Open GAL',initialdir='./' )

    def openTXT(self):
        self.fileTXT = tkFileDialog.askopenfilename(filetypes = [('.csv files','.txt'),('.csv files','.csv')], title = 'Open Comma Delimited',initialdir='./' )

    def onExit(self):
        self.quit()


def main():
  
    root = Tk()
    root.geometry("600x400+200+200")
    app = Project_GPH(root)
    root.mainloop()  


if __name__ == '__main__':
    main()
    
    

