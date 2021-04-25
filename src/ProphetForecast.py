"""ProphetForecast
    Facebooks Prophet algortihm to forecast corona cases.
    
    Attributes:
        * name: SALFIC
        * date: 24.04.2021
        * version: 0.0.1 Beta- free

Example:
    None

TODO:
    * Suppress Logging info from prophet
"""
import warnings; 
warnings.simplefilter('ignore')
from AbstractForecast import *
import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt


class FbProphetForecast(AbstractForecast):
    """FbProphetForecast
        The Facebook Prophet Algorithm forecast corona data with the given prophet algorithm.
        The Fetched data from the database needs to be adjusted to the used algorithm.
    """
    def getForecast(self):
        """getFbForecast
            Converts the fetched Data into a form the Prophet algorithm can process.
            Creates and fits a Prophet model that generate a forecast

        Returns://///TODO
            [type]: [description]
        """
        # Prophet algorithm needs dataframe to be in specific order with specific name
        self.redisData = self.redisData.rename(columns={"data":"y", "date":"ds"})        
        self.redisData = self.redisData[["y", "ds"]]

        model = Prophet(interval_width=0.95, daily_seasonality=True, yearly_seasonality=True,weekly_seasonality=True)        
        # changepoints=str(formatDf['ds'].iloc[-1]).split(' ')[0]
        model.fit(self.redisData)
        future = model.make_future_dataframe(periods=self.future,freq='D')
        forecast = model.predict(future)
        plt1 = model.plot(forecast)
        plt.get_current_fig_manager().canvas.set_window_title(self.titel)
        self.result = forecast

    def showResult(self):
        pass