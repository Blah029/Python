import cmath
import math

import numpy as np

#data
y12 = 0
y13 = 6.6627-34.1615j
y23 = 16.0256-80.1282j
#inital values
V = np.array([[1],
              [1.04],
              [1.02]])
D = np.zeros((3,1))
P = np.array([[3.6],
              [0],
              [2]])
Q = np.array([[1.1833],
              [0],
              [0]])
N = np.shape(V)[0]


def vComp(index):
    return cmath.rect(V[index,0],D[index,0])
    

#admittance matrix
print("--------Y")
Y = np.array([[y12+y13, -y12,    -y13],
              [-y12,    y12+y23, -y23],
              [-y13,    -y23,    y13+y23]]);
print(Y)
print(np.abs(Y))
print(np.angle(Y)/math.pi*180)

#gauss-siedel
#active power of bus 3, Q[2,0]
print("--------Q")
for i in [2]:
    for j in range(N):
        print('\t',V[i,0],np.abs(Y[i,j]),V[j,0],'\t',D[i,0],-D[j,0],-np.angle(Y[i,j])/math.pi*180)
        print('\t',np.abs(V[i,0]*Y[i,j]*V[j,0]),math.sin(D[i,0]-D[j,0]-np.angle(Y[i,j])))
        Q[i,0] += np.abs(V[i,0]*Y[i,j]*V[j,0]) * math.sin(D[i,0]-D[j,0]-np.angle(Y[i,j]))
# Q[2,0] = -0.667
print(Q,'\n')

#voltave of bus 1, V[0,0] and 3, V[2,0]
print("--------V1,D1")
for i in [0]:
    yv = 0
    for j in range(N):
        if i != j:
            yv += Y[i,j]*V[j]
    print('\t',Y[i,i],-P[i,0]+1j*Q[i,0],np.conj(vComp(i)),yv)
    vv = 1/Y[i,i] * ((-P[i,0]+1j*Q[i,0])/np.conj(vComp(i)) - yv)
    V[i,0] = np.abs(vv)
    D[i,0] = np.angle(vv)
print("--------V3,D3")
for i in [2]:
    yv = 0
    for j in range(N):
        if i != j:
            yv += Y[i,j]*V[j]
    print('\t',Y[i,i],P[i,0]-1j*Q[i,0],np.conj(vComp(i)),yv)
    vv = 1/Y[i,i] * ((P[i,0]-1j*Q[i,0])/np.conj(vComp(i)) - yv)
    V[i,0] = np.abs(vv)
    D[i,0] = np.angle(vv)
for vv,dd in np.column_stack((V,D)):
    print(cmath.rect(vv,dd))
print(V)
print(D/math.pi*180,'\n')
