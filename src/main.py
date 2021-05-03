"""main
    Main function to analysze corona data with redis and forecast corona data with 
    FFT, Facebook Prophet and machine learning algorithms.
    
    Attributes:
        * name: SALFIC
        * date: 30.04.2021
        * version: 0.0.1 Beta- free
        
TODO:
    * Put data in redis server with queue // In work... Not Possible
"""
from RedisClient import *
from ProphetForecast import *
from FourierForecast import *
from SARIMAForecast import *
from Controller import *
from HoltWintersForecast import *
from AnalyzeCoronaData import *
from unittests.unittestsAbstractForecast import *
from unittests.unittestsRedisClient import *
import matplotlib.pyplot as plt

def main(args):
    """main
        main function controls program flow.
        creates objects and calls needed methods.
    """
    ###This Variable declares how many days should be forecasted
    ###And if Plots are shown###################################
    if len(args) > 0 and len(args) < 5:
        FutureCast = int(args[0])
        showAnalyzedData = bool(args[1])
        showForecastPlots = bool(args[2])
        prophetIncluded = bool(args[3])
    else:
        FutureCast = 10
        showAnalyzedData = True
        showForecastPlots = True
        prophetIncluded = True
    ############################################################
    ############################################################
    
    # Window to chose german state to analyze
    window = ControllerMVC()
    state = window.run()
    # Builds Connection to redis server
    try:
        redisDB = RedisClient(_state=state)
    except Exception as generalError:
        print(f"Somethin went wrong connecting to redis: {generalError}")
        return

    # Fetching data and storing in redis Server
    try:
        redisDB.fillRedisDatabase()
    except Exception as generalError:
        print(f"Somethin went wrong: {generalError}")
        return
    
    if showAnalyzedData == True:
        AnObj = AnalyzeCorona(redisDB)
        AnObj.coronaPeaksIncident()
        AnObj.averageCoronaIncident()

    HWTitel = "Holt Winter's Exponenial Smoothing"
    FFTTitel = "Fast Fourier Transformation"
    SARIMATitel = "SARIMA machine learning"
    FBProphetTitel = "FB Prophet Forecast"

    # Create objects and call forecast function

    HWObj = HWForecast(redisDB, FutureCast, HWTitel)
    HWObj.getForecast()

    fourierTransObj = FourierForecast(redisDB, FutureCast, FFTTitel)
    fourierTransObj.getForecast()

    sarimaObj = SARIMAForecast(redisDB, FutureCast, SARIMATitel)
    sarimaObj.getForecast()

    if prophetIncluded == True:
        fbProphetObj = FbProphetForecast(redisDB, FutureCast, FBProphetTitel)
        fbProphetObj.getForecast()

    if showForecastPlots == True:
        # Create subplots for forecasting methods
        fig, ax = plt.subplots(3)
        HWObj.showResult(ax,0)
        fourierTransObj.showResult(ax,1)
        sarimaObj.showResult(ax,2)
        # To prevent overlaping of titels
        plt.tight_layout()
        plt.show()
        
    ###########################################Unittests Section
    ############################################################  
    testAbstractFr = TestAbstractForecast()
    testAbstractFr.run()
    testRedisCli = TestRedisClient()
    testRedisCli.run()
    ############################################################
    ############################################################ 
    #redisDB.flushDB()

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)