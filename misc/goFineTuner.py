import sys
sys.path.append("D:\\User Files\\Documents\\Python\\modules")
import numpy as np


data = np.array([[153.41000000000005,2579.017419925979],[154.19000000000005,2653.5296642233943],[155.24,2570.690786911442],[156.13000000000005,2502.1084526210107],[156.65000000000003,2567.3162283475076],[157.82000000000005,2567.3162283475076],[158.97,2156.594761543887],[159.63,2210.9072925400746],[161.19,2053.8560808576904],[161.69,2051.5262969015757],[162.6,2058.260031355638],[163.76999999999998,2058.260031355638],[165.33,1994.5585830414275],[166.74,1839.028904093021],[167.91,1839.028904093021]]
)
x, y = data[:,0], data[:,1]
xMax = np.max(x)
yMax = np.max(y)
prod = 0
prodX = 0
prodY = 0
for i, j in zip(x,y):
    if i*j > prod:
        prod = i*j
        prodX = i
        prodY = j
# print("x weight:  {:12f}    y weight:  {:12f}".format(1/xMax,1/yMax))
print("x max:     {:12f}    y max:     {:12f}".format(xMax,yMax))
print("x optimal: {:12f}    y optimal: {:12f}".format(prodX,prodY))
print("x ratio :  {:12f}    y ratio:   {:12f}".format(prodX/xMax,prodY/yMax))
