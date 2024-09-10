# Assume we received this bit stream (same as encoded_data)
received_data = '1110001111010'
Gx = '110011'

def xor(a, b):
    # XOR operation between two strings
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)

def mod2div(dividend, divisor):
    # Modulo-2 division (similar to binary division)
    pick = len(divisor)
    tmp = dividend[0:pick]
    
    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:
            tmp = xor('0'*pick, tmp) + dividend[pick]
        pick += 1
    
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)
    
    return tmp

# Perform the check
received_remainder = mod2div(received_data, Gx)

if received_remainder == '0'*(len(Gx)-1):
    print("No error detected in the received data.")
else:
    print("Error detected in the received data.")
