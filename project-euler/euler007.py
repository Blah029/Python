#10001st prime number
import datetime

primes=[2]
i=2
prime=None
x=datetime.datetime.now()

while len(primes)<10001:

    for j in primes:

        if i%j==0:
            prime=False
            break

        else:
            prime=True

    if prime==True:
        primes+=[i]

    i+=1

y=datetime.datetime.now()
print(primes.index(primes[-1])+1,"st prime= ",primes[-1], sep="")
print("time elapsed=",y-x)

#can't include 2 into for loop despite being a prime

#10001st prime number
#answer is 104743
