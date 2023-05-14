from datetime import datetime

start=datetime.now()
(i,j,k)=(1,1,1)
sum=0

while i<4000001:
    
    if i%2==0:
        sum=sum+i
        print(i, "even fibonacci")
        
    else:
        print(i)
        
    i=j+k
    k=j
    j=i
    
print("loop over")
print("i =",i)
print("j =",j)
print("k =",k)
print("sum =",sum)
print("\ntime elspsed=",datetime.now()-start)
