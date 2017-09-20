import sys
import ast

sides = 6

if len(sys.argv)>1:
    try:
        sides = int(sys.argv[1])
        sys.argv = sys.argv[1:]
    except ValueError:
        pass

if len(sys.argv)>2:
    premises = sys.argv[1:-1]
    conclusion = sys.argv[-1]
else:
    print("python probab-reasoning.py [n] premise1 premise2 ... conclusion\n")
    print("The premises and conclusion can contain up to five events designated by \na single letter other than P.\n")
    print("The optional n parameter specifies how many die sides to use.\n")
    print("Boolean operations allowed:")
    print(" a&b : conjunction of a with b")
    print(" a|b : disjunction of a with b (not to be confused with conditional probability)")
    print(" ~a  : negation of a\n")
    print("Probabilistic operations allowed:")
    print(" P(a) : unconditional probability of a")
    print(" P(a,b) : conditional probability of a given b")    
    print(" supports(a,b) : short for: P(a,b) > P(a)\n")
    print("You can operate on the probabilities with standard arithmetical operations and comparisons.\n")
    print("Any expression which involves a divide by zero counts as automatically false.") 
    sys.exit(1)
    
variables = set()

def addVariables(s):
    for node in ast.walk(ast.parse(s)):
        if isinstance(node, ast.Name) and len(node.id)==1 and node.id != "P":
            variables.add(node.id)
            
for premise in premises:
    addVariables(premise)
addVariables(conclusion)

compiledPremises = [compile(premise, '<string>', 'eval') for premise in premises]
compiledConclusion = compile(conclusion, '<string>', 'eval')

variableTuple = tuple(sorted(variables))

if len(variableTuple) < 1 or len(variableTuple) > 5:
    print("Number of variables must be between 1 and 5.")
    sys.exit(2)

Omega = set(range(1,sides+1))
OmegaList = list(range(1,sides+1))

class mySet(set):
    def __invert__(self):
        return Omega-self
        
    def __str__(self):
        return str(sorted(self)).replace("[","{").replace("]","}")

def makeSet(l, binary):
    s = mySet()
    x = 0
    while binary:
        if binary&1:
            s.add(l[x])
        x += 1
        binary >>= 1
    return s
    
def P(*s):
    if len(s) > 1:
        return len(s[0] & s[1]) / float(len(s[1]))
    return len(s[0]) / float(sides)
    
def supports(p,q):
    return P(q) < P(q,p)
    
def checkPremises(vars):
    try:
        for premise in compiledPremises:
            if not eval(premise, vars):
                return False
        return True
    except ZeroDivisionError:
        return False
        
def checkConclusion(vars):
    try:
        return eval(compiledConclusion, vars)
    except ZeroDivisionError:
        return False

def generate(position,dict,intersectionSoFar=OmegaList,intersectionComplementsSoFar=OmegaList):
    def generateSets():
        if len(intersectionSoFar)==sides and len(intersectionComplementsSoFar)==sides:            
            for n in range(sides+1):
                yield makeSet(OmegaList,2**n-1)
        elif len(intersectionSoFar)==0 and len(intersectionComplementsSoFar)==0:
            for n1 in range(2**sides):
                yield makeSet(OmegaList,n1)
        elif len(intersectionSoFar)>0 and len(intersectionComplementsSoFar)==0:
            complement = sorted(Omega-set(intersectionSoFar))
            for m in range(len(intersectionSoFar)+1):
                for n1 in range(2**len(complement)):
                    yield makeSet(intersectionSoFar,2**m-1) | makeSet(complement,n1)
        elif len(intersectionComplementsSoFar)>0 and len(intersectionSoFar)==0:
            complement = sorted(Omega-set(intersectionComplementsSoFar))
            for m in range(len(intersectionComplementsSoFar)+1):
                for n1 in range(2**len(complement)):
                    yield makeSet(intersectionComplementsSoFar,2**m-1) | makeSet(complement,n1)
        else:
            complement = sorted(Omega-set(intersectionSoFar)-set(intersectionComplementsSoFar))
            for m in range(len(intersectionSoFar)+1):
                for n in range(len(intersectionComplementsSoFar)+1):
                    for p1 in range(2**len(complement)):
                        yield makeSet(intersectionSoFar,2**m-1) | makeSet(intersectionComplementsSoFar,2**n-1) | makeSet(complement,p1)
                
    if position >= len(variableTuple):
        yield dict
    else:
        for p in generateSets():
            dict = dict.copy()
            dict[variableTuple[position]] = p
            i1 = sorted(set(intersectionSoFar)&p)
            i2 = sorted(set(intersectionComplementsSoFar)-p)
            for d in generate(position+1,dict,intersectionSoFar=i1,intersectionComplementsSoFar=i2):
                yield d
        
foundCounterexample = False

for s in generate(0,globals()):
    if checkPremises(s) and not checkConclusion(s):
        foundCounterexample = True
        print(", ".join(str(variableTuple[i])+"="+str(s[variableTuple[i]]) for i in range(len(variableTuple))))
                
if not foundCounterexample:
    print("No counterexamples found.")
    