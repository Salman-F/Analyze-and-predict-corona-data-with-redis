"""unittestsAbstractForecast
    * File for unittests regarding all methods included in AbstractForecast
    
    Attributes:
        * name: SALFIC
        * date: 26.04.2021
        * version: 0.0.1 Beta- free
"""
import unittest
import numpy as np
from SARIMAForecast import *
from RedisClient import *

class TestAbstractForecast(unittest.TestCase):
    """TestAbstractForecast
        * Contains unittests for AbstractForecast 

    Args:
        unittest (unittest): Inherits from unittest to contain all functionaliities
    """
    def setUp(self):
        """setUp
            * Because AbstractForecast is a abstract class and the SARIMAObj is inherited from it
                this object can be used to test the implemented function
        """
        self.redisDB = RedisClient()
        # Clear and fill database to avoid wrong values
        self.redisDB.flushDB()
        self.redisDB.fillRedisDatabase()
        # Database should be filled
        self.testFutureCast = 10
        self.AbstractForecastObj = SARIMAForecast(self.redisDB, self.testFutureCast, "none")

    def testZeroToNan(self):
        """testZeroToNan
            * Tests if a array initialized with zeros contains zeros after callinf the zeroToNan function
        """
        # Makes numpy array with 50 zeros
        npTemp = np.zeros((50), dtype=int)
        npTemp = self.AbstractForecastObj.zeroToNan(npTemp)
        for i in npTemp:
            self.assertNotEqual(0, i)
        print("Zero to Nan test passed successfully!")

    def testExtensionOrgData(self):
        """testExtensionOrgData
            * Tests if the original data is expanded successfully to match the x values of forecasted methods
        """
        orgData = self.redisDB.getRedisData()
        futureVal = self.testFutureCast
        
        totalLength = orgData.size + futureVal
        returnedLength = len(self.AbstractForecastObj.extendOrgData(orgData))
        self.assertEqual(totalLength, returnedLength)
        print("Extending original data passes successfully!")
        
if __name__ == "__main__":
    unittest.main()