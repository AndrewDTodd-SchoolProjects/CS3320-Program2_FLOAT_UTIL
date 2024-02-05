import struct
import sys
import numpy as np
import math

def float_to_bin(number):
    if sys.float_info.max_exp == 1024:
        return format(struct.unpack('!Q', struct.pack('!d', number))[0], '064b')
    else:
        return format(struct.unpack('!I', struct.pack('!f', number))[0], '032b')

def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0
    
def exponent(x) -> int:
    bin_str = float_to_bin(x)
    if sys.float_info.max_exp == 1024:
        biased_exponent = int(bin_str[1:12], 2)
        return biased_exponent - 1023 if biased_exponent != 0 else -1022
    else:
        biased_exponent = int(bin_str[1:9], 2)
        return biased_exponent - 126 if biased_exponent != 0 else -126

def fraction(x) -> int:
    bin_str = float_to_bin(x)
    if sys.float_info.max_exp == 1024:
        return int(bin_str[12:], 2) / (2 ** 52)
    else:
        return int(bin_str[9:], 2) / (2 ** 23)

def mantissa(x) -> int:
    return 1 + fraction(x) if exponent(x) != (2 - sys.float_info.max_exp) else fraction(x)

def is_posinfinity(x) -> bool:
    return x > 0 and exponent(x) == sys.float_info.max_exp and fraction(x) == 0

def is_neginfinity(x) -> bool:
    return x < 0 and exponent(x) == sys.float_info.max_exp and fraction(x) == 0

def ulp(x) -> int:
    if sys.float_info.max_exp == 1024:
        return abs(x - struct.unpack('!d', struct.pack('!Q', struct.unpack('!Q', struct.pack('!d', x))[0] + 1))[0])
    else:
        return abs(x - struct.unpack('!f', struct.pack('!I', struct.unpack('!I', struct.pack('!f', x))[0] + 1))[0])

def ulps(x, y) -> int:
    if sys.float_info.max_exp == 1024:
        return abs(struct.unpack('!Q', struct.pack('!d', x))[0] - struct.unpack('!Q', struct.pack('!d', y))[0])
    else:
        return abs(struct.unpack('!I', struct.pack('!f', x))[0] - struct.unpack('!I', struct.pack('!f', y))[0])
    
if __name__ == '__main__':
    y = 6.5
    subMin = np.nextafter(0,1) #subMin = 5e-324
    print(sign(y)) #1
    print(sign(0.0)) #0
    print(sign(-y)) #-1
    print(sign(-0.0)) #0
    print(exponent(y)) #2
    print(exponent(16.6)) #4
    print(fraction(0.0)) #0.0
    print(mantissa(y)) #1.625
    print(mantissa(0.0)) #0.0
    var1 = float('nan')
    print(exponent(var1)) #1024
    print(exponent(0.0)) #0
    print(exponent(subMin)) #-1022
    print(is_posinfinity(math.inf)) #True
    print(is_neginfinity(math.inf)) #False
    print(not is_posinfinity(-math.inf)) #True
    print(is_neginfinity(-math.inf)) #True
    print(ulp(y)) #8.881784197001252e-16
    print(ulp(1.0)) #2.220446049250313e-16
    print(ulp(0.0)) #5e-324
    print(ulp(subMin)) #5e-324
    print(ulp(1.0e15)) #0.125
    print(ulps(1,2)) #4503599627370496