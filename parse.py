#####################################################################
#
# CAS CS 320, Fall 2015
# parse.py
#
# Name: Laixian Wan
# BUID: U43250934
# Email: wanlx@bu.edu


import re

def number(tokens, top = True):
    if re.compile(r"(-(0|[1-9][0-9]*)|(0|[1-9][0-9]*))").match(tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])

def variable(tokens, top = True):
    if re.compile(r"[a-z][A-Za-z0-9]*").match(tokens[0]):
        return ({"Variable": [tokens[0]]}, tokens[1:])

def expression(tmp, top = True):
    ''' returns the parse tree for vaild input tmp. '''
    tokens = tmp[0:]
    r = left(tokens, False)
    if not r is None:
        temp, tokens = r
        if len(tokens) != 0 and tokens[0] == '+':
            tokens = tokens[1:]
            r = expression(tokens, False)
            if not r is None:
                temp2, tokens = r
                if not top or len(tokens) == 0:
                    return {'Plus':[temp, temp2]}, tokens
        else:
            if not top or len(tokens) == 0:
                return temp, tokens
    

def left(tmp, top = True):
    ''' Impliment of left recursion elimination on BNF notation of expression. '''
    tokens = tmp[0:]
    if tokens[0] == 'true':
        return 'True', tokens[1:]
    elif tokens[0] == 'false':
        return 'False', tokens[1:]
    elif tokens[0] == '$':
        tokens = tokens[1:]
        r = variable(tokens, False)
        if not r is None:
            temp, tokens = r
            return {'Variable':[temp]}, tokens
    elif tokens[0] == '@':
        tokens = tokens[1:]
        r = variable(tokens, False)
        if not r is None:
            temp1, tokens = r
            if tokens[0] == '[':
                tokens = tokens[1:]
                r = expression(tokens, False)
                if not r is None:
                    temp2, tokens = r
                    if tokens[0] == ']':
                        tokens = tokens[1:]
                        return {'Element':[temp1, temp2]}, tokens
    else:
        r = number(tokens, False)
        if not r is None:
            temp, tokens = r
            return temp, tokens

def program(tmp, top = True):
    ''' returns parse tree for valid input tmp. '''
    tokens = tmp[0:]
    if tokens == []:
        return 'End', []
    elif tokens[0] == '@':
        tokens = tokens[1:]
        r = variable(tokens, False)
        if not r is None:
            temp, tokens = r
            if tokens[0] == ':=' and tokens[1] == '[':
                tokens = tokens[2:]
                r = expression(tokens, False)
                if not r is None:
                    temp1, tokens = r
                    if tokens[0] == ',':
                        tokens = tokens[1:]
                        r = expression(tokens, False)
                        if not r is None:
                            temp2, tokens = r
                            if tokens[0] == ',':
                                tokens = tokens[1:]
                                r = expression(tokens, False)
                                if not r is None:
                                    temp3, tokens = r
                                    if tokens[0] == ']' and tokens[1] == ';':
                                        tokens = tokens[2:]
                                        if not top:
                                            return {'Assign':[temp, temp1, temp2, temp3, 'End']}, tokens                                            
                                        r = program(tokens, True)
                                        if not r is None:
                                            rest, tokens = r
                                            return {'Assign':[temp, temp1, temp2, temp3, rest]}, tokens
    elif tokens[0] == 'print':
        tokens = tokens[1:]
        r = expression(tokens, False)
        if not r is None:
            temp, tokens = r
            if tokens[0] == ';':
                tokens = tokens[1:]
                if not top:
                    return {'Print':[temp, 'End']}, tokens
                r = program(tokens, True)
                if not r is None:
                    rest, tokens = r
                    return {'Print':[temp, rest]}, tokens
    elif tokens[0] == 'loop' and tokens[1] == '$':
        tokens = tokens[2:]
        r = variable(tokens, False)
        if not r is None:
            temp, tokens = r
            if tokens[0] == 'from':
                tokens = tokens[1:]
                r = number(tokens, False)
                if not r is None:
                    temp1, tokens = r
                    if tokens[0] == '{':
                        tokens = tokens[1:]
                        r = program(tokens, False)
                        if not r is None:
                            temp2, tokens = r
                            if tokens[0] == '}':
                                tokens = tokens[1:]
                                if not top:
                                    return {'Loop':[temp, temp1, temp2, 'End']}, tokens
                                r = program(tokens, True)
                                if not r is None:
                                    rest, tokens = r
                                    return {'Loop':[temp, temp1, temp2, rest]}, tokens
                        

def tokenizeAndParse(s):
    ''' returns a parse tree for vaild input string s. '''
    tokens = re.split(r"(\s+|:=|print|\+|loop|from|{|}|;|\[|\]|,|@|\$)", s)
    tokens = [t for t in tokens if not t.isspace() and not t == ""]
    tree, tokens = program(tokens, True)
    return tree

#eof
