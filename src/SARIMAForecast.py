"""SARIMAForecast
    SARIMA machine learning algorithm to forecast new corona cases per day.
    
    Attributes:
        * name: SALFIC
        * date: 25.04.2021
        * version: 0.0.1 Beta- free
"""
from AbstractForecast import *
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np

class SARIMAForecast(AbstractForecast):
    """SARIMAForecast
        The SARIMA Forecast predicts future corona data with the implemented SARIMA machine learning algorithm.
    
    Args:
        AbstractForecast (ABC): Abstract class this class inherits from. Implementation of abstract funtions is needed.
    """
    def getForecast(self):
        """getSARIMAForecast
            Creates a Model with the fetched data from the redis databse.
            This Model is fitted and creates a prediction at the end.
            Therfore a numpyArray containing all y values is created and taken to create the model.
            The result is stored in the class variable: result.
        """
        lenOfData = len(self.redisData.index)
        npArray = np.empty(shape=(1,lenOfData), dtype=int)
        # Iterate through the fetched redisData and filter all values
        for i in range (lenOfData):
            npArray[0][i] = self.redisData["data"][i]
        
        self.extendOrgData(npArray[0])
        ## SARIMA(p,d,q)(P,D,Q)m
        ## Configuration for seasonality, trend import for model
        myOrder = (2, 2, 1)
        mySeasonal_order = (2, 1, 1, 12)
        model = SARIMAX(npArray[0], order=myOrder, seasonal_order=mySeasonal_order)
        ## Fit Model
        model_fit = model.fit(disp=False)

        # Make prediction
        predictYhat = model_fit.predict(1, (npArray.size + self.future))
        
        self.result = predictYhat