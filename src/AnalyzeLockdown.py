import pandas as pd

class Lockdown():
    def __init__(self, redisDB, _lockdown, _hardLockdown):
        self.lockdown = _lockdown
        self.hardLockdown = _hardLockdown
        self.redisData = redisDB.getRedisData()
    
    def lockdownPhases(self):
        phaseOneLD = self.redisData[(self.redisData["data"] > self.lockdown)]
        phsaeTwoLD = self.redisData[(self.redisData["data"] > self.hardLockdown)]
        phaseOneLD.reset_index(drop=True)
        phsaeTwoLD.reset_index(drop=True)
        self.printLockdownPhases(phaseOneLD,phsaeTwoLD)

    def printLockdownPhases(self, phOne, phTwo):
        print(f"Since "+ phOne["date"] +"is an easy Lockdown active")