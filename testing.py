from AguiV2 import window
from tkinter import *


App = window.Window()
App.line("a",20,20,30,30)



while App.running:
    App.set("a","x",App.mX)
    App.set("a", "y", App.mY)
    if App.mX >= 50:
        App.set("a","active",False)
    else:
        App.set("a", "active", True)
    App.update()


