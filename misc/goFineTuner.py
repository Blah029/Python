import numpy as np


data = np.array()
x, y = data[:,0], data[:,1]
xMax = np.max(x)
yMax = np.max(y)
# Calculate optimal through normalised summation
sum = 0
sumX = 0
sumY = 0
for i, j in zip(x,y):
    if i/xMax+j/yMax > sum:
        sum = i/xMax + j/yMax
        sumX = i
        sumY = j
# print("sum")
# print("x weight:  {:12f}    y weight:  {:12f}".format(1/xMax,1/yMax))
print("x max:     {:12f}    y max:     {:12f}".format(xMax,yMax))
print("x optimal: {:12f}    y optimal: {:12f}".format(sumX,sumY))
print("x ratio:   {:12f}    y ratio:   {:12f}".format(sumX/xMax,sumY/yMax))
# Calculate optimal through muliplication
prod = 0
prodX = 0
prodY = 0
for i, j in zip(x,y):
    if i*j > prod:
        prod = i*j
        prodX = i
        prodY = j
# print("prod")
# print("x weight:  {:12f}    y weight:  {:12f}".format(1/xMax,1/yMax))
# print("x max:     {:12f}    y max:     {:12f}".format(xMax,yMax))
# print("x optimal: {:12f}    y optimal: {:12f}".format(prodX,prodY))
# print("x ratio:   {:12f}    y ratio:   {:12f}".format(prodX/xMax,prodY/yMax))
if sumX != prodX or sumY != prodY:
    print("\nWARNING: Conflicting results\n")