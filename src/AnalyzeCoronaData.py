"""AnalyzeCoronaData
    * Analyzes corona data with redis as a database.
    * Fetches data from redis database and computes it.
"""
import pandas as pd
import matplotlib.pyplot as plt
import operator

class AnalyzeCorona():
    """AnalyzeCorona
        * Contains all functions to analyze corona data fetched from redis database.
    """
    def __init__(self, redisDB):
        """Inits the analyze objekt with the redisClient Object.
            * With the help of the redisClient object we can get the connection to redis.
            * Two parameters are set to store the highest and lowest incident value (in the last 30 days)

        Args:
            redisDB (RedisClient): RedisClient object containing every important attribute, method for our redis database
        """
        self.redisDB = redisDB.getClient()
        self.highest = (0,0)
        self.lowest = (99999,99999)
    
    def coronaPeaksIncident(self):
        """coronaPeaksIncident
            * Gets keys from redis database and converts them to datetime to sort them and get the latest entries.
            * The highest and lowest value will be searched in the latest entries.
        """
        # Get all keys from redis db->convert them to datetime and sort the pandas Serie
        # Important! Use of keys is not recommand in normal use cases because there can be a lot more keys then in this example
        keys = pd.to_datetime(pd.Series(self.redisDB.keys())).sort_values(ignore_index=True)
        # Slicing the last 30 entries and removing the timestamp
        keys = keys.tail(30).dt.date

        for key in keys:
            # Get hashmap for key, redis just accepts str
            hashSet = self.redisDB.hgetall(str(key))
            # Search for the key with the highest value in the return dict
            highestKey = max(hashSet.items(), key=operator.itemgetter(1))[0]
            if int(hashSet[highestKey]) >= self.highest[1]:
                self.highest = (highestKey, int(hashSet[highestKey]))
            # Search for the smallest key
            lowestKey = min(hashSet.items(), key=operator.itemgetter(1))[0]
            if int(hashSet[lowestKey]) <= self.lowest[1]:
                self.lowest = (lowestKey, int(hashSet[lowestKey]))

    def averageCoronaIncident(self):
        """averageCoronaIncident
            * Iterates trough all keys and hmset in redis database and calculates the average incident for the recorded time
        """
        # Dict for all german states
        states = {"DE-BB" : 0, "DE-BE":0, "DE-BW":0, "DE-BY":0, "DE-HB":0,
                    "DE-HE":0, "DE-HH":0, "DE-MV":0, "DE-NI":0,
                    "DE-NW":0, "DE-RP":0, "DE-SH":0, "DE-SL":0, "DE-SN":0, "DE-ST":0, "DE-TH":0}
        
        redisKeys = self.redisDB.keys()
        for key in redisKeys:
            hashSet = self.redisDB.hgetall(key)
            for key, value in hashSet.items():
                # redis return str->cast to int is necassery
                states[key] += int(value)
        
        #for key in states:
            #print(f"The average icident of {key} is {round(states[key]/len(redisKeys),2)} measured with {len(redisKeys)} days")

        # calculating average incident and storing in list to plot
        yValues = [ value/len(redisKeys) for value in states.values()]

        highestCorona = f"Highest incident recorded in {self.highest[0]} : {self.highest[1]} new cases (last 30days)\n"
        lowestCorona = f"Lowest incident recorded in {self.lowest[0]} : {self.lowest[1]} new cases (last 30days)"
        textToPrint = highestCorona + lowestCorona
        
        # Plots result
        plt.bar(states.keys(), yValues, zorder=3)
        plt.title("Average incident cases in Germany")
        plt.xlabel("German states")
        plt.xticks(rotation=-45)
        plt.ylabel("Average incidents per day")
        # calc highest average incident and addind buffer for text box
        yMax = states.get(max(states, key=states.get))/len(redisKeys) + 400
        plt.ylim((0,yMax))
        plt.grid(True)
        plt.get_current_fig_manager().canvas.set_window_title("Analyze corona data with redis")
        plt.rc("font", size=9)
        plt.text(0, yMax-220, textToPrint,style="italic", bbox={"facecolor": 'red', "alpha": 0.5, "pad": 10})
        plt.show()
