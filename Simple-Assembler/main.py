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