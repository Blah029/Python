import sys
sys.path.append("D:\\User Files\\Documents\\Python\\_modules")
import graphs #from https://github.com/Blah029/python/blob/main/modules/graphs.py 
import numpy as np
import matplotlib.pyplot as plt

# center frecencies of the preset
bandData1 = np.array([31,62,125,250,500,1000,2000,4000,8000,16000]) #autoeq 10-band
bandData2 = np.array([31,60,150,400,1000,3000,8000,16000]) #samsing 7-band + 31hz
bandData3 = np.array([32,64,125,250,500,1000,2000,4000,8000,16000]) #hp 10-band

# center frequencies of the required bands
availableBands1 = np.array([60,150,400,1000,3000,8000,16000]) #samsung 7-band
availableBands2 = np.array([32,64,125,250,500,1000,2000,4000,8000,16000]) #hp 10-band

# gains corresponding to each band of the preset
gainData1 = np.array([6.5,1.8,-9.9,7.5,-13.0,-1.3,1.3,-0.7,-1.7,1.4]) #autoeq ath-ck1 parametric eq gains
gainData2 = np.array([6.5,2,-5.3,-6.4,-1.3,0.1,-1.7,1.4]) #autoeq ath-ck1 parametric eq gains converted to samsung 7-band
gainData3 = np.array([7.4,2.9,-3.7,-3.2,-1.7,0.6,1.6,2.3,-2.0,7.2]) #autoeg beoplay a1 10-band
gainData4 = np.array([6.6,-6.7,-6.1,-4.2,-1.9,3.0,-0.6,4.4,6.1,4.8]) #autoeq sony mdr zx110 10-band

# calculated gains
approxGain1 = np.zeros(len(availableBands1))
approxGain2 = np.zeros(len(availableBands2))
approxGain3 = np.zeros(len(availableBands1))
approxGain4 = np.zeros(len(availableBands1))

def getApprox(inBand,outBand,inGain,outGain, inLabel=None, outLabel=None, degree=9, inColour="tab:blue", outColour="tab:orange", plotInput=True, plotOutput=True):
    print("   Band     Gain")
    
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
        plt.plot(xAxis,yFitted, label="Calculated model", color=inColour)
        plt.plot(inBand,inGain,label=inLabel, color=inColour, alpha=0.5, linestyle="dashed")
        plt.plot(inBand,inGain,"o", color=inColour)

    if plotOutput:
        plt.plot(outBand,outGain,label=outLabel, color=outColour, alpha=0.5, linestyle="dashed")

    if plotInput:
        plt.plot(inBand,inGain,"o", color=inColour)

    if plotOutput:
        plt.plot(outBand,outGain,"o", color=outColour)

# getApprox(bandData3,availableBands1,gainData1,approxGain1,"AutoEq 10-band preset","7-band approximation",9)
# getApprox(bandData2,availableBands2,gainData2,approxGain2,"7-band phone EQ","10-band mimic",7)
# getApprox(bandData1,availableBands1,gainData3,approxGain3,"AutoEq 10-band preset","7-band approximation",9)
getApprox(bandData1,availableBands1,gainData4,approxGain4,"AutoEq 10-band preset","7-band approximation",9)
plt.xscale("log")
graphs.setGrid("Frequency band / Hz","Gain / dB","EQ")
plt.show()