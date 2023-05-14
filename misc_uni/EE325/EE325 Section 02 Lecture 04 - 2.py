import numpy as np
import matplotlib.pyplot as plt

N = 8
n = np.transpose(np.linspace(0, N-1, 8)) # actually a column matrix
x = 10*np.cos(2*np.pi/N*n) + 4*np.cos(2*np.pi*3*n/N + np.pi/4)

# plt.stem(n,x)
# plt.show()

W = np.empty((8,8), dtype=complex)

for  k in range(N):
    w = np.transpose(np.exp(-1j*2*np.pi*k*n/N))
    W[k] = w

W.transpose()
print("W", W, "", sep="\n")

# W' X x matrix
C = np.matmul(np.transpose(W),x)/N
print("C", C, "", sep="\n")
print("absolute", np.abs(C), "", sep="\n")
print("angle", np.angle(C), "", sep="\n")

# fig, ax = plt.subplots(2)
# ax[0].stem(n, np.abs(C))
# ax[1].stem(n, np.angle(C))
# plt.show()