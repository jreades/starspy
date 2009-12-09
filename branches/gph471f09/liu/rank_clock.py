from Tkinter import *
import os, random
from dbfpy import dbf
from math import *

os.chdir ('D:/My Dropbox/python/rank-clock')
dbr=dbf.Dbf('USData.dbf')
names = dbr.fieldNames

top = Tk()
top.title("Rank-Clock")

s=Frame(top)
Label(s, text="Number of Ranks:").pack(side=LEFT, padx=5, pady=10)

content = StringVar()
ent = Entry(s,width=8,textvariable=content)
content.set('100')
ent.pack(side = LEFT)

## the matrix is the list of records of the table
matrix = []    
for rec in dbr:
    row = []
    for name in names:
        row.append(rec[name])
    matrix.append(row)

## the item is the list of fields of the table
item = []
for name in names:
    itemi=[]
    for rec in dbr:
        ii = rec[name]
        itemi.append(ii)
    item.append(itemi)

## the rank is the list of sorted fields
rank = []
for r in range(1,len(item)):
    item[r].sort(reverse=True)
    rank.append(item[r])

## the ranksize is the list of the coordinate for drawing the rank-size plot
ranksize=[]
for rs in rank:
    ranksizeye=[]
    for i in range(len(rs)):
        if rs[i] != 0:
            rx = 100+200*log10(i+1)
            ry = 500-60*log10(rs[i])
            ranksizeye.append([rx,ry])
        else:
            break
    ranksize.append(ranksizeye)
    
Num_Ra = int(ent.get()) ##number of ranks in records
Num_Ti = len(rank)  ##number of periods

## line is the records of coordinates of each tranjactory
line = []
for city in matrix:
    line.append([city[0]])

unit_le = 250.000/(Num_Ra-1)
unit_an = 2*pi/(Num_Ti-1)
for ye in range(len(rank)):
    ang = unit_an*ye
    for i in range(Num_Ra):
        if rank[ye][i] != 0:
            for city2 in range(len(matrix)):
                if matrix[city2][ye+1] == rank[ye][i]:
                    x = unit_le*i*sin(ang)
                    y = unit_le*i*cos(ang)
                    line[city2].append([300+x,300-y,ye])

# set up the rank-size window
p = Frame(top)
canvas2 = Canvas(p, width=600, height=600, bg="black")
canvas2.pack(side=RIGHT)

def DrawRST(ranksizelist):
    for rst in ranksizelist:
        r = random.randrange(0,255,1)
        g = random.randrange(0,255,1)
        b = random.randrange(0,255,1)
        color = "#%02x%02x%02x" % (r, g, b)
        for i in range(len(rst)-1):
            canvas2.create_line(rst[i][0],rst[i][1],rst[i+1][0],rst[i+1][1], fill=color,width=1,tags = 'RSLines')

def DrawAxisRS():
    canvas2.create_line(70,500,550,500,fill="white",width=2)
    canvas2.create_line(100,530,100,50,fill="white",width=2)
    for xa in range(0,3,1):
        canvas2.create_line(100+200*xa,500,100+200*xa,530,fill="white",width=2)
        canvas2.create_text(95+200*xa,540,text=str(10**xa),fill="white",font=("14"))
    canvas2.create_text(95+200*xa,570,text="Log Rank",fill="white",font=("14"))
    for ya in range(0,8,1):
        canvas2.create_line(100,500-60*ya,70,500-60*ya,fill="white",width=2)
        canvas2.create_text(65,490-60*ya,text=str(10**ya),fill="white",font=("10"))
    canvas2.create_text(90,40,text="Log Population",fill="white",font=("10"))
def RankSize():
    SetButton2()    
    DrawAxisRS()
    DrawRST(ranksize)
    
# set up the rank-clock window
f=Frame(top)
f2=Frame(f)
f3=Frame(f)
canvas = Canvas(f, width=600, height=600, bg="black")
canvas.pack(side=RIGHT)
def DrawCircles():        
        for i in range(6):
                xmin = 50
                ymin = 50
                xmax = 550
                ymax = 550
                dd = (xmax-xmin)/10
                canvas.create_oval(50+dd*i,50+dd*i,550-dd*i,550-dd*i,outline = "white")
        
def DrawAxis(n):
        ang = 2*pi/(n-1)
        for num in range(n-1):
                canvas.create_line(300,300,300+250*sin(ang*num),300-250*cos(ang*num),fill='white')
                year = str(1790+10*num)
                canvas.create_text(300+260*sin(ang*num),300-260*cos(ang*num), text=year, fill='white')
                
def DrawLines(lines):
    for record in lines:
        r = random.randrange(0,255,1)
        g = random.randrange(0,255,1)
        b = random.randrange(0,255,1)
        color = "#%02x%02x%02x" % (r, g, b)
        for i2 in range(1,len(record)-1):
            canvas.create_line(record[i2][0],record[i2][1],record[i2+1][0],record[i2+1][1], fill=color,width=1,tags = 'Lines')

