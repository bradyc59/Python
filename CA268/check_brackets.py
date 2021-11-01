#!/usr/bin/env python3

def check_brackets(line):
    brac = "[{()}]"
    string = "".join(a for a in line if a in brac)
    
    stack = []
    for pos in range(len(string)):
        if string[pos] == '[' or string[pos] == '(' or string[pos] == '{':
            stack.append(string[pos])

        if len(stack) == 0:
            return False

        if string[pos] == '}':
            pop = stack.pop()
            if (pop == '[') or (pop == '('):
                return False

        elif string[pos] == ')':
            pop = stack.pop()
            if (pop == '[') or (pop == '{'):
                return False

        elif string[pos] == ']':
            pop = stack.pop()
            if (pop == '(') or (pop == '{'):
                return False
    if len(stack):
        return False

    else:
        return True
