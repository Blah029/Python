def binary(bits):
    return "".join(bits)

def decimal(bits):
    decVal = 0

    for n in range (0,len(bits)):
        decVal += int(bits[n])*2**(len(bits)-n-1)

    return decVal

ref = "111111111111"
bitsChecked = 5
readings = []

for i in range(2):
    readings.append(ref[:bitsChecked]+str(i)*(len(ref)-bitsChecked))

print("check first",bitsChecked,"bits")
print("reference:",ref)
print("readings :")
print("          ",readings[0])
print("          ",readings[1])
print("tolerance:")

for entry in readings:
    print("          ",abs(decimal(entry)-decimal(ref))/decimal(ref))
