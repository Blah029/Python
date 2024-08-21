import numpy as np
import matplotlib.pyplot as plt

vm = 100
phi = 0.2
f0 = 50

T = 1/f0
w0 = 2*np.pi*f0
ts = T/100
t = np.linspace(0,T-ts,int(T/ts))

# without noise
# x = vm*np.cos(w0*t + phi)

# with noise
x = vm*np.cos(w0*t + phi) + 100*np.random.random(np.size(t))

z = 2/T*ts*np.sum(np.multiply(x,np.exp(-1j*w0*t)))
print(np.abs(z))
print(np.angle(z))

plt.plot(t,x)
plt.show()