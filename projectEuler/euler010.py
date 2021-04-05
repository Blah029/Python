import sys
sys.path.append(open("D:/User Files/Documents/Python/projectEuler/_modulePath.txt").read())
from datetime import datetime
from myMath import primeNumbers

start=datetime.now()
total=0

for prime in primeNumbers(99999):
##for prime in primeNumbers(1999999):
    total+=prime

print(total)
print("time elsapsed=",datetime.now()-start)
