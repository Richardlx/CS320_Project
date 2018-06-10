#####################################################################
#
# CAS CS 320, Fall 2015
# Midterm (skeleton code)
# compile.py
#
# Name: Laixian Wan
# BUID: U43250934
# Email: wanlx@bu.edu

from random import randint
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('optimize.py').read())
exec(open('machine.py').read())

Leaf = str
Node = dict
Array = list

def freshStr():
    return str(randint(0,10000000))

def compileExpression(env, e, heap):
    if type(e) == Leaf:
        if e == 'True':
            heap += 1
            insts = ['set ' + str(heap) + ' 1']
            addr = heap
            return (insts, addr, heap)
        elif e == 'False':
            heap += 1
            insts = ['set ' + str(heap) + ' 0']
            addr = heap
            return (insts, addr, heap)
        else:
            if e in env:
                heap += 1
                insts = ['set 3 ' + str(env[e]),\
                         'set 4 ' + str(heap),\
                         'copy'\
                         ]
                addr = heap
                return (insts, addr, heap)
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                n = children[0]
                heap = heap + 1
                return (['set ' + str(heap) + ' ' + str(n)], heap, heap)
            elif label == 'Variable':
                e1 = children[0]
                return compileExpression(env, e1, heap)
            elif label == 'Element':
                e1 = children[0]
                e2 = children[1]
                array = env[e1['Variable'][0]]
                insts2, index, heap = compileExpression(env, e2, heap)
                heap += 1
                instscopy2 = copyFromRef(0, heap)
                insts3 = ['set 1 ' + str(array),\
                          'set 3 ' + str(index),\
                          'set 4 2',\
                          'copy',\
                          'add'\
                          ] + instscopy2
                addr = heap
                return (insts2 + insts3, addr, heap)

def compileProgram(env, s, heap = 8): # Set initial heap default address.
    if type(s) == Leaf:
        if s == 'End':
            return (env, [], heap)

    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                [e, p] = children
                (instsE, addr, heap) = compileExpression(env, e, heap)
                (env, instsP, heap) = compileProgram(env, p, heap)
                return (env, instsE + copy(addr, 5) + instsP, heap)
            elif label == 'Assign':
                e1 = children[0]
                e2 = children[1]
                e3 = children[2]
                e4 = children[3]
                rest = children[4]
                array = e1['Variable'][0]
                insts1, addr, heap = compileExpression(env, e2, heap)
                insts2, n, heap = compileExpression(env, e3, heap)
                insts3, n, heap = compileExpression(env, e4, heap)
                env[array] = addr
                new_env, instsRest, heap = compileProgram(env, rest, heap)
                return (new_env, insts1 + insts2 + insts3 + instsRest, heap)
            elif label == 'Loop':
                mark = freshStr()
                e1 = children[0]
                e2 = children[1]
                body = children[2]
                rest = children[3]
                count = e1['Variable'][0]
                insts1, addr, heap = compileExpression(env, e2, heap)
                env[count] = addr
                env, insts0, heap = compileProgram(env, body, heap)
                instsBody = ['label startLoop' + mark,\
                             'branch LoopBody' + mark + ' ' + str(addr),\
                             'goto EndofLoop' + mark,\
                             'label LoopBody' + mark\
                             ]\
                             + insts0 +\
                             ['set 1 -1',\
                              'set 3 ' + str(addr),\
                              'set 4 2',\
                              'copy',\
                              'add',\
                              'set 3 0',\
                              'set 4 ' + str(addr),\
                              'copy',\
                              'goto startLoop' + mark,\
                              'label EndofLoop' + mark\
                              ] + insts0
                new_env, instsRest, heap = compileProgram(env, rest, heap)
                return (new_env, insts1 + instsBody + instsRest, heap)
                
                
def compile(s):
    p = tokenizeAndParse(s)

    if not typeProgram({}, p) is None:
        s = foldConstants(p)
        k = eliminateDeadCode(s)
        (env, insts, heap) = compileProgram({}, k)
        return insts

def compileAndSimulate(s):
    return simulate(compile(s))

#eof
