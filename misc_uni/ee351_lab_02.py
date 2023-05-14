import sys
sys.path.append("D:\\User Files\\Documents\\Python\\_modules")
import numpy as np
import matplotlib.pyplot as plt
import graphs

frequencyLog = np.log10(np.array([1,5,10,15,20,25,30,35,40,45,50,55,60])*1000)
peakVoltage = np.array([5,5.2,1.4,0.6,0.3,0.2,0.1,0.1,0.1,0.1,0.0,0.0,0.0])
timeShift = np.array([55,50,42,30,23,19,16,14,12,11,10,10,9])
gain = np.array([1,1.04,0.28,0.12,0.06,0.04,0.02,0.02,0.02,0.02,0,0,0])
phase = np.array([-0.346,-1.571,-2.639,-2.827,-2.890,-2.985,-3.016,-3.079,-3.016,-3.110,-3.142,-3.456,-3.393])

plt.figure(4)
# graphs.plotBestFitPoly(frequency,gain,3)
# graphs.plotBestFitLog(frequency,gain)
graphs.plotPoints(frequencyLog,gain)
plt.xlabel("log(f)")
plt.ylabel("Gain / dB")
plt.title("Frequency vs. Gain")
plt.grid()
plt.grid(which="minor", alpha=0.25)
plt.minorticks_on()

plt.figure(5)
# graphs.plotBestFitPoly(frequency,phase,3)
graphs.plotPoints(frequencyLog,phase)
plt.xlabel("log(f)")
plt.ylabel("Phase / rad")
plt.title("Frequency vs. Phase")
plt.grid()
plt.grid(which="minor", alpha=0.25)
plt.minorticks_on()

plt.show()
