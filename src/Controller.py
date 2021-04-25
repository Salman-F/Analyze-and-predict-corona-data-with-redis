"""Controller
    Contains the Controller class needed for the MVC model
    
    Attributes:
        * name: SALFIC
        * date: 25.04.2021
        * version: 0.0.1 Beta- free
"""

from Model import ModelMVC
from View import ViewMVC
from tkinter import *

class ControllerMVC():
    """ControllerMVC
        Controlls the model and the view
    """
    def __init__(self):
        """Initits the model and view needed for the controller
        """
        self.master = Tk()
        self.model = ModelMVC()
        self.view = ViewMVC(self.master, self.model)

    def run(self):
        """run
            Controls the shown frame and the data of the model
        Returns:
            str: Contains the state the user wants to analyze the corona data from
        """
        self.master.title("Choose the state you are interested in")
        self.model.fillValues()
        self.view.plot(self.model.getValues())
        self.master.mainloop()
        return self.view.getRetVal()