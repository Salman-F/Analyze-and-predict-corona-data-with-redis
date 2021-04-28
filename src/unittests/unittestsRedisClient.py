"""unittestsRedisClient
    * File for unittests regarding all methods included in RedisClient
    
    Attributes:
        * name: SALFIC
        * date: 26.04.2021
        * version: 0.0.1 Beta- free
"""
import unittest
import numpy as np
import pandas as pd
from RedisClient import *

class TestRedisClient(unittest.TestCase):
    """TestRedisClient
        * Contains unittests for RedisClient

    Args:
        unittest (unittest): Inherits from unittest to contain all functionaliities
    """
    def __init__(self):
        """Inits Test class
            * stores RedisClient Object in parameter
        """
        self.redisCli = RedisClient()
        # Clear and fill database to avoid wrong values
        self.redisCli.flushDB()
        self.redisCli.fillRedisDatabase()
        # Database should be filled
        self.originalData = self.fetchOriginalData()

    def testFillingDatabase(self):
        """testFillingDatabase
            * Tests if the length of the values in redis db matches the length of the original data
            * Requirement is that this instance of redis db is just used for this purpose
        """
        # If database is filled sucessfully it contains as many keys as days recorded

        orgDataFrame = self.fetchOriginalData()

        keysInDB = self.redisCli.getClient().keys()
        lengthOfKeys = len(keysInDB)
        numberOfDates = orgDataFrame.size

        self.assertNotEqual(lengthOfKeys, numberOfDates)
        print("Filling of database passes successfully!")

    def testPreprocessing(self):
        """testPreprocessing
            * Tests if the colm time_iso8601 still exists (should be renamed in csvPreprocessing)
            * Checks if the data contains 0 as values or negativ values (HoltWitner needs the data like that)
        """
        preProcessedData = self.redisCli.csvPreprocessing(self.originalData)

        for colm in preProcessedData:
            self.assertNotEqual(str(colm), "time_iso8601")      # Renaming of time column not sucessfull
            if colm == "date":
                continue
            else:
                for val in preProcessedData[colm]:               # Checks if any values are 0 or less then zero
                    self.assertNotEqual(val, 0)
                    self.assertLess(0, val)

        print("Preprocessing passed successfully!")

    def testGetRedisData(self):
        """testGetRedisData
            * Checks if the fetched data from redis db matches with the keys in redis db
            * Requirement is that this instance of redis db is just used for this purpose
            * Checks if date column is sorted
        """
        # returned dt should match the number of keys
        fetchedRedisDB = self.redisCli.getRedisData()
        keysInDB = self.redisCli.getClient().keys()
        self.assertNotEqual(len(fetchedRedisDB), keysInDB)       # Checks if fetched data is consistent with data in db

        # checks is sorted
        dateIndex = pd.Series(fetchedRedisDB["date"])
        # Checks if Series is monotonic increasing (in other words, if colm in df is sorted from getRedisData)
        ret = dateIndex.is_monotonic_increasing

        self.assertTrue(ret)
        print("Getting data form redis passes successfully!")

    def fetchOriginalData(self):
        """fetchOriginalData
            * Fetches original data from the source to compare with data stored in redis

        Raises:
            Exception: Raises Exception if a problem appears while fetching data from the url

        Returns:
            DataFrame: DataFrame fetched from the source
        """
        try:
            df = pd.read_csv(self.redisCli.getUrl())
        except Exception as urlError:
            raise Exception(urlError)
        
        return df
    
    def run(self):
        self.testFillingDatabase()
        self.testPreprocessing()
        self.testGetRedisData()