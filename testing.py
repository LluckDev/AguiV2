from AguiV2 import window

App = window.Window()
App.rect("b",10,10,50,50,fill="#eeeeee")
App.textbox("a",10,10,50,50,10,defualtValue="1000000000")

while App.running:
    App.update()

