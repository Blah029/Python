import numpy as np
import matplotlib.pyplot as plt

# Create a grid of points
v1 = np.linspace(-10, 10, 100)
v2 = np.linspace(-10, 10, 100)
V1, V2 = np.meshgrid(v1, v2)

# Define matrices
V = np.array([v1,v2])
VT = np.transpose(V)
Q = np.array([[1,  1],
              [1, -1]])
VP = np.matmul(np.transpose(Q),V)
alpha = 0.9
lambda1 = 1 + alpha
lambda2 = 1 - alpha
LAMBDA = np.array([[lambda1, 0],
                   [0, lambda2]])
Emin = 1

# Define the function
E = Emin + np.matmul(np.transpose(VP), np.matmul(LAMBDA,V))

# Create the contour plot
plt.figure(figsize=(8, 6))
plt.contour(V1, V2, E, levels=20)   
plt.xlabel("v\'0")
plt.ylabel("v\'1")
plt.title('Contour plot of E')
plt.colorbar(label='E')
plt.grid(True)
plt.show()
