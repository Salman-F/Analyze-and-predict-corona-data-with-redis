"""AbstractForecast
    Abstract class other forecast algorithm can inherit beacause 
    a lot of methods are similar within the different algorithms
    
    Attributes:
        * name: SALFIC
        * date: 25.04.2021
        * version: 0.0.1 Beta- free

Example:
    None

TODO:
    
"""
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class AbstractForecast(ABC):
    """AbstractForecast
        Implements the main methods a forecast algorithm should have.

    Args:
        ABC (abc): Gurantees that no instances of this class are made
    """
    def __init__(self, redisDB, futureCast, titel):
        """Inits the main attributes of a forecast algorithm

        Args:
            redisDB (redis Client): Contains the redis connection
            futureCast (int): Describes the amount of days the algorithm should estimate into the future
            titel (str): Is needed to Plot a correct Titel
        """
        self.redisData = redisDB.getRedisData()
        self.future = futureCast
        self.result = None
        self.orgDataExtended = None
        self.titel = titel

    @abstractmethod
    def getForecast(self):
        """getForecast
            Abstractmethod is implemented in each class that inherites this class
        """
        pass

    def extendOrgData(self, npArray):
        """extendOrgData
            To print the original corona data with the forecasted data the length of both x values need to be the same.
            This function adds an numpy Array with the size of the prediction value to the end of the original values

        Args:
            npArray (numpyArray): Contains the x Values of the original corona data
        """
        npTemp = np.zeros((self.future), dtype=int)
        npAddedValues= np.concatenate((npArray, npTemp), axis=None)
        self.orgDataExtended = self.zeroToNan(npAddedValues)

    def zeroToNan(self, values):
        """zeroToNan
            Replaces Zeros to NaN and returns a copy. Reason is that Matplotlib should not print the added zeros at the end.

        Source:
            * https://stackoverflow.com/questions/18697417/not-plotting-zero-in-matplotlib-or-change-zero-to-none-python

        Args:
            values (numpyArray): Contains the original corona data with the added zero values for plotting reason

        Returns:
            numpyArray: Copy that Replaced all zeros to Nans
        """
        return [float('nan') if x==0 else x for x in values]

    def showResult(self):
        """showResult
            Creates a plot to show the forecasted and original data in one figure.
            Sets the Figure Titel and creates daterange to match the addetional days given by the forecast algorithm.
            After all plots are created the main function calls plt.show() to display them
        """
        plot = plt.figure()
        plt.get_current_fig_manager().canvas.set_window_title(self.titel)
        # Create date values for the complete data including the forecastet data
        dateAxes = pd.date_range(start=self.redisData["date"][0], periods=len(self.redisData)+self.future, freq='D')       
        plt.plot(dateAxes, self.result,"r", label = 'Predicted Values')
        plt.plot(dateAxes, self.orgDataExtended, 'b', label = 'daily changes', linewidth = 1.5) 
        plt.legend()