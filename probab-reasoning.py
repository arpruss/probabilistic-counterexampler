import sys

sides = 6

if len(sys.argv)>2:
    premises = sys.argv[1:-1]
    conclusion = sys.argv[-1]
else:
    print("python probab-reasoning.py premise1 premise2 ... conclusion")
    print("The premises and conclusion can contain three events: a,b,c.")
    print("Boolean operations allowed:")
    print(" a&b : conjunction of a with b")
    print(" a|b : disjunction of a with b (not to be confused with conditional probability)")
    print(" ~a  : negation of a")
    print("Probabilistic operations allowed:")
    print(" P(a) : unconditional probability of a")
    print(" P(a,b) : conditional probability of a given b")    
    print(" supports(a,b) : short for: P(a,b) > P(a)")
    print("You can operate on the probabilities with standard arithmetical operations and comparisons.")
    print("Any expression which involves a divide by zero counts as automatically false.") 
    sys.exit(1)

#premises = [ "P(a, c) > P(a, b)" ]
#conclusion = "P(a, b|c) > P(a,b)"

Omega = set(range(1,sides+1))

class mySet(set):
    def __invert__(self):
        return Omega-self
        
    def __str__(self):
        return str(sorted(list(self))).replace("[","{").replace("]","}")

def makeSet(binary):
    s = mySet()
    x = 1
    while binary:
        if binary&1:
            s.add(x)
        x += 1
        binary >>= 1
    return s
    
def P(*s):
    if len(s) > 1:
        return P(s[0] & s[1]) / P(s[1]) 
    return len(s[0]) / float(sides)
    
def supports(p,q):
    return P(q) < P(q,p)
    
def checkPremises(a,b,c):
    try:
        for premise in premises:
            if not eval(premise):
                return False
        return True
    except ZeroDivisionError:
        return False
        
def checkConclusion(a,b,c):
    try:
        return eval(conclusion)
    except ZeroDivisionError:
        return False

foundCounterexample = False        
for m1 in range(sides): 
    for n2 in range(2**sides): 
        for n3 in range(2**sides):
            n1 = 2**m1-1
            p = makeSet(n1)
            q = makeSet(n2)
            r = makeSet(n3)
            
            if checkPremises(p,q,r) and not checkConclusion(p,q,r):
                foundCounterexample = True
                print("a="+str(p)+", b="+str(q)+", c="+str(r))
if not foundCounterexample:
    print("No counterexamples found.")
    