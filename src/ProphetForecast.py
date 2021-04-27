"""ProphetForecast
    * Facebooks Prophet algortihm to forecast corona cases.
    
    Attributes:
        * name: SALFIC
        * date: 24.04.2021
        * version: 0.0.1 Beta- free
"""

from AbstractForecast import *
import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt
import os


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
        with self.suppress_stdout_stderr():          # Important to suppress printing of fitting info in terminal 
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

    class suppress_stdout_stderr(object):
        """
            A context manager for doing a "deep suppression" of stdout and stderr in
            Python, i.e. will suppress all print, even if the print originates in a
            compiled C/Fortran sub-function.
            This will not suppress raised exceptions, since exceptions are printed
            to stderr just before a script exits, and after the context manager has
            exited (at least, I think that is why it lets exceptions through).

            Source:
                * https://github.com/facebook/prophet/issues/223
        """
        def __init__(self):
            # Open a pair of null files
            self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
            # Save the actual stdout (1) and stderr (2) file descriptors.
            self.save_fds = [os.dup(1), os.dup(2)]

        def __enter__(self):
            # Assign the null pointers to stdout and stderr.
            os.dup2(self.null_fds[0], 1)
            os.dup2(self.null_fds[1], 2)

        def __exit__(self, *_):
            # Re-assign the real stdout/stderr back to (1) and (2)
            os.dup2(self.save_fds[0], 1)
            os.dup2(self.save_fds[1], 2)
            # Close the null files
            for fd in self.null_fds + self.save_fds:
                os.close(fd)