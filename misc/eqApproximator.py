# import sys
# sys.path.append("C:\\Users\\toran\\Documents\\Python\\modules")
import graphs #from https://github.com/Blah029/python/blob/main/modules/graphs.py 
import math
import numpy as np
import matplotlib.pyplot as plt

# center frecencies of the preset
bandData1 = np.array([31,62,125,250,500,1000,2000,4000,8000,16000]) #10-band eq
# bandData2 = np.array([31,60,150,400,1000,3000,8000,16000])

# gains corresponding to each band of the preset
gainData1 = np.array([6.5,1.8,-9.9,7.5,-13.0,-1.3,1.3,-0.7,-1.7,1.4]) #autoeq ath-ck1 parametric eq gains
# gainData2 = np.array([6.5,2,-5.3,-6.4,-1.3,0.1,-1.7,1.4])

# center frequencies of the required bands
availableBands1 = np.array([60,150,400,1000,3000,8000,16000]) #samsung eq
# availableBands2 = np.array([32,64,125,250,500,1000,2000,4000,8000,16000])

# calculated gains for approximation
approxGain1 = np.zeros(len(availableBands1))
# approxGain2 = np.zeros(len(availableBands2))

def getApprox(inBand,inGain,outBand,outGain, outLabel=None, outColour=None, inLabel=None, inColour=None, plotInput=True, plotOutput=True):
    print("     Band     Gain")
    
    for i in range(len(outBand)):

        for j in range(len(inBand)):

            if (inBand[j] == outBand[i]):
                outGain[i] = inGain[j]
                print(i,j,"%5.0f"%outBand[i],"Hz","%5.1f"%outGain[i],"dB")
                break
            
            elif (inBand[j] > outBand[i]):
                m,c = np.polyfit(np.array([math.log(inBand[j-1]),math.log(inBand[j])]),np.array([inGain[j-1],inGain[j]]),1)
                outGain[i] = m*math.log(outBand[i]) + c
                print(i,j,"%5.0f"%outBand[i],"Hz","%5.1f"%outGain[i],"dB")
                break
            
    if plotInput:
        plt.plot(inBand,inGain,label=inLabel, color=inColour)
        plt.plot(inBand,inGain,"o", color=inColour)

    if plotOutput:
        plt.plot(outBand,outGain,label=outLabel, color=outColour)
        plt.plot(outBand,outGain,"o", color=outColour)

getApprox(bandData1,gainData1,availableBands1,approxGain1,"7-band approximation","tab:orange","AutoEq preset","tab:blue")
# getApprox(bandData2,gainData2,availableBands2,approxGain2,"10-band mimic of 7-band","tab:green", plotInput=0, plotOutput=0)
# adjustedGains = approxGain2.copy()
# adjustedGains[2] = -4.5
# adjustedGains[3] = -6.2
# adjustedGains[4] = -5.7
# adjustedGains[6] = -0.2
# adjustedGains[7] = -0.2
# plt.plot(availableBands2,adjustedGains, label="Adjusted mimic", color="tab:purple")
# plt.plot(availableBands2,adjustedGains,"o", color="tab:purple")
plt.xscale("log")
graphs.setGrid("Center frequency / Hz","Gain / dB","EQ")
plt.show()
