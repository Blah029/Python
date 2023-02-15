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
P = np.array([[3.6],
              [0],
              [2]])
Q = np.array([[1.1833],
              [0],
              [0]])
N = np.shape(V)[0]
D = np.zeros((N,1))


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
JInverse = np.linalg.inv(J)
print(J)
print(JInverse)
#change in P,Q
print("--------P1,P3 inital")
PInitial = np.zeros((N,1))
for i in [0,2]:
    for j in range(N):
        # print('\t',i+1,j+1,'\t',V[i,0],np.abs(Y[i,j]),V[j,0],'\t',D[i,0],-D[j,0],-np.angle(Y[i,j])/math.pi*180)
        # print('\t',i+1,j+1,'\t',np.abs(V[i,0]*Y[i,j]*V[j,0]),math.cos(D[i,0]-D[j,0]-np.angle(Y[i,j])))
        # print('\t',i+1,j+1,'\t',np.abs(V[i,0]*Y[i,j]*V[j,0]) * math.cos(D[i,0]-D[j,0]-np.angle(Y[i,j])))
        PInitial[i,0] += np.abs(V[i,0]*Y[i,j]*V[j,0]) * math.cos(D[i,0]-D[j,0]-np.angle(Y[i,j]))
print(PInitial)
print("--------Q1 inital")
QInitial = np.zeros((N,1))
for i in [0]:
    for j in range(N):
        # print('\t',i+1,j+1,'\t',V[i,0],np.abs(Y[i,j]),V[j,0],'\t',D[i,0],-D[j,0],-np.angle(Y[i,j])/math.pi*180)
        # print('\t',i+1,j+1,'\t',np.abs(V[i,0]*Y[i,j]*V[j,0]),math.sin(D[i,0]-D[j,0]-np.angle(Y[i,j])))
        # print('\t',i+1,j+1,'\t',np.abs(V[i,0]*Y[i,j]*V[j,0]) * math.sin(D[i,0]-D[j,0]-np.angle(Y[i,j])))
        QInitial[i,0] += np.abs(V[i,0]*Y[i,j]*V[j,0]) * math.sin(D[i,0]-D[j,0]-np.angle(Y[i,j]))
print(QInitial)
print("--------PQ delta")
PDelta = P-PInitial
QDelta = Q-QInitial
PQDelta = np.row_stack((PDelta[0],PDelta[2],QDelta[0]))
print(PQDelta)
#voltage values
print("--------DV delta")
DVDelta = np.matmul(JInverse,PQDelta)
print(DVDelta)
print("--------DV")
DVInital = np.row_stack((D[0,0],D[2,0],V[0,0]))
DV = DVInital + DVDelta
print(DVInital)
print(DV)

#fast decouple
#jacobian matrix
print('\n',"--------J2", sep="")
JP2 = np.concatenate((PD,np.zeros((2,1))), axis=1)
JQ2 = np.concatenate((np.zeros((1,2)),QV), axis=1)
J2 = np.concatenate((JP2,JQ2))
J2Inverse = np.linalg.inv(J2)
print(J2)
print(J2Inverse)
#voltage values
print("--------DV delta")
DVDelta2 = np.matmul(J2Inverse,PQDelta)
print(DVDelta2)
print("--------DV")
DVInital = np.row_stack((D[0,0],D[2,0],V[0,0]))
DV2 = DVInital + DVDelta2
print(DVInital)
print(DV2)





    