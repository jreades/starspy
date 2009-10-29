from Tkinter import *

# set up the window itself
top = Tk()
top.title("Frame holding a label and 2 buttons")

f=Frame(top)
Button(f, text="Rank-Size").pack(side=TOP)
Button(f,text="Rank-Clock",command=canvas.pack()).pack(side=TOP)
Button(f, text="Quit", command=f.quit).pack(side=TOP)

#set up the canvas
canvas = Canvas(f, width=500, height=500, bg="white")
canvas.create_oval(50,50,450,450,fill="black")

f.pack()
top.mainloop()
