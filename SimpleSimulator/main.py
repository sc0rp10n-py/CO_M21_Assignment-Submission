'''
Anjali Sarda - 2020174
Ankush Kumar Jha - 2020175
Pragyan Yadav - 2020226
'''
from matplotlib import pyplot as plt
import numpy as np

#registers dict
REGISTER_REVERSE = {
    '000': 'R0',
    '001': 'R1',
    '010': 'R2',
    '011': 'R3',
    '100': 'R4',
    '101': 'R5',
    '110': 'R6',
    '111': 'FLAGS',
}

#opcode dict
OPCODE = {
    'add': '00000',
    'sub': '00001',
    'mov': '00010',
    'mov2': '00011',
    'ld': '00100',
    'st': '00101',
    'mul': '00110',
    'div': '00111',
    'rs': '01000',
    'ls': '01001',
    'xor': '01010',
    'or': '01011',
    'and': '01100',
    'not': '01101',
    'cmp': '01110',
    'jmp': '01111',
    'jlt': '10000',
    'jgt': '10001',
    'je': '10010',
    'hlt': '10011',
}

regValues = {
    'R0': 0,
    'R1': 0,
    'R2': 0,
    'R3': 0,
    'R4': 0,
    'R5': 0,
    'R6': 0,
    'FLAGS': 0,
}

# global progCount
# progCount = 0

def dec2bin(dec, a=16):
    #decimal to binary
    dec = int(dec)
    tbinary = bin(dec).replace('0b', '')
    binary = ''
    if len(tbinary) < 16:
        binary += '0'*(a-len(tbinary))
    binary += tbinary
    return binary

def bin2dec(binary):
    #binary to decimal
    binary = str(binary)
    dec = int(binary, 2)
    return dec

def typeA(op, r1, r2, r3):
    r1 = REGISTER_REVERSE[r1]
    r2 = REGISTER_REVERSE[r2]
    r3 = REGISTER_REVERSE[r3]
    if op == OPCODE['add']:
        regValues[r1] = regValues[r2] + regValues[r3]
        if regValues[r1] > 16:
            regValues['FLAGS'] = 8
            regValues[r1] = int(str(regValues[r1])[-16:])
    elif op == OPCODE['sub']:
        regValues[r1] = regValues[r2] - regValues[r3]
        if regValues[r1] < 0:
            regValues['FLAGS'] = 8
            regValues[r1] = 0
    elif op == OPCODE['mul']:
        regValues[r1] = regValues[r2] * regValues[r3]
        if regValues[r1] > 16:
            regValues['FLAGS'] = 8
            regValues[r1] = int(str(regValues[r1])[-16:])
    elif op == OPCODE['xor']:
        regValues[r1] = regValues[r2] ^ regValues[r3]
    elif op == OPCODE['or']:
        regValues[r1] = regValues[r2] | regValues[r3]
    elif op == OPCODE['and']:
        regValues[r1] = regValues[r2] & regValues[r3]
    
def typeB(op, r1, a):
    r1 = REGISTER_REVERSE[r1]
    a = bin2dec(a)
    if op == OPCODE['mov']:
        regValues[r1] = a
    elif op == OPCODE['rs']:
        regValues[r1] = regValues[r1] >> a
    elif op == OPCODE['ls']:
        regValues[r1] = regValues[r1] << a