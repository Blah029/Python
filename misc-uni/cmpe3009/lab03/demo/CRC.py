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

def encode_data(data, key):
    key_len = len(key)
    appended_data = data + '0'*(key_len-1)
    remainder = mod2div(appended_data, key)
    return data + remainder

# Given G(x) and D(x)
Dx = '100100'
Gx = '1101'

# Calculate the CRC
encoded_data = encode_data(Dx, Gx)
crc = encoded_data[-(len(Gx)-1):]

print(f"Original data: {Dx}")
print(f"Generator polynomial: {Gx}")
print(f"CRC: {crc}")
print(f"Encoded data: {encoded_data}")