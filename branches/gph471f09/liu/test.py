from Tkinter import *
from math import *

# set up the window itself
top = Tk()
top.title("Frame holding a label and 2 buttons")

f=Frame(top)
Button(f, text="Rank-Size").pack(side=LEFT)
Button(f,text="Rank-Clock").pack(side=LEFT)
Button(f, text="Quit", command=f.quit).pack(side=LEFT)

#set up the canvas
canvas = Canvas(f, width=800, height=800, bg="white")
canvas.create_oval(50,50,750,750,fill="black")

def drawlines(n):
	ang = 2*pi/n
	for num in range(n):
		canvas.create_line(400,400,400+350*cos(ang*num-pi/2),400+350*sin(ang*num-pi/2),fill='white')
drawlines(10)

canvas.pack()
f.pack()
top.mainloop()
