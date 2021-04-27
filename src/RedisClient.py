"""RedisClient
    * Controls all actions to communicate with redis database.
    * This File reads and writes to the database.
    * In most cases the configuration information needs to be adjusted
    * In most cases redisHost = "localhost", redisPw = "", redisPort should be always "6379"
    
    Attributes:
        * name: SALFIC
        * date: 24.04.2021
        * version: 0.0.1 Beta- free

TODO:
    * Queue for backround jobs // Not possible because of bugs: https://github.com/rq/rq/issues/758
"""

import redis
from rq import Queue
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

class RedisClient():
    """RedisClient
        * The Redis Client handles all operation regarding the redis database.
        * The databse can be filled with data and data can be fetched from the database.
        * Also some smaller functions like csvPreprocessing are implemented that makes the usage of the databse easier.
    """
    def __init__(self, _redisHost = "192.168.137.234", _redisPort = "6379", _redisPw = "redis", _state="DE-BW", _url="https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-state.csv"):
        """Inits RedisClient

        Args:
            _redisHost (str, optional): Includes the Ip Addres from the device your redis server is running. Defaults to "192.168.137.234".
            _redisPort (str, optional): Port to communicate with redis Server. Defaults to "6379".
            _redisPw (str, optional): Password to your redis server. Defaults to "redis".
            _url (str, optional): URL to a csv File for corona cases. Defaults to "https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-state.csv".
            _state (str, optional): Defines a german state the user wishes to know the corona cases from. Defaults to "DE-BW".
        """
        self.redisHost = _redisHost
        self.redisPort = _redisPort
        self.redisPw = _redisPw
        self.url = _url
        self.state = _state
        self.redClient = self.connectToRedisDB()

    def connectToRedisDB(self):
        """connecToRedis
            * Builds connection to the existing redis server and throws Execption if no connection can be build

        Raises:
            Exception: Errormessage for any error raised while trying to connect to redis server

        Returns:
            redis.client.Redis: Client that holds connection to your redis server
        
        Test:
            * Test if connectig was succesfull
        """
        try:
            connection = redis.Redis(host=self.redisHost, port=self.redisPort, password=self.redisPw, decode_responses=True)
            connection.ping()
            return connection
        except (redis.exceptions.ConnectionError, ConnectionRefusedError) as connectionError:
            raise Exception(connectionError)      

    def fillRedisDatabase(self):
        """fillRedisDatabase
            * Reads csv File with pandas libary.
            * Iterrates through all rows in the csv file and makes a hashset and stores the data in the connected redis server.

        Raises:
            Exception: Should raise an Exception if the given URL is faulty or invalid.
        """
        # Checking if the given url is working (maybe the site was deleted)
        try:
            df = pd.read_csv(self.url)
        except Exception as urlError:
            raise Exception(urlError)
        df = self.csvPreprocessing(df)
        # Creating RQ Queue
        #TODO
        #queue = Queue(connection=self.redClient)
        for i,row in df.iterrows():
            #queue.enqueue(fillEachDate,args=(row, self.redisHost, self.redisPort, self.redisPw),ttl=120)
            keys = row.keys()
            data = {key: row[key] for key in keys[1:]}
            self.redClient.hset(str(row[0]), mapping=data)

    def csvPreprocessing(self, df):
        """csvPreprocessing
            * Makes some little changes to the read Dataframe.
            * Given Database includes total cases but we need all new cases per day.

        Args:
            df (DataFrame): Includes the read data from the given URL in fillRedisDatabae

        Returns:
            DataFrame: Dataframe that includes the new corona cases per day
        
        Test:
            * Rename succesful?
            * No 0 values in the data and no negativ values?
        """
        # Deleting Time Stamp from date
        df["time_iso8601"] = pd.to_datetime(df["time_iso8601"]).dt.date
        df = df.rename(columns={"time_iso8601":"date"})

        # Given CSV the corona cases are added to the day before
        # We just want the new cases for a day
        for colm in df:
            if colm == "sum_cases":
                df.drop(["sum_cases"], axis=1, inplace=True)
            elif colm == "date":
                continue
            else:
                # To work with every Agorithm no negativ values or zeros can be in the data
                # In the following code i Calculates the diffrence to the value before (diff())
                # Should there be no value the value that was in this row is saved
                # Convertion to integer with numpy at the end
                # Replace all zeros to the value that was given the day before
                # The following if statement set the first entry to 1 if it is 0 so the replacement can be efficient
                if df.loc[0, colm] == 0:
                    df.loc[0, colm] = 1
                df[colm]= df[colm].diff().fillna(df[colm]).apply(np.int64).replace(to_replace=0, method="ffill").clip(lower=1)

        return df

    def getRedisData(self):
        """getRedisData
            * Fetches data from database for the state the user wishes.
            * Builds a Dataframe with the fetched data from the databse to use in further algorithms.
            * Dtypes of the column are given and the rows are sorted by the date.

        Returns:
            DataFrame: Includes data fetched from database to use with further algorithms.
        """
        # Create dataframe and fetch value for wished state from redis
        df = pd.DataFrame(columns=["date", "data"])
        for key in self.redClient.keys():
            value = self.redClient.hget(key, self.state)
            newRow = {"date":key, "data":value}
            df = df.append(newRow, ignore_index=True)

        # Converts the fetched date from Redis to a specific datetime
        df["date"] = pd.to_datetime(df["date"])
        df["data"] = df["data"].astype("int64")

        # Sorting by date
        df.sort_values(by=["date"], inplace=True, ascending=True, ignore_index=True)
        return df

    def getUrl(self):
        """getUrl
            * Returns url to data source

        Returns:
            str: Contains Url to fetched data
        """
        return self.url

    def getClient(self):
        """getClient
            * Returns Client Object. For direct Communication to the redis server.

        Returns:
            Redis Client: Holds the Connection to the redis server.
        """
        return self.redClient

    def flushDB(self):
        """flushDB
            * To delete the whole Database.
            * For Testing reasons.
        """
        self.redClient.flushdb()

#This function should be called by the queue and build the hashset in a job queue
#def fillEachDate(row, redisHost, redisPort, redisPw):
    #connection = redis.Redis(host=redisHost, port=redisPort, password=redisPw, decode_responses=True)
    #keys = row.keys()
    #data = {key: row[key] for key in keys[1:]}
    #connection.hmset(row[0],data)