#a*b*c product of the pythagorean triplet in which a+b+c=1000 and a<b<c
from datetime import datetime

start=datetime.now()

for a in range(1,1000):
    b_c=1000-a

    for b in range(1,1000):
        c=b_c-b

        if a<b<c and a+b+c==1000 and a**2+b**2==c**2:
            #print("a=",a,", b=",b,", c=",c)
            print("a= {0}, b= {1}, c= {2}".format(a,b,c))
            print("a*b*c=",a*b*c)
            
print("\ntime elsapsed=",datetime.now()-start)
