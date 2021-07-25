#import sys
sys.path.#append("C:\\Users\\toran\\Documents\\Python\\modules")
import graphs #from https://github.com/Blah029/python/blob/main/modules/graphs.py 
import math
import numpy as np
import matplotlib.pyplot as plt

# center frecencies of the preset
bandData1 = np.array([31,62,125,250,500,1000,2000,4000,8000,16000]) #10-band eq
bandData2 = np.array([31,60,150,400,1000,3000,8000,16000])

# gains corresponding to each band of the preset
gainData1 = np.array([6.5,1.8,-9.9,7.5,-13.0,-1.3,1.3,-0.7,-1.7,1.4]) #autoeq ath-ck1 parametric eq gains
gainData2 = np.array([6.5,2,-5.3,-6.4,-1.3,0.1,-1.7,1.4])
gainData3 = np.array([8.6,-1.2,-6.5,-6.1,-4.5,-1.7,5.1,6.9,-0.2,-11.6])

# center frequencies of the required bands
availableBands1 = np.array([60,150,400,1000,3000,8000,16000]) #samsung eq
availableBands2 = np.array([32,64,125,250,500,1000,2000,4000,8000,16000])

# calculated gains for approximation
approxGain1 = np.zeros(len(availableBands1))
approxGain2 = np.zeros(len(availableBands2))
approxGain3 = np.zeros(len(availableBands1))

def getApprox(inBand,inGain,outBand,outGain, outLabel=None, outColour=None, inLabel=None, inColour=None, degree=9, plotInput=True, plotOutput=True):
    print("     Band     Gain")
    
    for i in range(len(outBand)):
        f = np.polyfit(np.log(inBand),inGain,degree)
        xAxis = np.linspace(inBand[0],inBand[-1],inBand[-1]-inBand[0]+1)
        yFitted = np.zeros(len(xAxis))
        
        for k in range(degree+1):
            yFitted += f[-k-1]*np.log(xAxis)**k
            outGain += (f[-k-1]*np.log(outBand)**k)/len(outBand) #why tf does it need to be divided?

    for i in range(len(outBand)):
        print(i,"%5.0f"%outBand[i],"Hz","%5.1f"%outGain[i],"dB") #why does this need a separate for loop?

    if plotInput:
        plt.plot(xAxis,yFitted, label="Model calculated from preset", color=inColour)
        plt.plot(inBand,inGain,label=inLabel, color=inColour, alpha=0.5, linestyle="dashed")
        plt.plot(inBand,inGain,"o", color=inColour)

    if plotOutput:
        plt.plot(outBand,outGain,label=outLabel, color=outColour, alpha=0.5, linestyle="dashed")

    if plotInput:
        plt.plot(inBand,inGain,"o", color=inColour)

    if plotOutput:
        plt.plot(outBand,outGain,"o", color=outColour)

# getApprox(bandData1,gainData1,availableBands1,approxGain1,"7-band approximation","tab:orange","AutoEq preset","tab:blue",9)
# getApprox(bandData2,gainData2,availableBands2,approxGain2,"10-band mimic of 7-band","tab:orange","7-band EQ","tab:blue",7)
getApprox(bandData1,gainData3,availableBands1,approxGain3,"7-band approximation","tab:orange","10-band preset","tab:blue",9)
plt.xscale("log")
graphs.setGrid("Center frequency / Hz","Gain / dB","EQ")
plt.show()
