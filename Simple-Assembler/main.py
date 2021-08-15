'''
Anjali Sarda - 2020174
Ankush Kumar Jha - 2020175
Pragyan Yadav - 2020226
'''

#registers dict
REGISTER = {
    'R0': '000',
    'R1': '001',
    'R2': '010',
    'R3': '011',
    'R4': '100',
    'R5': '101',
    'R6': '110',
    'FLAGS': '111',
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

def dec2bin(dec):
    #decimal to binary
    dec = int(dec)
    tbinary = bin(dec).replace('0b', '')
    binary = ''
    binary += '0'*(8-len(tbinary))
    binary += tbinary
    return binary

def hltcheck(statements):
    #check for hlt instruction
    h_count = 0
    for i in range(len(statements)):
        if statements[i][0] == 'hlt' or 'hlt' in statements[i]:
            h_count += 1
        if h_count > 1:
            print(f'More than 1 hlt is given on input line {i+1}')
            quit()

def varcount(statements, var):
    #counts the number of times a variable is used
    v_count = 0
    for i in range(len(statements)):
        if len(statements[i]) > 1 and statements[i][1] == var:
            v_count += 1
    return v_count

def varin(statements):
    #checks for variables in between instructions
    tvar = {}
    for i in range(len(statements)):
        if statements[i][0] != 'var':
            break
        tvar[i] = statements[i]

    for i in range(len(tvar), len(statements)):
        if statements[i][0] == 'var':
            print(f'Variables declared in between instructions in input line {i+1}')
            quit()

def lblcheck(statements):
    #check for labels
    label = {}
    lbl = 0
    for i in range(len(statements)):
        if ':' in statements[i][0]:
            label[lbl] = statements[i]
            lbl += 1
        if statements[i][0] in ['jmp', 'jlt', 'jgt', 'je']:
            for j in range(len(label)):
                if statements[i][2] not in label[j][0].rstrip(':'):
                    print(f'Undefined label called on line {i+1}')
                    quit()

def in_errorhandler(statements):
    #check for errors in input file
    if len(statements) > 256:
        print('Input exceeds 256 bit limit')
        quit()
    
    hltcheck(statements)

    for i in range(len(statements)):
        if statements[i][0] == 'var':
            vcount = varcount(statements, statements[i][1])
            if vcount > 1:
                print(f'2 or more variables with same name are passed on input line {i+1}')
                quit()
    
    varin(statements)
    lblcheck(statements)
    return None

def inschecker(instruction, i):
    #check for errors in instruction
    if ':' in instruction[0]:
        if instruction[1] in ['add', 'sub', 'mul', 'xor', 'or', 'and'] and len(instruction) != 5:
            print(f'Wrong ISA instruction on line {i+1}')
            quit()
        elif instruction[1] in ['mov', 'ld', 'st', 'div', 'rs', 'ls', 'not', 'cmp'] and len(instruction) != 4:
            print(f'Wrong ISA instruction on line {i+1}')
            quit()
        elif instruction[1] in ['jmp', 'jlt', 'jgt', 'je', 'var'] and len(instruction) != 3:
            print(f'Wrong ISA instruction on line {i+1}')
            quit()
        elif instruction[1] == 'hlt' and len(instruction) != 2:
            print(f'Wrong ISA instruction on line {i+1}')
            quit()
    elif instruction[0] in ['add', 'sub', 'mul', 'xor', 'or', 'and'] and len(instruction) != 4:
        print(f'Wrong ISA instruction on line {i+1}')
        quit()
    elif instruction[0] in ['mov', 'ld', 'st', 'div', 'rs', 'ls', 'not', 'cmp'] and len(instruction) != 3:
        print(f'Wrong ISA instruction on line {i+1}')
        quit()
    elif instruction[0] in ['jmp', 'jlt', 'jgt', 'je', 'var'] and len(instruction) != 2:
        print(f'Wrong ISA instruction on line {i+1}')
        quit()
    elif instruction[0] == 'hlt' and len(instruction) != 1:
        print(f'Wrong ISA instruction on line {i+1}')
        quit()
    return None

def flagerror(instruction, i):
    #check for errors in flags
    if instruction[0] != 'mov' and 'FLAGS' in instruction[1: len(instruction)]:
        print(f'Flag Error on line {i+1}')
        quit()

def varrepeat(variables):
    #check for repeat variables
    for i in range(len(variables)):
        for j in range(len(variables)):
            if variables[i] == variables[j] and i != j:
                print(f'Variable Name should be unique. Repeated on line {wovariables+j+1}')
                quit()

def varcheck(instructions, variables):
    #check for variables if defined or not
    for i in range(len(instructions)):
        if instructions[i][0] in ['ld', 'st']:
            for j in range(len(variables)):
                if variables[j][1] not in instructions[i][1:len(instructions[i])]:
                    print(f'Undefined variable called on line {i+1}')
                    quit()

def errorhandler(instructions):
    #main error handler
    for i in range(len(instructions)):
        if instructions[i][0] not in OPCODE and instructions[i][0] != 'var' and ':' not in instructions[i][0]:
            print(f'Wrong ISA Syntax on line {i+1}')
            quit()
        if instructions[i][0] == 'mov' and '$' in instructions[i][2]:
            if instructions[i][2].strip('$') not in range(0, 256):
                print(f'Illegal Immediate Value (less than 0 or more than 255) on line {i+1}')
                quit()
        elif ':' in instructions[i][0]:
            if ':' in instructions[i][1:len(instructions[i])]:
                print(f'Nesting of labels is illegal at line {i+1}')
                quit()
            else:
                for j in range(len(instructions)):
                    if instructions[i][0] == instructions[j][0] and i != j:
                        print(f'Label Name should be unique. Repeated on line {j+1}')
                        quit()

def typeA(op, r1, r2, r3):
    #type A: 3 register type
    r1 = r1.upper()
    r2 = r2.upper()
    r3 = r3.upper()
    print(op + '0'*2 + REGISTER[r1] + REGISTER[r2] + REGISTER[r3])

def typeB(op, r1, a):
    #type B: register and immediate value
    r1 = r1.upper()
    a = a.replace('$', '')
    print(op + REGISTER[r1] + dec2bin(a))

def typeC(op, r1, r2):
    #type C: 2 register type
    r1 = r1.upper()
    r2 = r2.upper()
    print(op + '0'*5 + REGISTER[r1] + REGISTER[r2])
    
def typeD(op, r1, mem):
    #type D: register and memory address type
    r1 = r1.upper()
    print(op + REGISTER[r1] + dec2bin(mem))

def typeE(op, mem):
    #type E: memody address type
    print(op + '0'*3 + dec2bin(mem))

def typeF(op):
    #type F: halt
    print(op + '0'*11)

    def main():
    statements = {} #dictionary to store all the statements
    instructions = {} #dictionary to store all the instructions
    variables = {} #dictionary to store all the variables
    labels = {} #dictionary to store all the labels
    t = 0
    lbl = 0
    global wovariables #instructions without variables length

    while True:
        try:
            l = input().split()
            if (l != ''):
                for i in range(len(l)):
                    l[i].strip()
                statements[t] = l
                t += 1
        except EOFError:
            break
    
    inerror = in_errorhandler(statements)

    ins = 0
    var = 0
    for i in range(len(statements)):
        if statements[i][0] == 'var':
        	variables[var] = statements[i]
        	var+=1                       	         
        else:
            instructions[ins] = statements[i]
            ins += 1
    
    # print(instructions)
    wovariables = len(instructions)
    lenins = wovariables
    for i in range(len(variables)):
        instructions[lenins] = variables[i]
        lenins += 1
    
    # print(statements)
    # print(instructions)
    # print(variables)
    # print(wovariables)
    varrepeat(variables)
    varcheck(instructions, variables)
    for i in range(len(instructions)):
        inscheck = inschecker(instructions[i], i)
        flagerror(instructions[i], i)
        errorhandler(instructions)
        if ':' in instructions[i][0]:
            labels[lbl] = instructions[i]
            lbl += 1
            if instructions[i][1] == 'add':
                typeA(OPCODE['add'], instructions[i][2], instructions[i][3], instructions[i][4])
            elif instructions[i][1] == 'sub':
                typeA(OPCODE['sub'], instructions[i][2], instructions[i][3], instructions[i][4])
            elif instructions[i][1] == 'ld':
                for j in range(len(variables)):
                    if instructions[i][3] == variables[j][1]:
                        mem = j + wovariables
                        typeD(OPCODE['ld'], instructions[i][2], mem)
            elif instructions[i][1] == 'st':
                for j in range(len(variables)):
                    if instructions[i][3] == variables[j][1]:
                        mem = j + wovariables
                        typeD(OPCODE['st'], instructions[i][2], mem)
            elif instructions[i][1] == 'mul':
                typeA(OPCODE['mul'], instructions[i][2], instructions[i][3], instructions[i][4])
            elif instructions[i][1] == 'div':
                typeC(OPCODE['div'], instructions[i][2], instructions[i][3])
            elif instructions[i][1] == 'rs':
                typeB(OPCODE['rs'], instructions[i][2], instructions[i][3])
            elif instructions[i][1] == 'ls':
                typeB(OPCODE['ls'], instructions[i][2], instructions[i][3])
            elif instructions[i][1] == 'xor':
                typeA(OPCODE['xor'], instructions[i][2], instructions[i][3], instructions[i][4])
            elif instructions[i][1] == 'or':
                typeA(OPCODE['or'], instructions[i][2], instructions[i][3], instructions[i][4])
            elif instructions[i][1] == 'and':
                typeA(OPCODE['and'], instructions[i][2], instructions[i][3], instructions[i][4])
            elif instructions[i][1] == 'not':
                typeC(OPCODE['not'], instructions[i][2], instructions[i][3])
            elif instructions[i][1] == 'cmp':
                typeC(OPCODE['cmp'], instructions[i][2], instructions[i][3])
            elif instructions[i][1] == 'jmp':
                for j in range(len(instructions)):
                    if instructions[i][2] == instructions[j][0]:
                        mem = j
                        typeE(OPCODE['jmp'], mem)
            elif instructions[i][1] == 'jlt':
                for j in range(len(instructions)):
                    if instructions[i][2] == instructions[j][0]:
                        mem = j
                        typeE(OPCODE['jlt'], mem)
            elif instructions[i][1] == 'jgt':
                for j in range(len(instructions)):
                    if instructions[i][2] == instructions[j][0]:
                        mem = j
                        typeE(OPCODE['jgt'], mem)
            elif instructions[i][1] == 'je':
                for j in range(len(instructions)):
                    if instructions[i][2] == instructions[j][0]:
                        mem = j
                        typeE(OPCODE['je'], mem)
            elif instructions[i][1] == 'hlt':
                typeF(OPCODE['hlt'])
            elif instructions[i][1] == 'mov':
                if '$' not in instructions[i][3]:
                    # move register
                    typeC(OPCODE['mov2'], instructions[i][2], instructions[i][3])
                else:
                    # move immediate
                    typeB(OPCODE['mov'], instructions[i][2], instructions[i][3])
            
        elif instructions[i][0] == 'add':
            typeA(OPCODE['add'], instructions[i][1], instructions[i][2], instructions[i][3])
        elif instructions[i][0] == 'sub':
            typeA(OPCODE['sub'], instructions[i][1], instructions[i][2], instructions[i][3])
        elif instructions[i][0] == 'ld':
            for j in range(len(variables)):
                if instructions[i][2] == variables[j][1]:
                    mem = j + wovariables
                    typeD(OPCODE['ld'], instructions[i][1], mem)
        elif instructions[i][0] == 'st':
            for j in range(len(variables)):
                if instructions[i][2] == variables[j][1]:
                    mem = j + wovariables
                    typeD(OPCODE['st'], instructions[i][1], mem)
        elif instructions[i][0] == 'mul':
            typeA(OPCODE['mul'], instructions[i][1], instructions[i][2], instructions[i][3])
        elif instructions[i][0] == 'div':
            typeC(OPCODE['div'], instructions[i][1], instructions[i][2])
        elif instructions[i][0] == 'rs':
            typeB(OPCODE['rs'], instructions[i][1], instructions[i][2])
        elif instructions[i][0] == 'ls':
            typeB(OPCODE['ls'], instructions[i][1], instructions[i][2])
        elif instructions[i][0] == 'xor':
            typeA(OPCODE['xor'], instructions[i][1], instructions[i][2], instructions[i][3])
        elif instructions[i][0] == 'or':
            typeA(OPCODE['or'], instructions[i][1], instructions[i][2], instructions[i][3])
        elif instructions[i][0] == 'and':
            typeA(OPCODE['and'], instructions[i][1], instructions[i][2], instructions[i][3])
        elif instructions[i][0] == 'not':
            typeC(OPCODE['not'], instructions[i][1], instructions[i][2])
        elif instructions[i][0] == 'cmp':
            typeC(OPCODE['cmp'], instructions[i][1], instructions[i][2])
        elif instructions[i][0] == 'jmp':
            for j in range(len(instructions)):
                if instructions[i][1] == instructions[j][0].rstrip(':'):
                    mem = j
                    typeE(OPCODE['jmp'], mem)
        elif instructions[i][0] == 'jlt':
            for j in range(len(instructions)):
                if instructions[i][1] == instructions[j][0].rstrip(':'):
                    mem = j
                    typeE(OPCODE['jlt'], mem)
        elif instructions[i][0] == 'jgt':
            for j in range(len(instructions)):
                if instructions[i][1] == instructions[j][0].rstrip(':'):
                    mem = j
                    typeE(OPCODE['jgt'], mem)
        elif instructions[i][0] == 'je':
            for j in range(len(instructions)):
                if instructions[i][1] == instructions[j][0].rstrip(':'):
                    mem = j
                    typeE(OPCODE['je'], mem)
        elif instructions[i][0] == 'hlt':
            typeF(OPCODE['hlt'])
        elif instructions[i][0] == 'mov':
            if '$' not in instructions[i][2]:
                # move register
                typeC(OPCODE['mov2'], instructions[i][1], instructions[i][2])
            else:
                # move immediate
                typeB(OPCODE['mov'], instructions[i][1], instructions[i][2])
    
if __name__ == '__main__':
    main()