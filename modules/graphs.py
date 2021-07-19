import numpy as np
import matplotlib.pyplot as plt

"""
figure template

plt.figure(_int_)
plt.plot(_array_,_array_, label=_string_, color=_string_)
plt.xlabel(_string_)
plt.ylabel(_string_)
plt.title(_string_)
plt.legend()
plt.grid()
plt.grid(which="minor", alpha=0.25))
"""

def plotBestFit(x,y, degree=1, plotLabel=None, plotColour="tab:blue"):
    """Plots the best fit curve of given degree to fit the given data"""
    m,b = np.polyfit(x,y,degree)
    plt.plot(x,y,"o", color=plotColour)
    plt.plot(x,m*x+b, label=plotLabel, color=plotColour)
