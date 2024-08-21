#multiples of 3 or 5 below 1000
from datetime import datetime

start=datetime.now()
total=0

for number in range(1000):

    if number%3==0 or number%5==0:
        total+=number

print(total)
print("time elapsed=",datetime.now()-start)
