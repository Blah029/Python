import numpy as np
import matplotlib.pyplot as plt
import math

speed = [[]]*4
torque = [[]]*4
m = np.zeros(4)
b = np.zeros(4)
speedBestFit = np.zeros(3)
plotLabel = ["Vt = 200V, If = 0.22A","Vt = 210V, If = 0.22A","Vt = 210V, If = 0.20A","Vt = 210V, If = 0.18A"]
plotColour = ["tab:blue","tab:orange","tab:green","tab:red"]

# electromagnetic toruqe
speed[0] = np.array([1243.8,1235.8,1218.2])
torque[0] = np.array([1.163,1.239,1.464])

speed[1] = np.array([1309.0,1305.5,1297.4])
torque[1] = np.array([1.163,1.304,1.448])

speed[2] = np.array([1359.9,1357.1,1350.3])
torque[2] = np.array([1.186,1.280,1.391])

speed[3] = np.array([1417.9,1414.5,1411.0])
torque[3] = np.array([1.200,1.266,1.331])

plt.figure(1)

for i in range(4):
    m[i],b[i] = np.polyfit(speed[i],torque[i],1)
    speedBestFit[0] = (torque[i][0]-b[i])/m[i]
    speedBestFit[1] = speed[i][1]
    speedBestFit[2] = (torque[i][2]-b[i])/m[i]
    plt.plot(speed[i],torque[i],"o", color=plotColour[i])
    plt.plot(speedBestFit,m[i]*speedBestFit+b[i], label=plotLabel[i], color=plotColour[i])

plt.xlabel("Speed/rpm")
plt.ylabel("Torque/Nm")
plt.title("Angular Velocity vs. Electromagnetic Torque")
plt.legend()
plt.grid()
plt.grid(which="minor",alpha=0.25)
plt.minorticks_on()


# shaft torque
speed[0] = np.array([1243.8,1235.8,1218.2])
torque[0] = np.array([0.509,0.597,0.836])

speed[1] = np.array([1309.0,1305.5,1297.4])
torque[1] = np.array([0.450,0.595,0.748])

speed[2] = np.array([1359.9,1357.1,1350.3])
torque[2] = np.array([0.424,0.521,0.639])

speed[3] = np.array([1417.9,1414.5,1411.0])
torque[3] = np.array([0.376,0.445,0.515])

plt.figure(2)

for i in range(4):
    m[i],b[i] = np.polyfit(speed[i],torque[i],1)
    plt.plot(speed[i],torque[i],"o", color=plotColour[i])
    speed[i][0] = (torque[i][0]-b[i])/m[i]
    speed[i][1] = speed[i][1]
    speed[i][2] = (torque[i][2]-b[i])/m[i]
    plt.plot(speed[i],m[i]*speed[i]+b[i], label=plotLabel[i], color=plotColour[i])

plt.xlabel("Speed/rpm")
plt.ylabel("Torque/Nm")
plt.title("Angular Velocity vs. Shaft Torque")
plt.legend()
plt.grid()
plt.grid(which="minor",alpha=0.25)
plt.minorticks_on()

# render figures
plt.show()