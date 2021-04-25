import warnings; 
warnings.filterwarnings("ignore")
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np
from AbstractForecast import *

class HWForecast(AbstractForecast):
    def getForecast(self):
        lenOfData = len(self.redisData.index)
        npArray = np.empty(shape=(1,lenOfData), dtype=int)
        for i in range (lenOfData):
            npArray[0][i] = self.redisData["data"][i]
        
        self.extendOrgData(npArray[0])
        
        model = ExponentialSmoothing(npArray[0], seasonal_periods=12, trend="add", seasonal="mul")
        model_fit = model.fit()        

        predictYhat = model_fit.predict(1, (npArray.size + self.future))
        self.result = predictYhat
