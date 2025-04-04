from math import trunc
from tkinter import *
from tkinter.font import Font
import time

from more_itertools.more import difference


def inArea(x, y, xp, yp, mx, my):
    if x <= mx <= xp and y <= my <= yp:
        return True
    else:
        return False






#window class
class Window():
    def __init__(self, grid=100, screenX=800, screenY=520, bgc="#ffffff", fullscreen=False, title="Agui"):


        # objects
        self.objects = {} # dict [id : object]
        self.loc = {} # dict [id : n]
        self.propertys = [] # array [type,tag,active,parent,[children],x,y,args*]
        self.actives = []
        self.mouseMoveUpdates = []
        self.clickUpdates1 = []
        self.keyUpdates = []
        self.updated = []
        self.n = 0 # total number of objects


        # window setup
        self.disp = Tk()
        self.disp.configure(bg=bgc)
        self.disp.geometry(str(screenX) + "x" + str(screenY))
        self.disp.title(title)
        self.canvas = Canvas(self.disp, width=self.disp.winfo_width() / 1.25,
                             height=self.disp.winfo_height() / 1.25, bg=bgc)
        self.canvas.pack()
        if fullscreen:
            self.disp.state('zoomed')
        self.canvas.pack()
        self.i = grid
        self.disp.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas.bind("<Button-1>", self.mouse1)
        self.canvas.bind("<Button-3>", self.mouse2)
        self.canvas.bind("<Button-2>", self.mouse3)
        self.canvas.bind("<ButtonRelease-1>", self.mouseup1)
        self.disp.bind_all("<Key>",self.key)
        self.clicktype = None
        self.mousedown = [False,False,False]


        # vars
        self.running = True
        self.winX = screenX
        self.winY = screenY
        self.mX = 0
        self.mY = 0
        self.lastkeypressed = None
        self.laskeysym = None
        self.keypressed = False



        #lookup
        self.lookup = {
            "point":{"tag":1,"active":2,"parent":3,"children":4,'x':5,'y':6,'radius':7,'color':8},
            "line": {"tag":1, 'active':2, 'parent':3, "children":4, 'x':5, 'y':6, 'xp':7, 'yp':8, 'thickness':9, "fill":10},
            "rect": { "tag":1, "active":2, "parent":3, "children":4, 'x':5, 'y':6, 'xp':7, 'yp':8, 'thickness':9, "fill":10, "stroke":11},
            "circle": {"tag": 1, "active": 2, "parent": 3, "children": 4, 'x': 5, 'y': 6, 'xp': 7, 'yp': 8,'thickness': 9, "fill": 10, "stroke": 11},
            "text":{ "tag":1, "active":2, 'parent':3, "children":4, 'x':5, "y":6, 'size':7, 'text':8, 'fill':9, 'font':10, 'angle':11},
            "hitbox":{ 'tag':1, 'active':2, 'parent':3, "children":4, 'x':5, 'y':6, 'xp':7, 'yp':8, 'function':9,"activated":10},
            "button": { 'tag':1, 'active':2, 'parent':3, "children":4, 'x':5, 'y':6, 'xp':7, 'yp':8, 'functionL':9,'functionR':10,'functionM':11},
            "textbox": { 'tag':1, 'active':2, 'parent':3, "children":4, 'x':5, 'y':6,'xp':7,'yp':8,'size':9, 'value':10, 'fill':11, 'font':12, 'angle':13, 'defualtValue':14, 'whitelist':15, 'blacklist':16,"defaultValuePersistence":17,"selected":18,"position":19,"showCursor":20,"cursorTime":21},
            "draggable":{ 'tag':1, 'active':2, 'parent':3, "children":4, 'x':5, 'y':6, 'xp':7, 'yp':8, 'lockX':9, 'lockY':10, 'snapToMouse':11, "Xrel":12, "Yrel":13,"clickType":14}
        }
        self.keyupdateLookup={
            "textbox": self.__keyTextbox__
        }
        self.clickupdateLookup={
            "button": self.__updateButton__,
            "textbox":self.__selectTextbox__,
            "draggable":self.__selectDraggable__
        }
        self.updateLookup={
            "point":self.__updatePoint__,
            "line":self.__updateLine__,
            "rect":self.__updateRect__,
            "circle": self.__updateCircle__,
            "text":self.__updateText__,
            "hitbox":self.__updateHitbox__,
            "button":self.__updateButton__,
            "textbox": self.__updateTextbox__,
            "draggable":self.__updateDraggable__
        }
        self.activeLookup={True:"normal",False:"hidden"}

    def close(self):
        self.running=False
        self.disp.destroy()
    def mouseup1(self,event):
        self.mousedown[0] = False
    def mouse1(self,event):
        self.clicktype = 1
        self.mousedown[0] = True

        for i in self.clickUpdates1:
            self.__select_item__(i)

    def mouse2(self,event):
        self.clicktype = 2

        for i in self.clickUpdates1:
            self.__select_item__(i)

    def mouse3(self,event):
        self.clicktype = 3

        for i in self.clickUpdates1:
            self.__select_item__(i)
    def key(self,tag):
        self.lastkeypressed = tag.char
        self.laskeysym = tag.keysym
        self.keypressed = True
        for i in self.keyUpdates:
            self.__key_item__(i)
        self.keypressed = False




    def update(self):
        self.updated = []
        #print(self.mouseMoveUpdates)
        if(self.winY-self.disp.winfo_height()!=0 or self.winX-self.disp.winfo_width()!=0):
            self.winY = self.disp.winfo_height()
            self.winX = self.disp.winfo_width()
            self.canvas.config(width=self.winX, height=self.winY)
            for i in self.actives:
                self.__update_item__(i)




        for i in self.mouseMoveUpdates:
            self.__update_item__(i)
        self.mX = (self.i / self.winX) * (self.disp.winfo_pointerx() - self.disp.winfo_x() - 8)
        self.mY = (self.i / self.winY) * (self.disp.winfo_pointery() - self.disp.winfo_y() - 30)



        # update backend (Last)

        self.disp.update()
        self.disp.update_idletasks()


    def __update_item__(self,tag):
        self.updateLookup[self.propertys[self.loc[tag]][0]](tag)
    def __select_item__(self,tag):
        self.clickupdateLookup[self.propertys[self.loc[tag]][0]](tag)
    def __key_item__(self,tag):
        self.keyupdateLookup[self.propertys[self.loc[tag]][0]](tag)


    def point(self,tag,x,y,radius=1,color="#000000",active=True,parent=None):
        self.objects[tag] = self.canvas.create_oval(x, y, x, y, fill=color,outline=color)
        self.loc[tag] = self.n
        self.propertys.append(["point",tag,active,parent,[],x,y,radius,color])
        self.n +=1
        if parent != None:
            self.propertys[self.loc[parent]][4].append(tag)
        self.actives.append(tag)
        self.__updatePoint__(tag)
    def __updatePoint__(self,tag):

        if self.propertys[self.loc[tag]][2] or tag in self.actives:
            self.__updateChildren__(tag)
            p = self.__calcloc__(tag)
            x = p[0]
            y = p[1]
            n = self.loc[tag]
            a = self.__calcVis__(tag)
            if not(a):
                self.actives.remove(tag)
                self.canvas.itemconfig(self.objects[tag], state="hidden")
            elif a and not(tag in self.actives):
                self.actives.append(tag)
                self.canvas.itemconfig(self.objects[tag], state="normal")

            self.canvas.coords(self.objects[tag],self.__calcX__(x)+(self.propertys[n][7]/2),self.__calcY__(y)+(self.propertys[n][7]/2),self.__calcX__(x)-(self.propertys[n][7]/2),self.__calcY__(y)-(self.propertys[n][7]/2))

    def line(self, tag, x, y, xp,yp, fill="#000000",thickness=1 ,active=True, parent=None):
        self.objects[tag] = self.canvas.create_line(x, y, xp-x, yp-x, fill=fill,width=thickness)
        self.loc[tag] = self.n
        self.propertys.append(["line", tag, active, parent, [], x, y, xp-x, yp-x,thickness, fill])
        self.n += 1
        if parent != None:
            self.propertys[self.loc[parent]][4].append(tag)
        self.actives.append(tag)
        self.__updateLine__(tag)
    def __updateLine__(self,tag):
        if self.propertys[self.loc[tag]][2] or tag in self.actives:
            self.__updateChildren__(tag)
            p = self.__calcloc__(tag)
            x = p[0]
            y = p[1]
            n = self.loc[tag]
            a = self.__calcVis__(tag)
            if not (a):
                self.actives.remove(tag)
                self.canvas.itemconfig(self.objects[tag], state="hidden")
            elif a and not (tag in self.actives):
                self.actives.append(tag)
                self.canvas.itemconfig(self.objects[tag], state="normal")
            self.canvas.coords(self.objects[tag],self.__calcX__(x),self.__calcY__(y),self.__calcX__(x+float(self.propertys[n][7])),self.__calcY__(y+float(self.propertys[n][8])))

    def rect(self, tag, x, y, xp,yp, fill="#000000",stroke="#000000",thickness=1 ,active=True, parent=None):
        self.objects[tag] = self.canvas.create_rectangle(x, y, xp-x, yp-x, fill=fill,outline=stroke,width=thickness)
        self.loc[tag] = self.n
        self.propertys.append(["rect", tag, active, parent, [], x, y, xp-x, yp-x,thickness, fill,stroke])
        self.n += 1
        if parent != None:
            self.propertys[self.loc[parent]][4].append(tag)
        if active:
            self.actives.append(tag)
        self.__updateRect__(tag)
    def __updateRect__(self,tag):
        if self.propertys[self.loc[tag]][2] or tag in self.actives:

            p = self.__calcloc__(tag)
            x = p[0]
            y = p[1]
            n = self.loc[tag]
            a = self.__calcVis__(tag)
            if not (a):
                self.actives.remove(tag)
                self.canvas.itemconfig(self.objects[tag], state="hidden")
            elif a and not (tag in self.actives):
                self.actives.append(tag)
                self.canvas.itemconfig(self.objects[tag], state="normal")
            self.__updateChildren__(tag)
            self.canvas.coords(self.objects[tag],self.__calcX__(x),self.__calcY__(y),self.__calcX__(x+float(self.propertys[n][7])),self.__calcY__(y+float(self.propertys[n][8])))

    def circle(self, tag, x, y, xp,yp, fill="#000000",stroke="#000000",thickness=1 ,active=True, parent=None):
        self.objects[tag] = self.canvas.create_oval(x, y, xp-x, yp-x, fill=fill,outline=stroke,width=thickness)
        self.loc[tag] = self.n
        self.propertys.append(["circle", tag, active, parent, [], x, y, xp-x, yp-x,thickness, fill,stroke])
        self.n += 1
        if parent != None:
            self.propertys[self.loc[parent]][4].append(tag)
        if active:
            self.actives.append(tag)
        self.__updateRect__(tag)
    def __updateCircle__(self,tag):
        if self.propertys[self.loc[tag]][2] or tag in self.actives:
            self.__updateChildren__(tag)
            p = self.__calcloc__(tag)
            x = p[0]
            y = p[1]
            n = self.loc[tag]
            a = self.__calcVis__(tag)
            if not (a):
                self.actives.remove(tag)
                self.canvas.itemconfig(self.objects[tag], state="hidden")
            elif a and not (tag in self.actives):
                self.actives.append(tag)
                self.canvas.itemconfig(self.objects[tag], state="normal")
            self.canvas.coords(self.objects[tag],self.__calcX__(x),self.__calcY__(y),self.__calcX__(x+float(self.propertys[n][7])),self.__calcY__(y+float(self.propertys[n][8])))

    def text(self,tag,x,y,size,text,fill="#000000",font="Lato",parent=None,active=True,angle=0):
        self.objects[tag] = self.canvas.create_text(x,y,text=str(text),fill=fill,angle=angle,font=font)
        self.loc[tag]=self.n
        self.propertys.append(["text",tag,active,parent,[],x,y,size,text,fill,font,angle])
        self.n+=1
        if parent != None:
            self.propertys[self.loc[parent]][4].append(tag)
        if active:
            self.actives.append(tag)
    def __updateText__(self,tag):
        if self.propertys[self.loc[tag]][2] or tag in self.actives:
            self.__updateChildren__(tag)
            p = self.__calcloc__(tag)
            x = p[0]
            y = p[1]
            n = self.loc[tag]
            a = self.__calcVis__(tag)
            if not (a):
                self.actives.remove(tag)
                self.canvas.itemconfig(self.objects[tag], state="hidden")
            elif a and not (tag in self.actives):
                self.actives.append(tag)
                self.canvas.itemconfig(self.objects[tag], state="normal")
            self.canvas.coords(self.objects[tag], self.__calcX__(x), self.__calcY__(y))
            self.canvas.itemconfig(self.objects[tag],font=(self.propertys[n][10],int(self.propertys[n][7]*(self.winX+self.winY)/600)))

    def hitbox(self,tag,x,y,xp,yp,function=None,parent=None,active=True):
        self.loc[tag] = self.n
        self.propertys.append(["hitbox",tag,active,parent,[],x,y,xp,yp,function,False])
        self.n +=1
        if parent != None:
            self.propertys[self.loc[parent]][4].append(tag)
        if active:
            self.mouseMoveUpdates.append(tag)
    def __updateHitbox__(self,tag):

        p = self.__calcloc__(tag)
        x = p[0]
        y = p[1]
        n = self.loc[tag]
        a = self.__calcVis__(tag)
        if not (a):
            self.mouseMoveUpdates.remove(tag)
        elif a and not (tag in self.mouseMoveUpdates):
            self.mouseMoveUpdates.append(tag)

        if inArea(x,y,x+self.propertys[n][7],y+self.propertys[n][8],self.mX,self.mY):
            if(self.propertys[n][10]==False):
                self.propertys[n][10] = True
                if not (f"{n} {9}" in self.updated):
                    self.propertys[n][9]()
                    self.propertys[n][9]()

        else:
            self.propertys[n][10] = False
        self.__updateChildren__(tag)

    def button(self,tag,x,y,xp,yp,functionL,functionR=None,functionM=None,parent=None,active=True):
        self.loc[tag] = self.n
        self.propertys.append(["button", tag, active, parent, [], x, y, xp, yp, functionL,functionR,functionM])
        self.n += 1
        if parent != None:
            self.propertys[self.loc[parent]][4].append(tag)
        if active:
            self.clickUpdates1.append(tag)
    def __updateButton__(self,tag):

        p = self.__calcloc__(tag)
        x = p[0]
        y = p[1]
        n = self.loc[tag]
        a = self.__calcVis__(tag)
        if not(a):
            self.clickUpdates1.remove(tag)
        elif a and not (tag in self.clickUpdates1):
            self.clickUpdates1.append(tag)
        if inArea(x,y,x+self.propertys[n][7],y+self.propertys[n][8],self.mX,self.mY):
            try:
                if not(f"{n} {8+self.clicktype}" in self.updated):
                    self.updated.append(f"{n} {8 + self.clicktype}")
                    self.propertys[n][8+self.clicktype]()

            except:
                pass
        self.__updateChildren__(tag)

    def textbox(self,tag,x,y,xp,yp,size,defualtValue="text",blacklist=None,whitelist=None,fill="#000000",font="Lato",parent=None,active=True,angle=0,defaultValuePersistence=False,startSelected=False):
        self.objects[tag] = self.canvas.create_text(x, y, text=str(defualtValue), fill=fill, angle=angle, font=font,anchor="w")
        self.loc[tag] = self.n
        self.propertys.append(["textbox", tag, active, parent, [], x, y, xp,yp,size, defualtValue, fill, font, angle,defualtValue,whitelist,blacklist,defaultValuePersistence,startSelected,len(defualtValue),-1,time.time()])
        self.n += 1
        if parent != None:
            self.propertys[self.loc[parent]][4].append(tag)
        if active:
            self.mouseMoveUpdates.append(tag) #just activates every tick lol
            self.clickUpdates1.append(tag)
            self.keyUpdates.append(tag)
        else:
            self.canvas.itemconfig(self.objects[tag], state="hidden")
    def __updateTextbox__(self,tag):
        if self.propertys[self.loc[tag]][2] or tag in self.actives:

            self.__updateChildren__(tag)
            p = self.__calcloc__(tag)
            x = p[0]
            y = p[1]
            n = self.loc[tag]
            a = self.__calcVis__(tag)
            if not (a):
                self.actives.remove(tag)
                self.canvas.itemconfig(self.objects[tag], state="hidden")
            elif a and not (tag in self.actives):
                self.actives.append(tag)
                self.canvas.itemconfig(self.objects[tag], state="normal")
            if self.propertys[n][21] - time.time()<-.5:

                self.propertys[n][20] *= -1
                self.propertys[n][21] = time.time()

            text = self.propertys[n][10]
            if self.propertys[n][18]:
                if self.propertys[n][20] != -1:
                    text = self.propertys[n][10][:self.propertys[n][19]] + "|" + self.propertys[n][10][self.propertys[n][19]:]
                else:
                    text = self.propertys[n][10][:self.propertys[n][19]] + " " + self.propertys[n][10][self.propertys[n][19]:]
            self.canvas.itemconfig(self.objects[tag], text=text)
            medianx = x + ((len(self.propertys[n][10])/2)*self.propertys[n][9])/5
            mediany = (self.propertys[n][8]-y)/2+y
            self.canvas.coords(self.objects[tag], self.__calcX__(x), self.__calcY__(mediany)-int(self.propertys[n][9] * (self.winX + self.winY) / 1200))
            self.canvas.itemconfig(self.objects[tag], font=(
            self.propertys[n][12], int(self.propertys[n][9] * (self.winX + self.winY) / 600)))
    def __selectTextbox__(self,tag):
        p = self.__calcloc__(tag)
        x = p[0]
        y = p[1]
        n = self.loc[tag]
        a = self.__calcVis__(tag)
        if not (a):
            self.clickUpdates1.remove(tag)
        elif a and not (tag in self.clickUpdates1):
            self.clickUpdates1.append(tag)
        if inArea(x, y, x + self.propertys[n][7], y + self.propertys[n][8], self.mX, self.mY):
            if self.propertys[n][21] - time.time()<-.5:

                self.propertys[n][20] *= -1
                self.propertys[n][21] = time.time()

            text = self.propertys[n][10]
            if self.propertys[n][18]:
                if self.propertys[n][20] != -1:
                    text = self.propertys[n][10][:self.propertys[n][19]] + "|" + self.propertys[n][10][self.propertys[n][19]:]
                else:
                    text = self.propertys[n][10][:self.propertys[n][19]] + " " + self.propertys[n][10][self.propertys[n][19]:]
            font = Font(family=self.propertys[n][12], size=int(self.propertys[n][9] * (self.winX + self.winY) / 600))
            length = font.measure(text)
            lengthperletter = self.__calcX__(length) / len(self.propertys[n][10])
            self.propertys[n][19] =  round(((self.mX-self.propertys[n][5]/lengthperletter)-self.propertys[n][5])/2)
            if not (f"{n} {18}" in self.updated):
                self.propertys[n][18]=True
                self.updated.append(f"{n} {18}")
                if not(tag in self.keyUpdates):
                    self.keyUpdates.append(tag)


        else:
            if not (f"{n} {18}" in self.updated):
                self.propertys[n][18] = False
                self.updated.append(f"{n} {18}")
                if tag in self.keyUpdates:
                    self.keyUpdates.remove(tag)
    def __keyTextbox__(self,tag):
        key = self.lastkeypressed
        sym = self.laskeysym
        n = self.loc[tag]
        if (sym == "Left"):
            self.propertys[n][19] -= 1
            return
        if (sym == "Right"):
            self.propertys[n][19] += 1
            return
        if (sym == 'BackSpace'):
            if len(self.propertys[n][10]) == 0:
                self.propertys[n][10] = self.propertys[n][14]
                self.propertys[n][19] = len(self.propertys[n][10])
            self.propertys[n][10] = self.propertys[n][10][:self.propertys[n][19]-1]+self.propertys[n][10][self.propertys[n][19]:]
            self.propertys[n][19] -= 1

            return
        if(self.propertys[n][15] != None): #checks whitelist
            if not(key in self.propertys[n][15]):
                return
        if (self.propertys[n][16] != None): #checks blacklist
            if  (key in self.propertys[n][16]):
                return

        if (self.propertys[n][17] == False and self.propertys[n][10] == self.propertys[n][14]):
            self.propertys[n][10] = key
            return
        self.propertys[n][10] = self.propertys[n][10][:self.propertys[n][19]] + key + self.propertys[n][10][self.propertys[n][19]:]
        self.propertys[n][19]+=1

    def draggable(self,tag,x,y,xp,yp,parent=None,active=True,lockX=False,lockY=False,snapToMouse=False,clicktype=1):
        self.loc[tag] = self.n
        self.propertys.append(["draggable", tag, active, parent, [], x, y, xp-x, yp-x, lockX,lockY,snapToMouse,0,0,clicktype])
        self.n += 1
        if parent != None:
            self.propertys[self.loc[parent]][4].append(tag)
        if active:
            self.clickUpdates1.append(tag)
    def __updateDraggable__(self,tag):
        n = self.loc[tag]
        a = self.__calcVis__(tag)

        if a and not(tag in self.clickUpdates1):
            self.clickUpdates1.append()
        elif not(a) and tag in self.clickUpdates1:
            self.clickUpdates1.remove(tag)
        loc = self.__calcloc__(tag)
        x, y = loc[0], loc[1]
        if self.mousedown[self.propertys[n][14]-1] == True:

            if not(self.propertys[n][9]):
                differenceX = self.mX-x-self.propertys[n][12]
                self.propertys[n][5] += differenceX
            if not (self.propertys[n][10]):
                differenceY = self.mY - y - self.propertys[n][13]
                self.propertys[n][6] += differenceY


        else:
            self.mouseMoveUpdates.remove(tag)
        self.__updateChildren__(tag)
    def __selectDraggable__(self,tag):
        n = self.loc[tag]
        a = self.__calcVis__(tag)
        if not(a):
            self.clickUpdates1.remove(tag)
        if (self.clicktype == self.propertys[n][14]):
            loc = self.__calcloc__(tag)

            x,y = loc[0],loc[1]

            if inArea(x,y,x+self.propertys[n][7],y+self.propertys[n][8],self.mX,self.mY):
                if not( tag in self.mouseMoveUpdates):
                    self.mouseMoveUpdates.append(tag)
                if(self.propertys[n][11]==False):
                    self.propertys[n][12] = self.mX-self.propertys[n][5]
                    self.propertys[n][13] = self.mY - self.propertys[n][6]
                else:
                    self.propertys[n][12] = self.propertys[n][7]/2
                    self.propertys[n][13] = self.propertys[n][8]/2


    def __calcY__(self,n):
        return n*self.winY/self.i
    def __calcX__(self,n):
        return n*self.winX/self.i

    def __updateChildren__(self,tag):
        n= self.loc[tag]
        for i in self.propertys[n][4]:
            self.__update_item__(i)
            self.__updateChildren__(i)
    def __calcloc__(self,tag):
        x, y = 0, 0

        t = tag
        n = self.loc[t]
        x += self.propertys[n][5]
        y += self.propertys[n][6]

        while True:
            tn = self.loc[t]
            if (self.propertys[tn][3] == None):
                break
            t = self.propertys[tn][3]
            tn = self.loc[t]
            x += self.propertys[tn][5]
            y += self.propertys[tn][6]
        return (x,y)

    def __calcVis__(self,tag):
        active = True
        t = tag
        n = self.loc[t]
        if (self.propertys[n][2] == False):
            active = False
        while True:
            tn = self.loc[t]
            if (self.propertys[tn][3] == None):
                break
            t = self.propertys[tn][3]
        if (self.propertys[tn][2] == False):
            active = False
        return active

    def set(self,tag,loc,value):
        if self.propertys[self.loc[tag]][self.lookup[self.propertys[self.loc[tag]][0]][loc]] != value and(tag in self.actives or loc == "active"):
            self.propertys[self.loc[tag]][self.lookup[self.propertys[self.loc[tag]][0]][loc]] = value
            if(loc == "color"):
                self.canvas.itemconfig(self.objects[tag],fill=value,outline=value)
            elif(loc == "outline"):
                self.canvas.itemconfig(self.objects[tag],outline=value)
            elif (loc == "fill"):
                self.canvas.itemconfig(self.objects[tag], fill=value)
            elif (loc == "text"):
                self.canvas.itemconfig(self.objects[tag],text=value)
            else:
                self.__update_item__(tag)
    def get(self,tag,loc):
        return(self.propertys[self.loc[tag]][self.lookup[self.propertys[self.loc[tag]][0]][loc]])