def DrawTra(List):  ##the tranjectory of indivadual record
        for record in List:
            r = random.randrange(0,255,1)
            g = random.randrange(0,255,1)
            b = random.randrange(0,255,1)
            color = "#%02x%02x%02x" % (r, g, b)
            if len(line[record]) >= 3:
                for i3 in range(1,len(line[record])-1):
                    canvas.create_line(line[record][i3][0],line[record][i3][1],line[record][i3+1][0],line[record][i3+1][1], fill=color,width=2,tags = 'Lines')
                canvas.create_text(line[record][i3+1][0],line[record][i3+1][1], text=line[record][0], fill=color,tags='Lines')
            else:
                canvas.create_oval(line[record][1][0],line[record][1][1],line[record][1][0]+1,line[record][1][1]+1, fill=color,width=2,tags = 'Lines')
                canvas.create_text(line[record][1][0]+10,line[record][1][1]+10, text=line[record][0], fill=color, tags = 'Lines')

def DrawYeTra(List):  ##the trajactory based on year
    yearlines = []
    for year in List:
        for YeTra in line:
            for b in range(1,len(YeTra)):
                if YeTra[b][2]==year:
                    yearlines.append(YeTra)
    
    for record in yearlines:
        r = random.randrange(0,255,1)
        g = random.randrange(0,255,1)
        b = random.randrange(0,255,1)
        color = "#%02x%02x%02x" % (r, g, b)
        for i4 in range(1,len(record)-1):
            canvas.create_line(record[i4][0],record[i4][1],record[i4+1][0],record[i4+1][1], fill=color,width=2,tags = 'Lines')

def SetListBox(): ##Listbox of individual rank
    Label(f2, text='Load Indivadual',width=15,font=14,highlightcolor="black", highlightthickness=2).pack(side=TOP)
    sl = Scrollbar(f2)
    lb = Listbox(f2,height = 5)
    lb['yscrollcommand'] = sl.set
    for lbi in item[0]:
        lb.insert(END,lbi)
    lb.pack(side=LEFT)
    sl.pack(side = LEFT,fill = Y)
    sl['command'] = lb.yview
    
    def Load():
            List = lb.curselection()
            try:
                List = map(int, List)
            except ValueError: pass

            DrawTra(List)
            
    load = Button(f2,text="Load",command=Load,width=10, height = 2).pack(side=RIGHT)

def SetListBox2():  ##ListBox of years
    Label(f3, text='Load Year',width=15,font=14,highlightcolor="black", highlightthickness=2).pack(side=TOP)
    sl = Scrollbar(f3)
    lb = Listbox(f3,height = 5)
    lb['yscrollcommand'] = sl.set
    for year in range(1790,2010,10):
        lb.insert(END,year)
    lb.pack(side=LEFT)
    sl.pack(side = LEFT,fill = Y)
    sl['command'] = lb.yview
    
    def Load2():
            List = lb.curselection()
            try:
                List = map(int, List)
            except ValueError: pass
            DrawYeTra(List)
    load = Button(f3,text="Load",command=Load2,width=10, height = 2).pack(side=RIGHT)
def RankClock():
        DrawCircles()
        DrawAxis(Num_Ti)
        DrawLines(line)
        SetListBox()
        SetListBox2()
        f2.pack(side=TOP)
        f3.pack(side=TOP)
def DeletTag():
        canvas.delete('Lines')       

def Back():
    f.pack_forget()
    s.pack()

def SetButton():
        buSize = Button(f, text="Rank-Size",width=10, height = 2).pack(side=TOP)
        buClock = Button(f,text="Rank-Clock",command=RankClock,width=10, height = 2).pack(side=TOP)
        buClear = Button(f,text="Clear",command=DeletTag,width=10, height = 2).pack(side=TOP)
        buBack = Button(f, text="Back", command=Back,width=10, height = 2).pack(side=TOP)

def LoadData():
    s.pack_forget()
    SetButton()
    f.pack()

def Back2():
    p.pack_forget()
    s.pack()
    
def SetButton2():
    buBack = Button(p, text="Back", command=Back2,width=10, height = 2).pack(side=LEFT)
    
def LoadData2():
    s.pack_forget()
    RankSize()
    p.pack()   
    
buRC = Button(s,text="Rank Clock",command=LoadData,width=12, height = 2).pack(side=LEFT)
buRS = Button(s,text="Rank Size",command=LoadData2,width=12, height = 2).pack(side=LEFT)
buQuit = Button(s, text="Quit", command=s.quit,width=12, height = 2).pack(side=LEFT)
s.pack()   
top.mainloop()