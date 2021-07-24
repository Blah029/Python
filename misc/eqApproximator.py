import graphs #from https://github.com/Blah029/python/blob/main/modules/graphs.py 
import math
import numpy as np
import matplotlib.pyplot as plt

# center frecencies of the 10-band preset
bandData = np.array([31,62,125,250,500,1000,2000,4000,8000,16000])
# gain corresponding to each band of the preset
gainData = np.array([6.5,1.8,-9.9,7.5,-13.0,-1.3,1.3,-0.7,-1.7,1.4])
# center frequencies of the band available on the new EQ
availableBands = np.array([60,150,400,1000,3000,8000,16000])
approxGain = np.zeros(len(availableBands))
print(" Band     Gain")

for i in range(len(availableBands)):

    for j in range(len(bandData)):

        if (bandData[j] == availableBands[i]):
            approxGain[i] = gainData[j]
            print("%5.0f"%availableBands[i],"Hz","%5.0f"%approxGain[i],"dB")
            break
        
        elif (bandData[j] > availableBands[i]):
            m,c = np.polyfit(np.array([math.log(bandData[j-1]),math.log(bandData[j])]),np.array([gainData[j-1],gainData[j]]),1)
            approxGain[i] = m*math.log(availableBands[i]) + c
            print("%5.0f"%availableBands[i],"Hz","%5.0f"%approxGain[i],"dB")
            break

plt.plot(bandData,gainData,label="{}-band preset".format(len(bandData)), color="tab:blue")
plt.plot(bandData,gainData,"o", color="tab:blue")
plt.plot(availableBands,approxGain, label="{}-band approximation".format(len(availableBands)), color="tab:orange")
plt.plot(availableBands,approxGain,"o", color="tab:orange")
plt.xscale("log")
graphs.setGrid("Center frequency","Gain","EQ")
plt.show()
