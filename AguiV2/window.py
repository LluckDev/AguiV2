from tkinter import *


#window class
class Window():
    def __init__(self, grid=100, screenX=800, screenY=520, bgc="#ffffff", fullscreen=False, title="Agui"):


        # objects
        self.objects = {} # dict [id : object]
        self.loc = {} # dict [id : n]
        self.propertys = [] # array [type,tag,active,parent,[children],x,y,args*]
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


        # vars
        self.running = True
        self.winX = screenX
        self.winY = screenY
        self.mX = 0
        self.mY = 0



        #lookup
        self.lookup = {
            "point":{"tag":1,"active":2,"parent":3,"children":4,'x':5,'y':6,'radius':7,'stroke':8}
        }
        self.updateLookup={
            "point":self.__updatePoint__
        }
        self.activeLookup={True:"normal",False:"hidden"}

    def close(self):
        self.running=False
        self.disp.destroy()



    def update(self):
        if(self.winY-self.disp.winfo_height()!=0 or self.winX-self.disp.winfo_width()!=0):
            self.winY = self.disp.winfo_height()
            self.winX = self.disp.winfo_width()
            self.canvas.config(width=self.winX, height=self.winY)
            for i in self.loc:
                self.__update_item__(i)

        self.mX = (self.i/self.winX)*(self.disp.winfo_pointerx()-self.disp.winfo_x()-8)
        self.mY = (self.i/self.winY)*(self.disp.winfo_pointery()-self.disp.winfo_y()-30)




        # update backend (Last)

        self.disp.update()
        self.disp.update_idletasks()


    def __update_item__(self,tag):
        self.updateLookup[self.propertys[self.loc[tag]][0]](tag)



    def point(self,tag,x,y,radius=1,stroke="#000000",active=True,parent=None):
        self.objects[tag] = self.canvas.create_oval(x, y, x, y, fill=stroke)
        self.loc[tag] = self.n
        self.propertys.append(["point",tag,active,parent,[],x,y,radius,stroke])
        self.n +=1
        if parent != None:
            self.propertys[self.loc[parent]][4].append(tag)

        self.__updatePoint__(tag)

    def __updatePoint__(self,tag):
        self.__updateChildren__(tag)
        x,y=0,0
        t = tag
        n = self.loc[t]
        x += self.propertys[n][5]
        y += self.propertys[n][6]
        while True:
            tn = self.loc[t]
            if(self.propertys[tn][3]==None):
                break
            t = self.propertys[tn][3]
            tn = self.loc[t]
            x += self.propertys[tn][5]
            y += self.propertys[tn][6]


        self.canvas.coords(self.objects[tag],self.__calcX__(x)+(self.propertys[n][7]/2),self.__calcY__(y)+(self.propertys[n][7]/2),self.__calcX__(x)-(self.propertys[n][7]/2),self.__calcY__(y)-(self.propertys[n][7]/2))







    def __calcY__(self,n):
        return n*self.winY/self.i
    def __calcX__(self,n):
        return n*self.winX/self.i

    def __updateChildren__(self,tag):
        n= self.loc[tag]
        for i in self.propertys[n][4]:
            self.__update_item__(i)
            self.__updateChildren__(i)



    def set(self,tag,loc,value):
        self.propertys[self.loc[tag]][self.lookup[self.propertys[self.loc[tag]][0]][loc]]=value
        self.__update_item__(tag)