import sys
sys.path.append("C:\\Users\\toran\\Documents\\Python\\modules")
import graphs #from https://github.com/Blah029/python/blob/main/modules/graphs.py 
import math
import numpy as np
import matplotlib.pyplot as plt

# center frecencies of the preset
bandData1 = np.array([31,62,125,250,500,1000,2000,4000,8000,16000]) #10-band eq

# gains corresponding to each band of the preset
gainData1 = np.array([6.5,1.8,-9.9,7.5,-13.0,-1.3,1.3,-0.7,-1.7,1.4]) #autoeq ath-ck1 parametric eq gains

# center frequencies of the required bands
availableBands1 = np.array([60,150,400,1000,3000,8000,16000]) #samsung eq

# calculated gains for approximation
approxGain1 = np.zeros(len(availableBands1))

def getApprox(inBand,inGain,outBand,outGain, inLabel=None, inColour=None, outLabel=None, outColour=None):
    print(" Band     Gain")
    
    for i in range(len(outBand)):

        for j in range(len(inBand)):

            if (inBand[j] == outBand[i]):
                outGain[i] = inGain[j]
                print("%5.0f"%outBand[i],"Hz","%5.1f"%outGain[i],"dB")
                break
            
            elif (inBand[j] > outBand[i]):
                m,c = np.polyfit(np.array([math.log(inBand[j-1]),math.log(inBand[j])]),np.array([inGain[j-1],inGain[j]]),1)
                outGain[i] = m*math.log(outBand[i]) + c
                print("%5.0f"%outBand[i],"Hz","%5.1f"%outGain[i],"dB")
                break

    plt.plot(inBand,inGain,label=inLabel, color=inColour)
    plt.plot(inBand,inGain,"o", color=inColour)
    plt.plot(outBand,outGain,label=outLabel, color=outColour)
    plt.plot(outBand,outGain,"o", color=outColour)

getApprox(bandData1,gainData1,availableBands1,approxGain1,"AutoEq preset","tab:blue","7-band approximation","tab:orange")
plt.xscale("log")
graphs.setGrid("Center frequency / Hz","Gain / dB","EQ")
plt.show()
