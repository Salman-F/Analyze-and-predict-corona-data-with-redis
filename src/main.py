"""main
    Main function to analysze corona data with redis and forecast corona data with 
    FFT, Facebook Prophet and machine learning algorithms.
    
    Attributes:
        * name: SALFIC
        * date: 24.04.2021
        * version: 0.0.1 Beta- free
        
TODO:
    * Put data in redis server with queue // In work... Not Possible
    * build hasehs in redis server // Done
    * analyse the data          // Done
    * build prophet     //Done -- suppress loginfo 
    * fft               //Done
    * machine learning //Done
    * Doc Strings // Add while coding
    * Read me
    * tests unittests
"""
from RedisClient import *
from ProphetForecast import *
from FourierForecast import *
from SARIMAForecast import *
from Controller import *
from HoltWitnersForecast import *
from AnalyzeCoronaData import *
import matplotlib.pyplot as plt
import os

def main():
    """main
        main function controls program flow.
        creates objects and calls needed methods.
    """
    ###This Variable declares how many days should be forecasted
    ###And if Plots are shown###################################
    
    FutureCast = 10
    showAnalyzedData = True
    showForecastPlots = True
    
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

    fbProphetObj = FbProphetForecast(redisDB, FutureCast, FBProphetTitel)
    fbProphetObj.getForecast()

    if showForecastPlots == True:
        HWObj.showResult()
        fourierTransObj.showResult()
        sarimaObj.showResult()
        fbProphetObj.showResult()
        plt.show()
    
    os.system('cls' if os.name == 'nt' else 'clear')
    redisDB.flushDB()

if __name__ == "__main__":
    main()