import sys
sys.path.append(open("D:/User Files/Documents/Python/projectEuler/_modulePath.txt").read())
from datetime import datetime

def primeNumbers(upperLimit, lowerLimit=1):
    """Returns the prime numbers betwerrn upperLimit and lowerLimit"""

    if lowerLimit==1:
        primeNums=[2]
        a=2
        prime=None

        for _b in range(upperLimit-1):

            for c in primeNums:

                if a%c==0:
                    prime=False
                    break

                else:
                    prime=True

            if prime==True:
                primeNums+=[a]

            a+=1

    return primeNums

start=datetime.now()
total=0

for prime in primeNumbers(99999):
    total+=prime

print(total)
print("time elsapsed=",datetime.now()-start)
