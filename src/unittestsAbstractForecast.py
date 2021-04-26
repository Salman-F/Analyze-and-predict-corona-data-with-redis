"""unittestsAbstractForecast
    * File for unittests regarding all methods included in AbstractForecast
    
    Attributes:
        * name: SALFIC
        * date: 26.04.2021
        * version: 0.0.1 Beta- free
"""
import unittest
import numpy as np

class TestAbstractForecast(unittest.TestCase):
    """TestAbstractForecast
        * Contains unittests for AbstractForecast 

    Args:
        unittest (unittest): Inherits from unittest to contain all functionaliities
    """
    def __init__(self, SARIMAObj):
        """Inits TestAbstractForecast
            * Because AbstractForecast is a abstract class and the SARIMAObj is inherited from it
                this object can be used to test the implemented function

        Args:
            SARIMAObj (SARIMAForecast): Contains all methods implemented in AbstractForecast
        """
        self.AbstractForecastObj = SARIMAObj

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

    def testExtensionOrgData(self, orgData, futureVal):
        """testExtensionOrgData
            * Tests if the original data is expanded successfully to match the x values of forecasted methods

        Args:
            orgData (DataFrame): Contains the original data from redis
            futureVal (int): Describes the predict values (herefore the excess values from forecast methods)
        """
        totalLength = orgData.size + futureVal
        returnedLength = len(self.AbstractForecastObj.extendOrgData(orgData))
        self.assertEqual(totalLength, returnedLength)
        print("Extending original data passes successfully!")

