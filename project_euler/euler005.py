import sys
sys.path.append(open("_modulePath.txt").read())
from myMath import primeNumbers
from myMath import primeFactors
from roughWork import expand
from datetime import datetime

start=datetime.now()
pn=primeNumbers(20)
all_pf=[]
occur={2:0,3:0,5:0,7:0,11:0,13:0,17:0,19:0}
answer=1

for a in range(2,21):
    all_pf.append(primeFactors(a))

for b in all_pf:
    print(all_pf.index(b)+2,"= ",b, sep="")

    for c in pn:
            
        if b.count(c)>occur[c]:
            occur[c]=b.count(c)

expand(occur)

for d in occur:
    answer*=d**occur[d]

print("answer=",answer)
print("\ntime elapsed=",datetime.now()-start)
