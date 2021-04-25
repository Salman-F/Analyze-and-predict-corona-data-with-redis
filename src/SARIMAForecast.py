"""SARIMAForecast
    Machine learning algorithm to forecast new corona cases per day.
    
    Attributes:
        * name: SALFIC
        * date: 24.04.2021
        * version: 0.0.1 Beta- free

Example:
    None

TODO:
    * 
"""
from AbstractForecast import *
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np

class SARIMAForecast(AbstractForecast):
    """SARIMAForecast
        The SARIMA Forecast predicts future corona data with the implemented SARIMA machine learning algorithm.
    """
    def getForecast(self):
        """getSARIMAForecast
            Creates a Model with the fetched data from the redis databse.
            This Model is fitted and creates a prediction at the end

        Returns:
            List: Includes all corona values from the start of the given data to the end with the additional prediction
        """
        lenOfData = len(self.redisData.index)
        npArray = np.empty(shape=(1,lenOfData), dtype=int)
        for i in range (lenOfData):
            npArray[0][i] = self.redisData["data"][i]
        self.extendOrgData(npArray[0])
        ## SARIMA(p,d,q)(P,D,Q)m
        ## Test Configuration
        myOrder = (2, 2, 1)
        mySeasonal_order = (2, 1, 1, 12)
        model = SARIMAX(npArray[0], order=myOrder, seasonal_order=mySeasonal_order)
        ## Fit Model
        model_fit = model.fit(disp=False)
        ## Make Prediction
        yhat = model_fit.predict(start=len(npArray[0]), end=len(npArray[0]))
        ## forecast on data
        #forcasPredic = model_fit.forecast(prediction)
        # Make prediction
        predictYhat = model_fit.predict(1, (npArray.size + self.future))
        
        self.result = predictYhat