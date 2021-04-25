"""View
    Contains the View class for the MVC model
    
    Attributes:
        * name: SALFIC
        * date: 25.04.2021
        * version: 0.0.1 Beta- free
"""
from tkinter import *
class ViewMVC():
    """ViewMVC
        Creates the Buttons that should be shown in the mein frame
    """
    def __init__(self, root, model):
        """Inits the View class

        Args:
            root (Tk Object): Contains the frame that should be displayed
            model (ModelMVC): Contains the model and herfore the data 
        """
        self.frame = root
        self.model = model
        self.returnVal = ""

    def closeWindow(self,x):
        """closeWindow
            Destroys the view and saves the value of the pressed button

        Args:
            x (str): Value of the given Button
        """
        self.frame.destroy()
        self.returnVal = x

    def plot(self, values):
        """plot
            Plots all Buttons on the given frame and performs action on click. Defined in command=
        Args:
            values (dict): Contain the information the be displayed
        """
        v = StringVar(self.frame, "1")
        self.frame.geometry("400x560")
        for (text, value) in values.items():
            Radiobutton(self.frame, text = text, variable = v,
                        value = value, indicator = 0,
                        background = "light green", command=lambda x=value:self.closeWindow(x)).pack(fill = X, ipady = 5)

    def getRetVal(self):
        """getRetVal
            Return the saved value from funtionc closeWindow.
            Should the variable be empty a default value will be returned

        Returns:
            str: Contains the state the user chose
        """
        if self.returnVal == "":
            return "DE-BW"
        else:
            return self.returnVal