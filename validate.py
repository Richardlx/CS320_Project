#####################################################################
#
# CAS CS 320, Fall 2015
# validate.py
#
# Name: Laixian Wan
# BUID: U43250934
# Email: wanlx@bu.edu

exec(open('analyze.py').read())
exec(open('interpret.py').read())
exec(open('compile.py').read())

def convertValue(v):
    if type(v) == Leaf:
        if v == 'True':
            return 1
        elif v == 'False':
            return 0 # Complete for Problem #5.
    if type(v) == Node:
        for label in v:
            return 1 # Complete for Problem #5.

# Converts an output (a list of values) from the
# value representation to the machine representation
def convert(o):
    return [convertValue(v) for v in o]

def expressions(n):
    if n <= 0:
        return []
    elif n == 1:
        return ['True', 'False', {'Number':[1]}, {'Element':[{'Variable':['a']}, {'Number':[1]}]}] # Add all base case(s) for Problem #5.
    else:
        es = expressions(n - 1)
        return es + expressions(1)

def programs(n):
    if n <= 0:
        return []
    elif n == 1:
        return ['End'] # Add base case(s) for Problem #5.
    else:
        ps = programs(n-1)
        es = expressions(n-1)
        psN = []
        psN += [{'Print':[exp, p]} for exp in es for p in ps]
        psN += [{'Assign':['a', e1, e2, e3, p]} for e1 in es if type(e1) == Node for e2 in es if type(e2) == Node for e3 in es if type(e3) == Node for p in ps]
        psN += [{'Loop':['x', 1, p1, p2]} for p1 in ps for p2 in ps]

        return ps + psN
   
# Compute the formula that defines correct behavior for the
# compiler for all program parse trees of depth at most k.
# Any outputs indicate that the behavior of the compiled
# program does not match the behavior of the interpreted
# program.

def exhaustive(k):
    for p in programs(k):
        try:
            if simulate(compileProgram({}, p)[1]) != convert(execProgram({}, p)[1]):
                print('\nIncorrect behavior on: ' + str(p))
        except:
            print('\nError on: ' + str(p))

#eof
