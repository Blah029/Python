x = [1, 2, 3, 5, 7, 8]
y = [3, 6, 19, 99, 291, 444]
a = [0]*len(x)
b = a.copy()
c = a.copy()
d = a.copy()
xVal = 2.5
iVal = 1

def quadraticSplines():

    def quadraticA(i):
        a[i] = (y[i+1]-y[i])/(x[i+1]-x[i])**2 - (2*a[i-1]*x[i] + b[i-1])/(x[i+1]-x[i])

    def quadraticB(i):
        b[i] = 2*a[i-1]*x[i] + b[i-1] - 2*a[i]*x[i]

    def quadraticC(i):
        c[i] = y[i] - (a[i]*x[i]**2 + b[i]*x[i])

    a[0] = 0
    b[0] = (y[1]-y[0])/(x[1]-x[0])
    quadraticC(0)

    for i in range(1,len(x)-1):
        quadraticA(i)
        quadraticB(i)
        quadraticC(i)

    for i in range(len(x)-1):
        print ("i=",i,"a=",a[i],"b=",b[i],"c=",c[i])

    print(a[iVal]*xVal**2 + b[iVal]*xVal + c[iVal])

def cubicSplines():

    def cubicA(i):
        a[i] = (y[i+1]-y[i])/(x[i+1]-x[i])**3 - (3*a[i-1]*x[i]**2+2*b[i-1]*x[i]+c[i-1])/(x[i+1]-x[i])**2 - (6*a[i-1]*x[i]+2*b[i-1])/(2*(x[i+1]-x[i]))

    def cubicB(i):
        b[i] = (6*a[i-1]*x[i] + 2*b[i-1] - 6*a[i]*x[i])/2

    def cubicC(i):
        c[i] = 3*a[i-1]*x[i]**2 + 2*b[i-1]*x[i] + c[i-1] - (3*a[i]*x[i]**2 + 2*b[i]*x[i])

    def cubicD(i):
        d[i] = y[i] - (a[i]*x[i]**3 + b[i]*x[i]**2 + c[i]*x[i])

    a[0] = 0
    b[0] = 0
    c[0] = (y[1]-y[0])/(x[1]-x[0])
    cubicD(0)

    for i in range(1,len(x)-1):
        cubicA(i)
        cubicB(i)
        cubicC(i)
        cubicD(i)

    for i in range(len(x)-1):
        print ("i=",i,"a=",a[i],"b=",b[i],"c=",c[i],"d=",d[i])

    print(a[iVal]*xVal**3 + b[iVal]*xVal**2 + c[iVal]*xVal + d[iVal])

quadraticSplines()
cubicSplines()