#####################################################################
#
# CAS CS 320, Fall 2015
# analyze.py
#
# Name: Laixian Wan
# BUID: U43250934
# Email: wanlx@bu.edu

exec(open('parse.py').read())

Node = dict
Leaf = str
Array = list

def typeExpression(env, e):
    if type(e) == Leaf:
        if e == 'True' or e == 'False':
            return 'TyBoolean'
        
    elif type(e) == Array:
        return 'TyArray'
    
    elif type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                return 'TyNumber'

            elif label == 'Variable':
                e1 = children[0]
                return typeExpression(env, env[e1])

            elif label == 'Element':
                e1 = children[0]
                e2 = children[1]
                tye1 = typeExpression(env, env[e1])
                tye2 = typeExpression(env, e2)
                if tye1 == 'TyArray' and tye2 == 'Number':
                    return 'TyNumber'

            elif label == 'Plus':
                e1 = children[0]
                e2 = children[1]
                tye1 = typeExpression(e1)
                tye2 = typeExperssion(e2)
                if tye1 == tye2 == 'TyNumber':
                    return 'TyNumber'

def typeProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return 'TyVoid'
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                [e, p] = s[label]
                typ = typeProgram(env, p)
                if typ == 'TyVoid':
                    return 'TyVoid'
            if label == 'Assign':
                [xTree, e0, e1, e2, p] = s[label]
                x = xTree['Variable'][0]
                tye0 = typeExpression(env, e0)
                tye1 = typeExpression(env, e1)
                tye2 = typeExpression(env, e2)
                env[x] = Array
                typ = typeProgram(env, p)
                if tye0 == tye1 == tye2 == 'TyNumber':
                    if typ == 'TyVoid':
                        return 'TyVoid'
            if label == 'Loop':
                [xTree, nTree, p1, p2] = s[label]
                x = xTree['Variable'][0]
                tyn = typeExpression(env, nTree)
                env[x] = 'TyNumber'
                typ1 = typeProgram(env, p1)
                typ2 = typeProgram(env, p2)
                if typ1 == typ2 == 'TyVoid':
                    if tyn == 'TyNumber':
                        return 'TyVoid'

#eof
