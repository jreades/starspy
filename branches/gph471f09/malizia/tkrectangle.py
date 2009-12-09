# This script was written to time the speed of Tkinter in drawing
# a large number of random rectangles. 
#
# Written by Nicholas Malizia on December 8, 2009.


from Tkinter import *
import random
import time

start = time.clock()

# Creates the top window.
top = Tk()
top.title("Tkinter Canvas")

f=Frame(top)
canvas = Canvas(f, width=400, height=350, bg='white')

# Carries the dimensions of the canvas into the drawing loop. 
width1 = 400
height1 = 350

# A loop used to draw the random rectangles. 
for k in range(300):
    # set random x, y, w, h for rectangle
    w = random.randint(10, width1/2)
    h = random.randint(10, height1/2)
    x = random.randint(0, width1 - w)
    y = random.randint(0, height1 - h)
    canvas.create_rectangle(x, y, w, h, fill='blue')

#This publishes the canvas to the screen and stops the timer. 
canvas.pack()
f.pack()
elapsed = (time.clock() - start)

print elapsed

top.mainloop()



