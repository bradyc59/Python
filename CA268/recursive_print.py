#!/usr/bin/env python3

def rprint(x, y):

    print(x)

    if x >= y - 1:

        return x

    return rprint(x + 1, y)
