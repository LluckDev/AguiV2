from AguiV2 import window

App = window.Window()

def i():
    App.set("a","x",App.get("a","x")+1)
def o():
    App.set("a","x",App.get("a","x")-1)
def p():
    App.set("a","y",App.get("a","y")+1)
App.rect("a",5,5,25,25)
App.hitbox("b",0,0,20,20,i,parent="a")
while App.running:
    App.update()

