from datetime import datetime

start=datetime.now()
first_i=999
first_j=999
last_i=100
last_j=100
pal=[]

for i in range(first_i,last_i-1,-1):

    for j in range(first_j,last_j-1,-1):    
        num=[]
        num_rev=[]
        num_str=str(i*j)

        for k in num_str:
            num.append(k)

        num_rev=num.copy()
        num_rev.reverse()

        if num==num_rev:
            pal.append(int(num_str))

pal.sort()
print("loop over")
print("highest palindrome =",pal[-1])
print("\ntime elapsed=",datetime.now()-start)
            
        
