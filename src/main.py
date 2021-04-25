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
    * analyse the data          // In work
    * build prophet     //Done -- suppress loginfo 
    * fft               //Done
    * machine learning //Done
    * Doc Strings 
    * Read me
    * tests unittests
"""
from RedisClient import *
from ProphetForecast import *
from FourierForecast import *
from SARIMAForecast import *
from Controller import *
from HoltWitnersForecast import *
from AnalyzeLockdown import *
import matplotlib.pyplot as plt
import os
import time

def main():
    ###This Variable declares how many days should be forecasted
    ############################################################
    FutureCast = 10
    ############################################################
    ############################################################
    #window = ControllerMVC()
    #state = window.run()
    state = ""
    if state == "":
        state = "DE-BW"
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
    
    HWTitel = "Holt Winter's Exponenial Smoothing"
    FFTTitel = "Fast Fourier Transformation"
    SARIMATitel = "SARIMA machine learning"
    FBProphetTitel = "FB Prophet Forecast"

    #HWObj = HWForecast(redisDB, FutureCast, HWTitel)
    #HWObj.getForecast()

    #fourierTransObj = FourierForecast(redisDB, FutureCast, FFTTitel)
    #fourierTransObj.getForecast()

    #sarimaObj = SARIMAForecast(redisDB, FutureCast, SARIMATitel)
    #sarimaObj.getForecast()

    fbProphetObj = FbProphetForecast(redisDB, FutureCast, FBProphetTitel)
    fbProphetObj.getForecast()

    #HWObj.showResult()
    #fourierTransObj.showResult()
    #sarimaObj.showResult()
    #fbProphetObj.showResult()
    os.system('cls' if os.name == 'nt' else 'clear')
    #AnObj = Lockdown(redisDB, 100, 200)
    #AnObj.lockdownPhases()
    plt.show()
    redisDB.flushDB()

if __name__ == "__main__":
    main()