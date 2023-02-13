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

#newton-raphson
#jacobian matrix
PD = np.zeros((3,3))
PV = np.zeros((3,3))
QD = np.zeros((3,3))
QV = np.zeros((3,3))
print("--------PD")
for i in [0,2]:
    for j in range(N):
        pd = -V[i,0]*V[j,0]*np.abs(Y[i,j]) * math.sin(D[i,0]-D[j,0]-np.angle(Y[i,j]))
        # print('\t',i+1,j+1,' ',pd)
        PD[i,i] += pd
for i in [0,2]:
    for j in [0,2]:
        if i != j:
            pd = V[i,0]*V[j,0]*np.abs(Y[i,j]) * math.sin(D[i,0]-D[j,0]-np.angle(Y[i,j]))
            PD[i,j] = pd
PD = np.row_stack((PD[0],PD[2]))
PD = np.transpose(PD)
PD = np.row_stack((PD[0],PD[2]))
PD = np.transpose(PD)
print(PD)
print("--------PV")
for i in [0,2]:
    for j in range(N):
        if i != j:
            pv = V[j,0]*np.abs(Y[i,j]) * math.cos(D[i,0]-D[j,0]-np.angle(Y[i,j]))
            # print('\t',i+1,j+1,' ',pv)
            PV[i,i] += pv
    pv = 2*V[i,0]*np.abs(Y[i,j])*math.cos(D[i,0]-D[j,0]-np.angle(Y[i,i]))
    # print('\t',pv)
    PV[i,i] += pv
for i in [0,2]:
    for j in range(N):
        if i != j:
            PV[i,j] = V[i,0]*np.abs(Y[i,j]) * math.cos(D[i,0]-D[j,0]-np.angle(Y[i,j]))
PV = np.row_stack(PV[0:3,0])
PV = np.row_stack((PV[0],PV[2]))
print(PV)
print("--------QD")
for i in [0,2]:
    for j in range(N):
        qd = V[i,0]*V[j,0]*np.abs(Y[i,j]) * math.cos(D[i,0]-D[j,0]-np.angle(Y[i,j]))
        # print('\t',i+1,j+1,' ',qd)
        QD[i,i] += qd
for i in [0,2]:
    for j in [0,2]:
        if i != j:
            qd = -V[i,0]*V[j,0]*np.abs(Y[i,j]) * math.cos(D[i,0]-D[j,0]-np.angle(Y[i,j]))
            QD[i,j] = qd
QD = np.column_stack(QD[0,0:3])
QD = np.transpose(QD)
QD = np.row_stack((QD[0],QD[2]))
QD = np.transpose(QD)
print(QD)
print("--------QV")
for i in [0,2]:
    for j in range(N):
        if i != j:
            qv = V[j,0]*np.abs(Y[i,j]) * math.sin(D[i,0]-D[j,0]-np.angle(Y[i,j]))
            # print('\t',i+1,j+1,' ',qv,(D[i,0]-D[j,0]-np.angle(Y[i,j]))/math.pi*180)
            QV[i,i] += qv
    qv = -2*V[i,0]*np.abs(Y[i,j])*math.sin(D[i,0]-D[j,0]-np.angle(Y[i,i]))
    # print('\t',qv,(D[i,0]-D[j,0]-np.angle(Y[i,i]))/math.pi*180)
    QV[i,i] += qv
for i in [0,2]:
    for j in range(N):
        if i != j:
            QV[i,j] = V[i,0]*np.abs(Y[i,j]) * math.sin(D[i,0]-D[j,0]-np.angle(Y[i,j]))
QV = np.column_stack(QV[0,0:1])
print(QV)
print("--------J")
JP = np.concatenate((PD,PV), axis=1)
JQ = np.concatenate((QD,QV), axis=1)
J = np.concatenate((JP,JQ))
print(J)


    