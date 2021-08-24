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

def typeC(op, r1, r2):
    r1 = REGISTER_REVERSE[r1]
    r2 = REGISTER_REVERSE[r2]
    if op == OPCODE['mov2']:
        regValues[r1] = regValues[r2]
    elif op == OPCODE['div']:
        regValues['R0'] = regValues[r1] // regValues[r2]
        regValues['R1'] = regValues[r1] % regValues[r2]
    elif op == OPCODE['not']:
        regValues[r1] = ~regValues[r2]
    elif op == OPCODE['cmp']:
        if regValues[r1] < regValues[r2]:
            regValues['FLAGS'] = 4
        elif regValues[r1] > regValues[r2]:
            regValues['FLAGS'] = 2
        elif regValues[r1] == regValues[r2]:
            regValues['FLAGS'] = 1

def typeD(op, r1, a):
    r1 = REGISTER_REVERSE[r1]
    if op == OPCODE['st']:
        variables[bin2dec(a)] = regValues[r1]
    elif op == OPCODE['ld']:
        regValues[r1] = variables[bin2dec(a)]

def typeE(op, a):
    global progCount, i
    a = bin2dec(a)
    if op == OPCODE['jmp']:
        i = a
        # progCount = progList[i]
        progCount = a
    elif op == OPCODE['jgt']:
        if regValues['FLAGS'] == 2:
            i = a
            # progCount = progList[i]
            progCount = a
    elif op == OPCODE['jlt']:
        if regValues['FLAGS'] == 4:
            i = a
            # progCount = progList[i]
            progCount = a
    elif op == OPCODE['je']:
        if regValues['FLAGS'] == 1:
            i = a
            # progCount = progList[i]
            progCount = a
    
# def typeF(op):
#     pass

def printIns():
    print(f'{dec2bin(progCount, 8)} {dec2bin(regValues["R0"])} {dec2bin(regValues["R1"])} {dec2bin(regValues["R2"])} {dec2bin(regValues["R3"])} {dec2bin(regValues["R4"])} {dec2bin(regValues["R5"])} {dec2bin(regValues["R6"])} {dec2bin(regValues["FLAGS"])}')

def memDump(instructions):
    count = 0
    for i in range(len(instructions)):
        print(f'{instructions[i]}')
        count += 1
    if len(variables) > 0:
        for i in range(len(instructions), len(instructions)+len(variables)):
            print(f'{dec2bin(variables[i])}')
            count += 1
    for i in range(count, 256):
        print('0'*16)