"""HoltWitnersForecast
    * Holt Winter's Exponential Smoothing machine learning algorithm to forecast corona cases.
    
    Attributes:
        * name: SALFIC
        * date: 24.04.2021
        * version: 0.0.1 Beta- free
"""
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np
from AbstractForecast import *

class HWForecast(AbstractForecast):
    """HWForecast
        * Contains the algorithm to create and fit a model to forecast data.

    Args:
        AbstractForecast (ABC): Abstract class this class inherits from. Implementation of abstract funtions is needed.
    """
    def getForecast(self):
        """getForecast
            * Predicts future values with the fitted ExponentialSmoothing model.
            * Therfore a numpyArray containing all y values is created and taken to create the model.
            * The result is stored in the class variable: result.
        """
        lenOfData = len(self.redisData.index)
        npArray = np.empty(shape=(1,lenOfData), dtype=int)
        # Iterate through the fetched redisData and filter all values
        for i in range (lenOfData):
            npArray[0][i] = self.redisData["data"][i]
        
        extendedData = self.extendOrgData(npArray[0])
        # create model and fit model
        model = ExponentialSmoothing(npArray[0], seasonal_periods=12, trend="add", seasonal="mul")
        model_fit = model.fit()        
        # make prediction 
        predictYhat = model_fit.predict(1, (npArray.size + self.future))
        self.result = predictYhat
