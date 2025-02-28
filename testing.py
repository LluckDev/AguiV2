from AguiV2 import window
from tkinter import *


App = window.Window()

App.point("a",20,20,radius=5)
App.point("b",50,50,radius=5,parent="a")


while App.running:
    App.set("a","x",App.mX)
    App.set("a", "y", App.mY)
    App.update()


