from tkinter import *

class ViewMVC():
    def __init__(self, root, model):    
        self.frame = root
        self.model = model
        self.returnVal = ""

    def closeWindow(self,x):
        self.frame.destroy()
        self.returnVal = x

    def plot(self):
        v = StringVar(self.frame, "1")
        self.frame.geometry("400x560")
        for (text, value) in self.model.fillValues().items():
            Radiobutton(self.frame, text = text, variable = v,
                        value = value, indicator = 0,
                        background = "light green", command=lambda x=value:self.closeWindow(x)).pack(fill = X, ipady = 5)

    def getRetVal(self):
        return self.returnVal