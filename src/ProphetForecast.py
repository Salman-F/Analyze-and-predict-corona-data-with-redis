"""ProphetForecast
    * Facebooks Prophet algortihm to forecast corona cases.
    
    Attributes:
        * name: SALFIC
        * date: 24.04.2021
        * version: 0.0.1 Beta- free

TODO:
    * Suppress Logging info from prophet
"""

from AbstractForecast import *
import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt


class FbProphetForecast(AbstractForecast):
    """FbProphetForecast
        * The Facebook Prophet Algorithm forecast corona data with the given prophet algorithm.
        * The Fetched data from the database needs to be adjusted to the used algorithm.
    
    Args:
        AbstractForecast (ABC): Abstract class this class inherits from. Implementation of abstract funtions is needed.
    """
    def getForecast(self):
        """getFbForecast
            * Converts the fetched Data into a form the Prophet algorithm can process.
            * Creates and fits a Prophet model that generate a forecast
            * FbProphet uses its own plot method that is based on matplotlib but needs to be executed from the model.
            * Therfore a plot and its titel and size is created in here. The plot shows after the main function calls plot.show()
            * The result is stored in the class variable: result.
        """
        # Prophet algorithm needs dataframe to be in specific order with specific name
        self.redisData = self.redisData.rename(columns={"data":"y", "date":"ds"})        
        self.redisData = self.redisData[["y", "ds"]]
        # creates model
        model = Prophet(interval_width=0.95, daily_seasonality=True, yearly_seasonality=True,weekly_seasonality=True)        
        # changepoints=str(formatDf['ds'].iloc[-1]).split(' ')[0]
        # fitting model and make prediction
        model.fit(self.redisData)
        future = model.make_future_dataframe(periods=self.future,freq='D')
        forecast = model.predict(future)
        # Setting figure variables and creating a plot because of the special plotting of the fbProphet
        plt1 = model.plot(forecast)
        plt.get_current_fig_manager().canvas.set_window_title(self.titel)
        plt.get_current_fig_manager().resize(644,480)

        self.result = forecast

    def showResult(self):
        """showResult
            * This function is not needed here because of the included plotting within the fbProphet algorithm.
            * Overrides this function for this specific class. For other classes that inherit from AbstracForecast this
                function stays the same.
        """
        pass