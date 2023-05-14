import numpy as np


# From GO
data = np.array()
# Preferences
min_x = 0
min_y = 0

x, y = data[:,0], data[:,1]
max_x = np.max(x)
max_y = np.max(y)
prod = 0
prod_x = 0
prod_y = 0
for i, j in zip(x,y):
    if i*j > prod and i > min_x+0.0000009 and j > min_y+0.0000009:
        prod = i*j
        prod_x = i
        prod_y = j
print("x weight:  {:12f}    y weight:  {:12f}".format(1/max_x,1/max_y))
print("x max:     {:12f}    y max:     {:12f}".format(max_x,max_y))
print("x optimal: {:12f}    y optimal: {:12f}".format(prod_x,prod_y))
print("x ratio:   {:12f}    y ratio:   {:12f}    overall:   {:12f}".format(
                                                 prod_x/max_x,prod_y/max_y,
                                                 prod_x*prod_y/max_x/max_y))
