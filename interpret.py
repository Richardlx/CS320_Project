#####################################################################
#
# CAS CS 320, Fall 2015
# interpret.py
#
# Name: Laixian Wan
# BUID: U43250934
# Email: wanlx@bu.edu

exec(open('parse.py').read())
exec(open('analyze.py').read())

Node = dict
Leaf = str

def evalExpression(env, e):
    ''' evaluates input e as an expression. '''
    if type(e) == Leaf:
        if e == 'True' or e == 'False':
            return e
        elif e in env:
            return env[e]
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                return e
            elif label == 'Variable':
                return evalExpression(env, children[0])
            elif label == 'Plus':
                e1 = children[0]
                e2 = children[1]
                value1 = evalExpression(env, e1)
                value2 = evalExpression(env, e2)
                return {'Number':[unwarp(env, value1) + unwarp(env, value2)]}
            elif label == 'Element':
                e1 = children[0]
                e2 = children[1]
                array = evalExpression(env, e1)
                index = evalExpression(env, e2)
                return array[unwarp(env, index)]
                

def unwarp(env, node):
    ''' helper function which unwarps the content of the input node. '''
    if type(node) != Node: # If the input node doesn't need to be unwarpped, do nothing
        return node
    else:
        for label in node:
            if label == 'Number':
                return node['Number'][0]
            

def execProgram(env, s):
    ''' executes an abstract syntax tree s and returns its output with a updated environment. '''
    if type(s) == Leaf:
        if s == 'End':
            return (env, [])
    elif type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                [e,p] = s[label]
                v = evalExpression(env, e)
                (env, o) = execProgram(env, p)
                return (env, [v] + o)
            elif label == 'Assign':
                e1 = children[0]
                e2 = children[1]
                e3 = children[2]
                e4 = children[3]
                rest = children[4]
                name = e1['Variable'][0]
                value1 = evalExpression(env, e2)
                value2 = evalExpression(env, e3)
                value3 = evalExpression(env, e4)
                env[name] = [value1, value2, value3]
                new_env, output = execProgram(env, rest)
                return new_env, output
            elif label == 'Loop':
                e1 = children[0]
                e2 = children[1]
                body = children[2]
                rest = children[3]
                loop_control = evalExpression(env, e2)
                if unwarp(env, loop_control) < 0:
                    new_env, output = execProgram(env, rest)
                    return new_env, output
                loop_control = {'Number':[unwarp(env, loop_control) - 1]}
                name = e1['Variable'][0]
                env[name] = loop_control

                env, output1 = execProgram(env, body)

                new_env, output2 = execProgram(env, {'Loop':[e1, {'Variable':[name]}, body, rest]})
                return new_env, output1 + output2
                

def interpret(s):
    tokens = tokenizeAndParse(s)
    if not typeProgram({}, tokens) is None:
        new_env, output = execProgram({}, tokens)
        return output

#eof
