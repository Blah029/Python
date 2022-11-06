"""Tools for plotting graphs with pyplot"""

"""figure template
# Configure axes
fig, ax = plt.subplots(_int_)
ax.set_xscale(_string_)
ax.set_yscale(_string_)
ax.set_xlim(_int_,_int_)
ax.set_ylim(_int_,_int_)
# Plot. Replace plt with ax[_int_] for subplots.
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
import numpy as np
import matplotlib.pyplot as plt


def setGrid(xLabel=None, yLabel=None, title=None):
    """Configure axis labels, title and other roperties"""
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
        plt.text(i, j+1,("({:.0f},{:.0f})".format(i,j)),
                 backgroundcolor="white", alpha=0.5)


def plotPoints(x,y, colour=None, size=None):
    """Mark points on the graph"""
    plt.plot(x,y,".", color=colour, markersize=size)


def plotBestFitPoly(x,y, degree=1, plotLabel=None, plotColour="tab:blue"):
    """Plot the best fiting polynomial curve of given degree to fit 
    given numpy arrays"""
    coefficients = np.polyfit(x,y,degree)
    xAxis = np.linspace(x[0],x[-1],(x[-1]-x[0]+1)*100)
    yFitted = np.zeros(len(xAxis))    
    for i in range(degree+1):
        yFitted += coefficients[-i-1]*xAxis**i

    plt.plot(xAxis,yFitted, label=plotLabel, color=plotColour)
    plt.plot(x,y,"o", color=plotColour)


def plotBestFitLog(x,y, plotLabel=None, plotColour="tab:blue"):
    """Plot the best fiting polynomial curve of given degree to fit 
    given numpy arrays"""
    coefficients = np.polyfit(np.log(x),y,1)
    xAxis = np.linspace(x[0],x[-1],(x[-1]-x[0]+1)*100)
    yFitted = coefficients[0]*np.log(xAxis) + coefficients[1]

    plt.plot(xAxis,yFitted, label=plotLabel, color=plotColour)
    plt.plot(x,y,"o", color=plotColour)