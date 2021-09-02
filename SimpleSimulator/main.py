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
        if regValues[r1] > 65535:
            regValues['FLAGS'] = 8
            # regValues[r1] = int(str(regValues[r1])[-16:])
            regValues[r1] = bin2dec(dec2bin(regValues[r1])[-16:])
    elif op == OPCODE['sub']:
        regValues[r1] = regValues[r2] - regValues[r3]
        if regValues[r1] < 0:
            regValues['FLAGS'] = 8
            regValues[r1] = 0
    elif op == OPCODE['mul']:
        regValues[r1] = regValues[r2] * regValues[r3]
        if regValues[r1] > 65535:
            regValues['FLAGS'] = 8
            # regValues[r1] = int(str(regValues[r1])[-16:])
            regValues[r1] = bin2dec(dec2bin(regValues[r1])[-16:])
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
        a = ''
        r2 = dec2bin(regValues[r2])
        for i in range(16):
            if r2[i] == '0':
                a += '1'
            elif r2[i] == '1':
                a += '0'
        regValues[r1] = bin2dec(a)
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
        if regValues[r1] > 65535:
            variables[bin2dec(a)] = bin2dec(dec2bin(regValues[r1])[-16:])
        else:
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

def graph(progList, cycle):
    progList = np.array(progList)
    cycle = np.array(cycle)
    # print(progList)
    # print(cycle)
    plt.scatter(cycle, progList, color='red')
    plt.plot(cycle, progList)
    plt.title('Simulator Scatter Plot')
    plt.xlabel('Cycle Number')
    plt.ylabel('Memory Address')
    plt.savefig('graph.png')

def main():
    instructions = {} #dict of instructions
    global variables, progCount, progList, i
    variables = {} #dict of variables
    t = 0 #temp
    progCount = 0 #program counter
    progList = [] #list of program counter

    while True:
        try:
            line = input().strip()
            if line != '':
                instructions[t] = line
                t += 1
        except EOFError:
            break

    # varIndex = len(instructions)
    for i in range(len(instructions)):
        if instructions[i][0:5] in [OPCODE['st'], OPCODE['ld']]:
            variables[bin2dec(instructions[i][8:16])] = 0
    
    i = 0 #instruction count
    hltornot = None
    hltrun = False
    while instructions[i][0:5] not in [OPCODE['hlt']]:
        if instructions[i][0:5] in [OPCODE['add'], OPCODE['sub'], OPCODE['mul'], OPCODE['xor'], OPCODE['or'], OPCODE['and']]:
            #typeA
            oldFlag = regValues['FLAGS']
            typeA(instructions[i][0:5], instructions[i][7:10], instructions[i][10:13], instructions[i][13:16])
            if oldFlag == regValues['FLAGS']:
                regValues['FLAGS'] = 0
            printIns()
            progList.append(progCount)
            progCount += 1
            i += 1
        elif instructions[i][0:5] in [OPCODE['mov'], OPCODE['rs'], OPCODE['ls']]:
            #typeB
            oldFlag = regValues['FLAGS']
            typeB(instructions[i][0:5], instructions[i][5:8], instructions[i][8:16])
            if oldFlag == regValues['FLAGS']:
                regValues['FLAGS'] = 0
            printIns()
            progList.append(progCount)
            progCount += 1
            i += 1
        elif instructions[i][0:5] in [OPCODE['mov2'], OPCODE['div'], OPCODE['not'], OPCODE['cmp']]:
            #typeC
            oldFlag = regValues['FLAGS']
            typeC(instructions[i][0:5], instructions[i][10:13], instructions[i][13:16])
            if oldFlag == regValues['FLAGS']:
                regValues['FLAGS'] = 0
            printIns()
            progList.append(progCount)
            progCount += 1
            i += 1
        elif instructions[i][0:5] in [OPCODE['ld'], OPCODE['st']]:
            #typeD
            oldFlag = regValues['FLAGS']
            typeD(instructions[i][0:5], instructions[i][5:8], instructions[i][8:16])
            if oldFlag == regValues['FLAGS']:
                regValues['FLAGS'] = 0
            printIns()
            progList.append(progCount)
            progCount += 1
            i += 1
        elif instructions[i][0:5] in [OPCODE['jmp'], OPCODE['jlt'], OPCODE['jgt'], OPCODE['je']]:
            #typeE
            # oldFlag = regValues['FLAGS']
            oldi = i
            oldFlag = regValues['FLAGS']
            # print(oldi, progCount)
            print(f'{dec2bin(progCount, 8)} {dec2bin(regValues["R0"])} {dec2bin(regValues["R1"])} {dec2bin(regValues["R2"])} {dec2bin(regValues["R3"])} {dec2bin(regValues["R4"])} {dec2bin(regValues["R5"])} {dec2bin(regValues["R6"])} {dec2bin(0)}')
            progList.append(progCount)
            typeE(instructions[i][0:5], instructions[i][8:16])
            if oldFlag == regValues['FLAGS']:
                regValues['FLAGS'] = 0
            if oldi == i:
                progCount += 1
                i += 1
            # print(i, progCount)
            # printIns()
            hltornot = instructions[i][0:5]
        if hltornot in [OPCODE['hlt']]:
            #typeF
            # typeF(instructions[i][0:5])
            hltrun = True
            # print('in if')
            regValues['FLAGS'] = 0
            printIns()
            progList.append(progCount)
            break
    if hltrun == False and instructions[i][0:5] in [OPCODE['hlt']]:
        #typeF
        # typeF(instructions[i][0:5])
        regValues['FLAGS'] = 0
        printIns()
        progList.append(progCount)
        # print('outif')
    memDump(instructions)
    cycle = [x for x in range(len(progList))]
    # print(progList)
    # print(cycle)
    # graph(progList, cycle)

if __name__ == '__main__':
    main()