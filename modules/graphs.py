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
plt.minorticks_on()
plt.show()
"""

def setGrid(xLabel=None, yLabel=None, title=None):
    """Configures axis labels, title and other roperties"""
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.grid(which="minor", alpha=0.25)
    plt.minorticks_on()

def pointLabels(x,y):
    """Plot data points"""

    for i, j in zip(x, y):
        plt.text(i, j+1,("({:.0f},{:.0f})".format(i,j)), backgroundcolor="white", alpha=0.5)

def plotPoints(x,y, plotColour=None):
    plt.plot(x,y,"o", color=plotColour)

def plotBestFit(x,y, degree=1, plotLabel=None, plotColour="tab:blue"):
    """Plots the best fit curve of given degree to fit given numpy arrays"""
    
    for i in range(len(x)):
        f = np.polyfit(x,y,degree)
        xAxis = np.linspace(x[0],x[-1],(x[-1]-x[0]+1)*100)
        yFitted = np.zeros(len(xAxis))
        
        for k in range(degree+1):
            yFitted += f[-k-1]*xAxis**k

    plt.plot(xAxis,yFitted, label=plotLabel, color=plotColour)
    plt.plot(x,y,"o", color=plotColour)
