from AguiV2 import window

App = window.Window()

App.text("a",10,10,10,"hi",font="Monomakh")
while App.running:
    App.update()

