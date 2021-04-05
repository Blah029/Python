s_sq=0
sq_s=0
s=0

for i in range(1,101):
    s_sq+=i**2
    s+=i
    
sq_s=s**2
print(sq_s-s_sq)
