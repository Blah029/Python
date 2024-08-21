f=[]
pf=[]

for n in range(600851475143,0,-1):
    
    if len(pf)==0:
        
        for i in range(1,n+1):
            
            if n%i==0:
                f=f+[i]
                
        if len(f)<=2:
            
            if 600851475143%n==0:
                pf=pf+[n]
                print(n,"factor & prime number")
                
            else:
                print(n,"prime number")
                
            print("pf =",pf,"(length =",len(pf),")")
            
        f=[]
        
print("loop over")
print("largest prime factor is",pf[0])
