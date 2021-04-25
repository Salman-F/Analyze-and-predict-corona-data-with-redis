from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from contextlib import contextmanager
import sys, os

class AbstractForecast(ABC):
    def __init__(self, redisDB, futureCast, titel):
        self.redisData = redisDB.getRedisData()
        self.future = futureCast
        self.result = None
        self.orgDataExtended = None
        self.titel = titel

    @abstractmethod
    def getForecast(self):
        pass

    def extendOrgData(self, npArray):
        npTemp = np.zeros((self.future), dtype=int)
        npAddedValues= np.concatenate((npArray, npTemp), axis=None)
        self.orgDataExtended = self.zeroToNan(npAddedValues)

    def zeroToNan(self, values):
        return [float('nan') if x==0 else x for x in values]

    def showResult(self):
        plot = plt.figure()
        plt.get_current_fig_manager().canvas.set_window_title(self.titel)
        dateAxes = pd.date_range(start=self.redisData["date"][0], periods=len(self.redisData)+self.future, freq='D')
        plt.plot(dateAxes, self.orgDataExtended, 'b', label = 'daily changes', linewidth = 1.5)        
        plt.plot(dateAxes, self.result,"r", label = 'Predicted Values')
        plt.legend()
    
    @contextmanager
    def suppress_stdout(self):
        with open(os.devnull, "w") as devnull:
            old_stdout = sys.stdout
            sys.stdout = devnull
            try:  
                yield
            finally:
                sys.stdout = old_stdout

