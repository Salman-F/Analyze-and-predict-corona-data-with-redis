from Model import ModelMVC
from View import ViewMVC
from tkinter import *

class ControllerMVC():
    def __init__(self):
        self.master = Tk()
        self.model = ModelMVC()
        self.view = ViewMVC(self.master, self.model)

    def run(self):
        self.master.title("Choose the state you are interested in")
        self.view.plot()
        self.master.mainloop()
        return self.view.getRetVal()