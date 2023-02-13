import numpy as np
import matplotlib.pyplot as plt

N = 8
n = np.transpose(np.linspace(0, N-1, 8)) # actually a colum matrix
x = 10*np.cos(2*np.pi/N*n) + 4*np.cos(2*np.pi*3*n/N + np.pi/4)

# plt.stem(n,x)
# plt.show()

# w' X x is nearly 0
k = 0
w = np.exp(-1j*2*np.pi/N*k*n)
print("k = 0", np.matmul(w,np.transpose(x)))

# amplitude is 10. w' X x is 5 for k = 1 and k = -1
k = 1
w = np.exp(-1j*2*np.pi/N*k*n)
print("k = 1", np.matmul(w,np.transpose(x))/N)

# w' X x is nearly 0
k = 2
w = np.exp(-1j*2*np.pi/N*k*n)
print("k = 2", np.matmul(w,np.transpose(x))/N)

# absolute of w' X x is 2
k = 3
w = np.exp(-1j*2*np.pi/N*k*n)
print("k = 3", np.matmul(np.transpose(w),x)/N)
print("abs(ck)", np.abs(np.matmul(np.transpose(w),x)/N))
