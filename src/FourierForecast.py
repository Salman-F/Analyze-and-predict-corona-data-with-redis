"""FourierForecast
    Fourier Transforamtion to forecast corona cases.
    
    Attributes:
        * name: SALFIC
        * date: 24.04.2021
        * version: 0.0.1 Beta- free

Example:
    None

TODO:
    * 
"""
from AbstractForecast import *
import numpy as np
from scipy.fftpack import fft, fftfreq, ifft

class FourierForecast(AbstractForecast):
    """FourierForecast
        The FourierForecast predicts future corona values with the implemented fft.
        The given values are analyzed for any characteristics that decsribe the progress of the corona cases.
    """
    def getForecast(self):
        """getFFtForecast
            Executes the FFT Algortihm and prepares data for fft algorithm

        Returns: //////TODO
            [type]: [description]
        """
        lenOfData = len(self.redisData.index)
        npArray = np.empty(shape=(1,lenOfData), dtype=int)
        for i in range (lenOfData):
            npArray[0][i] = self.redisData["data"][i]
        self.extendOrgData(npArray[0])
        futureData = self.fftExtrapolation(npArray[0], self.future)
        self.result = futureData

    def fftExtrapolation(self, x, n_predict):
        """fftExtrapolation
            Analyses the given Data for frequency, harmonics, amplitude, phase etc.
            Creates a function that represents the progress of the corona cases most likely

        Source:
            * https://gist.github.com/tartakynov/83f3cd8f44208a1856ce (Some adjustments needed to be made)

        Args:
            x (numpyArray): Includes all new corona cases per day
            n_predict (int): Describes the number of days the Function should forecast

        Returns://///TODO
            [type]: [description]
        """
        n = x.size
        n_harm = 10                     # number of harmonics in model
        t = np.arange(0, n)
        p = np.polyfit(t, x, 1)         # find linear trend in x
        x_notrend = x - p[0] * t        # detrended x
        x_freqdom = fft(x_notrend)  # detrended x in frequency domain
        f = fftfreq(n)              # frequencies
        indexes = range(n)
        # sort indexes by frequency, lower -> higher
        indexes = list(range(n))
    
        t = np.arange(0, n + n_predict)
        restored_sig = np.zeros(t.size)
        for i in indexes[:1 + n_harm * 2]:
            ampli = np.absolute(x_freqdom[i]) / n   # amplitude
            phase = np.angle(x_freqdom[i])          # phase
            restored_sig += ampli * np.cos(2 * np.pi * f[i] * t + phase)
        return restored_sig + p[0] * t
