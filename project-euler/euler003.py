from datetime import datetime

start=datetime.now()
i=1
n=600851475143
f=[]

while i<=n:
    
    if n%i==0 and i%2!=0:
        n=n/i
        f.append(i)
        print(i,"odd factor of n")
        
    i+=1
    
print("highest prime factor =",f[-1])
print("\ntime elapsed=",datetime.now()-start)
