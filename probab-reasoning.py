def makeSet(binary):
    s = set()
    x = 1
    while binary:
        if binary&1:
            s.add(x)
        x += 1
        binary >>= 1
    return s
    
sides = 6
    
def P(*s):
    if len(s) > 1:
        return P(s[0] & s[1]) / P(s[1])
    return len(s[0]) / float(sides)
    
def supports(p,q):
    return P(q) < P(q,p)
    
def checkPremises(a,b,c):
    try:
        return P(a,c) > P(a,b)
    except:
        return False
        
def checkConclusion(a,b,c):
    try:
        return P(a, b|c) > P(a, b) 
    except:
        return False
   
for m1 in range(sides): 
    for n2 in range(2**sides): 
        for n3 in range(2**sides):
            n1 = 2**m1-1
            p = makeSet(n1)
            q = makeSet(n2)
            r = makeSet(n3)
            
            if checkPremises(p,q,r) and not checkConclusion(p,q,r):
                print(p,q,r)
