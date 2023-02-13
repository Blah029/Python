import numpy as np
import matplotlib.pyplot as plt

f0 = 50
T = 1/f0
w0 = 2*np.pi*f0
ts = T/100
t = np.linspace(0,T-ts,int(T/ts))

x1 = 100*np.cos(w0*t + 0.2)
x2 = 60*np.cos(2*w0*t + 0.4)
x3 = x1 + x2

plt.plot(t,x1)
plt.plot(t,x2)
plt.plot(t,x3)
plt.show()

# h = 1
z1 = 2/T*sum(np.multiply(x3,np.exp(-1j*1*w0*t)))*ts
# h = 2
z2 = 2/T*sum(np.multiply(x3,np.exp(-1j*2*w0*t)))*ts
print(np.abs(z1), np.angle(z1))
print(np.abs(z2), np.angle(z2))