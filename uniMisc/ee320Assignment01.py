from math import pi
import matplotlib.pyplot as plt

# given constants
v0 = 100
d = 10
h=0.1
rho0 = 10**(-10)
a = 5
epsilonR = 4
epsilon0 = 1/(36*pi)*10**(-9)
epsilon = epsilon0*epsilonR

# functions
def rho(z):
    return rho0/a*z

def phi(z):
    return -rho0/(6*a*epsilon)*z**3 + (v0/d + rho0*d**2/(6*a*epsilon))*z

def E(z):
    return rho0/(2*a*epsilon)*z**2 + v0/d + rho0*d**2/(6*a*epsilon)

# analytical method
phiAnalytical = [0]*101

for i in range(101):
    phiAnalytical[i] = phi(i*h)

# numerical method (finite difference method)
phiNumerical = [0]*101
phiNumerical[0] = phi(0)
phiNumerical[100] = phi(10)

def calculatePhi(node):
    z = node*h
    return (phiNumerical[node-1] + phiNumerical[node+1] + rho(z)*h**2/epsilon)/2

for i in range(1000):

    for j in range(1,100):
        phiNumerical[j] = calculatePhi(j)

# plot
z = [i/10 for i in range(101)]
plt.plot(z,phiAnalytical, label="Analytical Method")
plt.plot(z,phiNumerical, label="Numerical Method")
plt.xlabel("z")
plt.ylabel("phi(z)")
plt.title("Analytical and Numerical Value Comparison")
plt.legend()
plt.grid()
plt.show()