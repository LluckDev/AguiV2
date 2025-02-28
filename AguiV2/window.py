from tkinter import *


#window class
class Window():
    def __init__(self, grid=100, screenX=800, screenY=520, bgc="#ffffff", fullscreen=False, title="Agui"):


        # objects
        self.objects = {} # dict [id : object]
        self.loc = {} # dict [id : n]
        self.propertys = [] # array [type,tag,active,parent,[children],args*]
        self.n = 0 # total number of objects


        # window setup
        self.disp = Tk()
        self.disp.configure(bg=bgc)
        self.disp.geometry(str(screenX) + "x" + str(screenY))
        self.disp.title(title)
        self.canvas = Canvas(self.disp, width=self.disp.winfo_width() / 1.25,
                             height=self.disp.winfo_height() / 1.25, bg=bgc)
        if fullscreen:
            self.disp.state('zoomed')
        self.canvas.pack()
        self.i = grid


        # vars
        self.running = True



        #lookup
        self.lookup = {
            "point":{"tag":1,"active":2,"parent":3,"children":4,'x':5,'y':6,'radius':7,'stroke':8}
        }




    def update(self):






        # update backend (Last)
        self.disp.update_idletasks()
        self.disp.update()




    def point(self,tag,x,y,radius=1,stroke="#000000",active=True,parent=None):
        self.objects[tag] = self.canvas.create_line(x, y, x, y, width=radius, fill=stroke)
        self.loc[tag] = self.n
        self.propertys.append(["point",tag,active,parent,[],x,y,radius,stroke])
        self.n +=1
        if parent != None:
            self.propertys[self.loc[parent]][4].append(tag)
        if not(active):
            self.canvas.itemconfig(self.objects[tag], state="hidden")