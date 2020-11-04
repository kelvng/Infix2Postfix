import itertools


def readInfix(filename):
    with open(filename) as f:
        Infix = f.readlines()
    return Infix[0]
##########################################Student do these 2 function
def Infix2Postfix(Infix):
    Postfix = []
    Operator = {'~': 5, '&': 4, '|': 3, '>': 2, '=': 1, '(': 6}
    OpeStack = []
    for i in Infix:
        if i.isupper():
            Postfix.append(i)
        elif i in Operator:
            while (len(OpeStack) != 0 and Operator[i] <= Operator[OpeStack[-1]] and OpeStack[-1] != '('):
                Postfix.append(OpeStack.pop())
            OpeStack.append(i)
        elif i == '(':
            OpeStack.append(i)
        elif i == ')':
            while (OpeStack[-1] != '('):
                Postfix.append(OpeStack.pop())
            OpeStack.pop()
        else:
            exit()
    while len(OpeStack) > 0:
        if OpeStack[0] == ')':
            OpeStack.pop()
        else:
            Postfix.append(OpeStack.pop())
    return Postfix


def Postfix2Truthtable(Postfix):
    Truthtable = Postfix
    Character = []
    for i in Postfix:
        if i.isupper():
            Character.append(i)
    Character = list(set(Character))
    Character.sort()
    Truthtable = list(itertools.product([False, True], repeat = len(Character)))
    
    def Implies(a, b):
        if a:
            return b
        else:
            return True
    def implies(A, B):
        return [Implies(a, b) for a, b in zip(A, B)]
    def n(A):
        return [not k for k in A]
    def o(A, B):
        return [a or b for a, b in zip(A, B)]
    def a(A, B):
        return [a and b for a, b in zip(A, B)]
    def e(A, B):
        return [a == b for a, b in zip(A, B)]
    
    
    Operator = {'~': n, '&': a, '|': o, '>': implies, '=': e}
    Char = {Character[i]:[Table[i] for Table in Truthtable] for i in range(len(Character))}
    CalStack = []
    Truthtable = [[Table[i] for Table in Truthtable] for i in range(len(Character))]
    Temp1 = []
    Temp2 = []
    Temp3 = []    
    for i in Postfix:
        if i.isupper():
            for j in Character:
                if i == j:
                    CalStack.append(Char[j])
        if i in Operator:
            Temp1 = CalStack.pop()
            if i == '~':
                Truthtable.append(Operator[i](Temp1))
                CalStack.append(Operator[i](Temp1))
            elif i == '>':
                Temp2 = CalStack.pop()
                CalStack.append(Operator[i](Temp2, Temp1))
                Truthtable.append(Operator[i](Temp2, Temp1))  
            else:
                Temp2 = CalStack.pop()
                CalStack.append(Operator[i](Temp1, Temp2))
                Truthtable.append(Operator[i](Temp1, Temp2))                                   
    Truthtable = list(map(tuple, zip(*Truthtable)))
    return Truthtable
##########################################End student part
def writeTruthtable(table):
    import sys
    outfile=sys.argv[0]
    outfile=outfile[0:-2]
    outfile+="txt"  
    with open(outfile, 'w') as f:
        for lines in table:
            for item in lines:
                f.write("%s\t" % item)
            f.write("\n")
    f.close()
def main():
    Infix=readInfix("Logicexpression.txt")
    Postfix=Infix2Postfix(Infix)
    Truthtable=Postfix2Truthtable(Postfix)
    writeTruthtable(Truthtable)
main()
