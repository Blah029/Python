import numpy as np
import matplotlib.pyplot as plt

def plotBestFit(x,y,degree=1,plotLabel=None, plotColour="tab:blue"):
    """Plots the best fit curve of given degree to fit the given data"""
    m,b = np.polyfit(x,y,degree)
    plt.plot(x,y,"o", color=plotColour)
    plt.plot(x,m*x+b, label=plotLabel, color=plotColour)
