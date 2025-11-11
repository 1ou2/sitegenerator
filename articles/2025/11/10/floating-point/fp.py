import struct
import sys
import numpy as np
from math import pi
import torch
from tabulate import tabulate

def float32_to_binary(num):
    return ''.join(f'{b:08b}' for b in struct.pack('!f', num))

def binary_to_float32(binary):
    return struct.unpack('!f', int(binary, 2).to_bytes(4, byteorder='big'))[0]

def float64_to_binary(num):
    return ''.join(f'{b:08b}' for b in struct.pack('!d', num))

def binary_to_float64(binary):
    return struct.unpack('!d', int(binary, 2).to_bytes(8, byteorder='big'))[0]

def pprint_float32(num):
    binary = float32_to_binary(num)
    sign = binary[0]
    exponent = binary[1:9]
    fraction = binary[9:]
    print(f"Float32 representation of {num}:")
    print(f"Sign: {sign}")
    print(f"Exponent: {exponent}")
    print(f"Fraction: {fraction}")

def pprint_float64(num):
    binary = float64_to_binary(num)
    sign = binary[0]
    exponent = binary[1:12]
    fraction = binary[12:]
    print(f"Float64 representation of {num}:")
    print(f"Sign: {sign}")
    print(f"Exponent: {exponent}")
    print(f"Fraction: {fraction}\n")

num = 1.5

pprint_float64(num)

float32_pi= np.float32(pi)
pprint_float32(float32_pi)
float64_pi = np.float64(pi)
pprint_float64(float64_pi)



f32_type = torch.float32
bf16_type = torch.bfloat16
e4m3_type = torch.float8_e4m3fn
e5m2_type = torch.float8_e5m2

# collect finfo for each type
table = []
for dtype in [f32_type, bf16_type, e4m3_type, e5m2_type]:
    numbits = 32 if dtype == f32_type else 16 if dtype == bf16_type else 8
    info = torch.finfo(dtype)
    table.append([info.dtype, numbits, info.max, 
                  info.min, info.smallest_normal, info.eps])

headers = ['data type', 'bits', 'max', 'min', 'smallest normal', 'eps']
print(tabulate(table, headers=headers))

# use numpy float32 with number 1.5
np_float32 = np.float32(0.1)
print(f"Numpy float32 representation of 1.5: {float32_to_binary(np_float32)}")
pprint_float32(np_float32)