from AguiV2 import window
from tkinter import *


App = window.Window()
App.line("a",0,0,20,20,thickness=1)
App.point("b",20,20,radius=5,parent="a")



while App.running:
    App.set("a","x",App.mX)
    App.set("a", "y", App.mY)
    if App.mX >= 50:
        App.set("a","active",False)
        App.set("b","color","#00ff00")
    else:
        App.set("a", "active", True)
        App.set("b", "color", "#ff0000")
    App.update()


