"""Tools for plotting graphs with pyplot"""

"""figure template
# WIth subplots
fig, ax = plt.subplots(_int_)
ax.set_xscale(_string_)
ax.set_yscale(_string_)
ax.set_xlim(_int_,_int_)
ax.set_ylim(_int_,_int_)
# Without subplots
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


def plotPoints(x,y, colour=None, size=None, label=None, axis=None):
    """Plot scatter graph"""
    if axis == None:
        plt.plot(x,y,".", color=colour, markersize=size, label=label)
    else:
        axis.plot(x,y,".", color=colour, markersize=size, label=label)



def plotLine(x,y, colour=None, label=None, axis=None):
    """Plot line graph"""
    if axis == None:
        plt.plot(x,y,"-", color=colour, label=label)
    else:
        axis.plot(x,y,"-", color=colour, label=label)


def plotBestFitPoly(x,y, degree=1, label=None, plotColour="tab:blue"):
    """Plot the best fiting polynomial curve of given degree to fit 
    given numpy arrays"""
    coefficients = np.polyfit(x,y,degree)
    xAxis = np.linspace(x[0],x[-1],int((x[-1]-x[0]+1)*100))
    yFitted = np.zeros(len(xAxis))    
    for i in range(degree+1):
        yFitted += coefficients[-i-1]*xAxis**i

    plt.plot(xAxis,yFitted, label=label, color=plotColour)
    plt.plot(x,y,"o", color=plotColour)


def plotBestFitLog(x,y, label=None, plotColour="tab:blue"):
    """Plot the best fiting loarithmic curve to fit 
    given numpy arrays"""
    coefficients = np.polyfit(np.log(x),y,1)
    xAxis = np.linspace(x[0],x[-1],(x[-1]-x[0]+1)*100)
    yFitted = coefficients[0]*np.log(xAxis) + coefficients[1]

    plt.plot(xAxis,yFitted, label=label, color=plotColour)
    plt.plot(x,y,"o", color=plotColour)


def pointLabels(x,y, xOffset=None, yOffset=None):
    """Plot data points"""
    if yOffset == None:
        yOffset = xOffset
    for i, j in zip(x,y):
        plt.text(i+xOffset, j+yOffset,("({:.0f},{:.0f})".format(i,j)),
                 backgroundcolor="white", alpha=0.5)


def setGrid(xLabel=None, yLabel=None, title=None, xscale=None, yscale=None):
    """Configure axis labels, title and other properties"""
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    if xscale != None:
        plt.xscale(xscale)
    if yscale != None:
        plt.yscale(yscale)
    plt.legend()
    plt.grid()
    plt.grid(which="minor", alpha=0.25)
    plt.minorticks_on()


def setSubGrid(axis=None, xLabel=None, yLable=None, xscale=None, 
               yscale=None, title=None):
    """Configure axis labels, title and other properties of a subplot"""
    axis.set_xlabel(xLabel)
    axis.set_ylabel(yLable)
    if axis.get_title() == "":
        axis.set_title(title)
    if xscale != None:
        axis.set_xscale(xscale)
    if yscale != None:
        axis.set_yscale(yscale)
    axis.legend()
    axis.grid()
    axis.grid(which="minor",alpha=0.25)
    axis.minorticks_on()
    

def testPlot():
    """testing graphs.py"""
    fs = 5
    t = np.linspace(0,1,fs*5+1)
    x_t = np.cos(2*np.pi*1*t)

    plotPoints(t,x_t,"red",10,"plotPoints")
    plotLine(t,x_t,"green","plotLine")
    plotBestFitPoly(t,x_t,4,"plotBestFitPoly","black")
    plotBestFitLog(np.array([1,2,3]),np.array([1,1.1,1.11]),
                          "plotBestFitLog","yellow")
    pointLabels(t,x_t,0.025,0)
    setGrid("time","magnitude","test plot","log","log")
    plt.show()


def testSubplot():
    # Section 1 - Multplier Modulator/Demodulator
    # 1. Generate m(t)
    fm = 15000
    fc = 250000
    fs = 750000*10
    duration = 1/fm*4
    t = np.linspace(0,duration,int(fs*duration+1))
    m_t = 0.5*np.cos(2*np.pi*fm*t)
    # 2. Multiply with carrier
    # c_t = np.cos(2*np.pi*fc*t)
    c_t = np.cos(2*np.pi*fc*t)
    x_t = m_t*c_t

    # Frequency domain
    fig, ax = plt.subplots(4)
    ax[0].magnitude_spectrum(m_t, Fs=fs, label="m(t)")
    ax[0].set_title("Modulator Output Frequency Spectrum")
    ax[1].magnitude_spectrum(c_t, Fs=fs, label="c(t)")
    plotLine(t,m_t, axis=ax[2])
    plotPoints(t,m_t, axis=ax[3])
    for axis in ax:
        setSubGrid(axis,"f /kHz","Magnitude","log", title="Common Title")
        axis.set_xticks([1e4,1e5,1e6])
        axis.set_xticklabels([10,100,100])
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    testPlot()
    testSubplot()