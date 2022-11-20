import numpy as np


# From GO
data = np.array()
# Preferences (use 1 or 1.5 weight)
xMin = 0
yMin = 0
xWight = 1
yWeight = 1

x, y = data[:,0], data[:,1]
xMax = np.max(x)
yMax = np.max(y)
prod = 0
prodX = 0
prodY = 0
for i, j in zip(x,y):
    if i**xWight * j**yWeight > prod and i > xMin+0.0000009 and j > yMin+0.0000009:
        prod = i**xWight * j**yWeight
        prodX = i
        prodY = j
# print("x weight:  {:12f}    y weight:  {:12f}".format(1/xMax,1/yMax))
print("x max:     {:12f}    y max:     {:12f}".format(xMax,yMax))
print("x optimal: {:12f}    y optimal: {:12f}".format(prodX,prodY))
print("x ratio:   {:12f}    y ratio:   {:12f}".format(prodX/xMax,prodY/yMax))
